# Author : Umar Azam 
# Date   : 28th August 2023 11:09AM

# %%

import csv
import json 

# %%
# Location of the input file with the differential DB Structure
file_location = "./Differential_DB_structure_DB777.csv"

# Location and name of the output file 
output_file_name = 'DB777_block1_struct.json'

table_start = False
table_entries = {}
table_name = ''


# Open the CSV file for reading
with open(file_location, 'r') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)
    
    # Loop through each row in the file
    for row in csv_reader:
        if ('Level' in row[0] and row[1] == ''):
            table_start = True
            table_name = row[0]
            continue

        if ('' == row[0]):
            table_start = False

        if (table_start):
            table_entries[table_name] = table_entries.get(table_name,[]) + [row]
        #print(row)


# %%

# Adding information about offsets to use in parsing later on 
# After assigning information about the size of a data structure
# the offsets of any data types at the lower level can be compared against
# the upper level to see if they're nested under the bigger data structure
# E.G. An array of 10 USInts is 10 bytes long, each 1 byte element
# Under it will have an offset within the start and end offsets of the 
# Upper level 

for key in table_entries.keys():
    num_rows = len(table_entries[key])
    for i in range(1,num_rows):
        current_offset = table_entries[key][i][2]
        if (i == num_rows - 1 ):
            next_offset  = 99999
        else :
            next_offset = table_entries[key][i+1][2]
        
        table_entries[key][i].append({'start' : float(current_offset) , 'end' : float(next_offset)})


# %%

# Generate structure containing information about what elements of the lower level
# structure are contained under a higher level structure. e.g. array of INTs is higher
# level structure, once expanding the row, the lower level individual INTs are visible
def level_struct_generator(upper_level, lower_level, upper_level_key = 'upper',lower_level_key='lower'):
    struct_definition = {}
    for i in range(1,len(upper_level)):
        upper_start = upper_level[i][-1]['start']
        upper_end = upper_level[i][-1]['end']
        for j in range(1,len(lower_level)):
            if (upper_level[i][:3] == lower_level[j][0:3]):
                continue
            lower_start = lower_level[j][-1]['start']
            lower_end = lower_level[j][-1]['end']
            if (lower_end - lower_start < 0.001): # Float operations can have issues with equality comparison (==)
                continue
            if (lower_start >= upper_start and lower_end <= upper_end):
                struct_definition[f'{upper_level_key}-{i}'] = struct_definition.get(f'{upper_level_key}-{i}',[]) + [f'{lower_level_key}-{j}']
    return struct_definition
                


    
# View example of structure
#level_struct_generator(table_entries['Level 1'],table_entries['Level 2'])
# %%


# Generate level structure for all the levels in the csv structure file
DB_struct = []
key_list = list(table_entries.keys())
for i in range(len(table_entries)-1,0,-1):
    #print(i)
    # Starting from the second last and last level
    #print(f'Upper {key_list[i-1]} \nLower {key_list[i]} \n')
    DB_struct.append(level_struct_generator(table_entries[key_list[i-1]],
                                            table_entries[key_list[i]],
                                            upper_level_key=key_list[i-1], 
                                            lower_level_key=key_list[i]))
    

# 
# for level in DB_struct:
#     print(level.keys())

# 
# for item in key_list:
#     print(table_entries[item])

# %%
1
# extract level and index information from the location string
def level_index_split(key_string):
    level, index = key_string.split('-')
    return level, int(index)


# %%

def table_access(table,key):
    key_level,key_ind = level_index_split(key)
    return table[key_level][key_ind]




lowest_level_key = key_list[-1]
db_data_list_full = table_entries[lowest_level_key]
db_data_index = {f'fullind-{index}' : {} for index in range(len(table_entries[lowest_level_key]))}
db_struct = DB_struct.copy()
complete_struct = {}

key2ind = lambda x : int(x.split('-')[-1])

# %%

# Generate the structure by going through the level structure comparisons one by one
for level in db_struct:
    level_keys = list(level.keys())
    key_counter = 0
    #print(level_keys)
    skip_counter = 0
    
    
    db_data_index_keylist = list(db_data_index.keys())
    for index,db_data_key in enumerate(db_data_index_keylist):
        if (skip_counter > 0):
            skip_counter -= 1
            continue
        if (db_data_list_full[key2ind(db_data_key)][:3] == table_access(table_entries,level_keys[key_counter])[:3]):
            temp_dict = {}
            for key in level[level_keys[key_counter]]:
                skip_counter += 1
                updated_key = db_data_index_keylist[index+skip_counter]
                

                if (db_data_list_full[key2ind(updated_key)][:3]) != table_access(table_entries,key)[:3]:
                    print("ERROR IN PARSING")
                else :
                    temp_dict.update({updated_key : db_data_index[updated_key]})
                    db_data_index.pop(updated_key)

            db_data_index[db_data_key].update(temp_dict)

            
            key_counter = min(key_counter+1, len(level_keys)-1) 


# %%

storage_structure = {}

# Recursive function to navigate the nested tree structure
# Implementing depth first traversal
def directory_printer(struct,key = '', storage = {}):
    if (len(struct.keys()) == 0):
        return -1
    else :
        for struct_key in struct.keys():
            if (directory_printer(struct[struct_key],f'{key}\{struct_key}',storage) == -1):
                data_row = db_data_list_full[key2ind(struct_key)]
                temp_str = ''
                if (key != ''):
                    temp_str = '\\'.join([db_data_list_full[key2ind(item)][0] for item in key.split('\\') if item != ''])
                    directory_struct_key = '\\' + temp_str + '\\' + data_row[0]
                    storage[directory_struct_key] = data_row
                    #print(directory_struct_key)

# %%


directory_printer(db_data_index, storage = storage_structure)



# Save 
with open(output_file_name,'w') as json_output:
    json.dump(storage_structure,json_output,indent=4)
# %%

# Use the Differential_DB_structure_DB778.csv (during testing) file to extract data for testing

# %%

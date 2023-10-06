# DB Structure Extractor


## Overview

This script is designed to read a CSV file containing the structure of a database and generate a JSON file that represents that structure. It is written in Python and uses the built-in `csv` and `json` modules for parsing and generating files, respectively.



## Dependencies

- Python 3.9

## How to Run

1. Place your CSV file containing the database structure in the same directory as the script or specify the file's directory in the `file_location` variable inside the script.

    ```python
    file_location = "./Your_CSV_File.csv"
    ```

2. Specify the name and location of the output JSON file in the `output_file_name` variable.

    ```python
    output_file_name = 'Your_Output_File.json'
    ```

3. Run the script.

    ```bash
    python DB_structure_extractor.py
    ```

## Input CSV File Format


The input CSV file should contain the database structure in a specific format. The script assumes this format while parsing. Kindly refer to the sample input file for clarity. See the `Differential_DB_structure_DB778.csv` sample file for this structure and to test functionality. Also note that the structure for `Differential_DB_structure_DB778.csv` has been generated from a Siemens TIA project `Data_test_project.zip` available in this repo. The TIA project contains the Actual DB
that is used to generate the differential DB structure file. 

## Output JSON File

The script will generate a JSON file containing the parsed database structure, saved as per the `output_file_name` variable.

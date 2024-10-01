# Fordjupad-Pythonprogrammering

This Kunskapskontroll Python script is designed to clean and preprocess a dataset related to student performance. It is primarily focusing on ensuring that the dataset is properly formatted for further analysis or database updates. The script uses the DataCleaner class to perform a series of cleaning operations on a CSV file.

Design: The cleaning operations are implemented within a class. 
Logging: The script logs important actions, warnings and errors during data processing. 

Cleaning Methods:
1. read_data():
    -	This method loads a CSV dataset into a Pandas DataFrame.
    -	It checks the existence of the file and logs an error if the file cannot be found.
2. rename_columns():
    -	Automatically rename columns.
3. drop_duplicated():
    -	Removes duplicate rows from the dataset.
4. drop_missing():
    -	Removes rows with empty or NaN values.
5. strip_columns():
    -	Removes leading and trailing whitespace from the values in string columns.
6. clean_values():
    -	Removes unnecessary special characters from specific columns.
7. clean_date():
    -	Cleans date-related column ensuring the values are properly formatted.
8. process_date_column():
    -	Converts date columns into format (YYYY-MM-DD).
Exception Handling:
    -	The script includes basic exception handling.

Usage:
Run it after specifying the file path of the dataset. 
The output will be a cleaned DataFrame that will be saved as a CSV file.

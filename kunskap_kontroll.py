# %%
import pandas as pd     # Pandas library for data manipulation and analysis.
import logging          # Logging module for tracking and logging execution events.
import datetime as dt   # Datetime module for manipulation of date and time.
import os               # OS module for interacting with the operating system.

class DataCleaner:
    
    def __init__(self, dir: str):
        self.directory = dir
        self.log_path = None
        self.data_path = None
        self.log_filename: str = "program_logging.log"
        self.data_filename: str = "Students_Performance.csv"
        self.column_list: list[str] = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course', 'math score', 'reading score', 'writing score', 'date']
        self.encoding_list: list[str] = ["utf-8", "utf-16", "ISO-8859-1", "cp1252"]
        self.nan_list: list[str] = ["?", "NA", "n/a", "na", "Null", "NaN", "#####"]
        self.exclude_columns: list[str] = None
        self.df: pd.DataFrame = None

    def directory_path(self) -> str:
        """
        Ensures that a valid directory path exists for the log file and data file. 
        Returns:
            str: The valid directory path.
        """
        directory: str = self.directory
        
        if not os.path.isdir(directory):
            print(f"Warning: [The directory '{directory}' does not exist]")
            logging.warning(f"The directory [{directory}] does not exist. Prompting user for a new path.")
            
            while True:
                directory = input("Please enter the correct directory path: ")
                
                if os.path.isdir(directory):
                    logging.info(f"Valid directory path provided by the user: [{directory}]")
                    break
                else:
                    print(f"Warning: [The entered directory '{directory}' does not exist]")
                    logging.warning(f"User provided an invalid directory path: [{directory}]. Prompting for a new path.")
        
        self.directory = directory
        return self.directory
        
    def logging_path(self) -> str:
        """
        Retrieves or creates the log file and returns the path.
        Returns:
            str: The valid path of the log file. 
        """
        directory: str = self.directory_path()
        log_filename: str = self.log_filename
        
        log_path: str = os.path.join(directory, log_filename)
        
        if not os.path.isfile(log_path):
            logging.info(f"[{log_filename}] does not exist. A new file will be created.")
            try: 
                open(log_path, "a").close()
                logging.info(f"Log file [{log_filename}] has been created at [{directory}]")
                self.log_path = log_path
                return self.log_path
                
            except OSError as e:
                print(f"Operating System Error creating [{log_filename}] file: {e}")
                logging.warning(f"Operating System Error creating [{log_filename}] file: {e}")
                return ""
            
        else:
            logging.info(f"Log file [{log_filename}] already exists")
            self.log_path = log_path
            return self.log_path
        
    def configure_logging(self):
        """
        Configures the logging with the log file path.
        """
        log_path: str = self.logging_path()
        
        logging.basicConfig(
            filename=log_path, 
            filemode="a", 
            force=True, 
            level=logging.INFO, 
            format="[%(asctime)s][%(levelname)s]: [%(message)s]"
        )
       
    def dataset_path(self) -> str:
        """
        Retrieves the path for the data source file.
        Returns:
            str: The valid path of the data source file.    
        """
        directory: str = self.directory_path()
        data_filename: str = self.data_filename
        
        data_path: str = os.path.join(directory, data_filename)
        
        if not os.path.exists(data_path):
            print("Warning: [The data source does not exist]")
            logging.warning(f"Data source [{data_filename}] does not exist at [{directory}]. Prompting user for a new path.")
                
            while True:
                data_path: str = input("Please enter the correct path for the data file: ")
                
                if os.path.exists(data_path):
                    logging.info(f"New data source file has been identified by the user at: [{data_path}]")
                    break
                
                else:
                    print("Warning: [The entered data source path does not exist]")
                    logging.warning(f"User provided an invalid data path: [{data_path}]. Please re-enter.")


        logging.info(f"Data source [{data_filename}] exists at [{directory}]")
        self.data_path = data_path
        return self.data_path

    def read_data(self) -> pd.DataFrame:
        """
        Reads data from a CSV file using various encodings and replaces certain specified strings 
        as missing values (NaN).
        Returns: 
            pd.DataFrame: The data from the CSV file.
        """
        data_path: str = self.dataset_path()
        encoding_list: list[str] = self.encoding_list
        nan_list: list[str] = self.nan_list
        
        for encoding in encoding_list:
            try:
                df: pd.DataFrame = pd.read_csv(
                    data_path, 
                    encoding=encoding, 
                    keep_default_na=True, 
                    na_values=nan_list, 
                    header=0
                )
                
                logging.info(f"Successfully read file with encoding: {encoding.upper()}")
                self.df = df
                return self.df
            
            except UnicodeError as e:
                logging.warning(f'UnicodeError with encoding {encoding.upper()}: {str(e)}')
            
            except FileNotFoundError:
                logging.error(f"File not found: {data_path}")
                raise FileNotFoundError(f"Could not find file at: {data_path}")
            
            except Exception as e:
                logging.error(f"Error reading file with encoding {encoding.upper()}: {str(e)}")
                print(f"Encoding attempt using {encoding.upper()} failed for the file.")
        
        raise ValueError(f"All encoding attempts failed for the data file at: [{data_path}]")
       
    def rename_columns(self) -> pd.DataFrame:
        """
        Renames the header of the columns in the dataframe.
        Returns: 
            pd.DataFrame: DataFrame with renamed columns or original DataFrame if lengths do not match.
        """
        df = self.read_data()
        
        old_names = df.columns
        new_names = self.column_list
        
        if len(old_names) != len(new_names):
            logging.warning(f"Number of old columns ({len(old_names)}) does not match number of new names ({len(new_names)}). No changes have been made to the column headers.")
            return df 
        
        df = df.rename(columns=dict(zip(old_names, new_names)))
        
        logging.info(f"Renamed dataframe columns: {df.columns.tolist()}")
        
        self.df = df
        return self.df    
                
    def dataset_info(self) -> None:
        """
        Log information about the dataset, including duplicates and missing values.
        """
        df = self.df
        
        # Log DataFrame info
        logging.info(f"Dataset Shape: Rows [{df.shape[0]}] : Columns [{df.shape[1]}]")
        logging.info(f"Column Names: Rows {df.columns.tolist()}")
        logging.info(f"Column Data Types: {[f"{col}: {dtype}" for (col, dtype) in df.dtypes.items()]}")
        logging.info(f"Null Value Counts: {df.isna().sum().to_dict()}") 
        
        # Calculate missing values and duplicates efficiently
        missing_count = df.isna().sum()
        duplicated_count = df.duplicated().sum()
        
        # Log missing values for non-zero counts
        missing_info = missing_count[missing_count > 0].to_dict()
        logging.info(f"Missing values: {missing_info}")
        
        # Log duplicate information
        logging.info(f"Duplicated rows: the dataset has {duplicated_count} duplicated rows.")

    def drop_duplicated(self) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataframe.
        Returns: 
            pd.DataFrame: DataFrame with duplicates removed
        """
        df: pd.DataFrame = self.df
        
        # Store the number of rows before and after dropping duplicates
        rows_before = len(df)
        
        df.drop_duplicates(keep="first", inplace=True)
        
        rows_after = len(df)
        rows_dropped = rows_before - rows_after

        # Log the number of duplicates dropped and the new total number of rows
        logging.info(f"DUPLICATED rows: dropped [{rows_dropped}] out of [{rows_before}] rows. The new dataset includes: [{rows_after}] rows.")
        
        self.df = df
        return self.df

    def drop_missing(self) -> pd.DataFrame:
        """
        Remove rows with missing values in specified columns.
        Returns: 
        pd.DataFrame: DataFrame with rows containing missing values removed
        """
        df = self.df
        exclude_columns = self.exclude_columns

        rows_before = len(df)
        
        if exclude_columns is None:
            exclude_columns = []
        
        subset = [col for col in df.columns if col not in exclude_columns]
        df.dropna(axis=0, how="any", subset=subset, inplace=True)
        
        rows_after = len(df)
        rows_dropped = rows_before - rows_after

        logging.info(f"MISSING values: dropped {rows_dropped} rows out of {rows_before} rows. New dataset has {rows_after} rows.")

        self.df = df
        return self.df

    def strip_columns(self) -> pd.DataFrame:
        """
        Strips leading and trailing whitespace in columns with string datatype.
        Returns: 
            pd.DataFrame: DataFrame with cleaned string columns
        """
        df = self.df
        
        info: dict[str, int] = {}
        for col in df.columns:
            if df[col].dtype == object or df[col].dtype == 'string':
                original_values = df[col].values
                df[col] = df[col].str.strip()
                stripped_count: int = int(sum(original_values != df[col].values))
                info[col] = int(stripped_count)

        logging.info(f"Number of stripped leading and trailing whitespace: {info}")    

        self.df = df
        return self.df
    
    def clean_values(self) -> pd.DataFrame:
        """_summary_
        Cleans values in DataFrame columns
        Returns:
            pd.DataFrame: DataFrame with cleaned values
        """

        df = self.df

        correction_dict: dict = {
            "gender": {
                "female": ["F", "f", "Fe", "fe"],
                "male": ["M", "m", "Ma", "ma"]
            },
            "race/ethnicity": {
                "group A": ["A", "a", "groupA", "groupa", "group A", "group a"],
                "group B": ["B", "b", "groupB", "groupb", "group B", "group b"],
                "group C": ["C", "c", "groupC", "groupc", "group C", "group c"],
                "group D": ["D", "d", "groupD", "groupd", "group D", "group d"],
                "group E": ["E", "e", "groupE", "groupe", "group E", "group e"]
            },
            "lunch": {
                "free/reduced": ["free/???", "free/\\reduced"]
            }
        }

        expected_dict: dict = {
            "gender": ["female", "male"],
            "race/ethnicity": ["group A", "group B", "group C", "group D", "group E"],
            "parental level of education": ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"],
            "test preparation course": ["none", "completed"],
            "lunch": ["free/reduced", "standard"]
        }

        for col in correction_dict:
            if col not in df.columns:
                logging.warning(f"Column [{col}] not found in the DataFrame.")
                continue
            logging.info(f"Column [{col}] original values: {df[col].value_counts().to_dict()}")
            _dict: dict = {val: key
                            for key in correction_dict[col] 
                            for val in correction_dict[col][key]
                            }
            df[col] = df[col].replace(_dict)
            logging.info(f"Column [{col}] cleaned values:{df[col].value_counts().to_dict()}")
        
        for col in correction_dict:
            if col in expected_dict:
                expected_values: list[str] = [key for key in expected_dict[col]]
                unique_values: list[str] = list(df[col].unique())
                unexpected_values : list[str] = [val for val in unique_values if val not in expected_values]
                if unexpected_values:
                    logging.warning(f"Unexpected values has been found in [{col}] column after cleaning: {unexpected_values}")
            else:
                pass

        self.df = df
        return self.df

    def clean_date(self) -> pd.DataFrame:
        """
        Cleans date column replacing multiple consecutive slashes with a single slash.
        Returns:
            pd.DataFrame: DataFrame with cleaned date column.
        """
        
        df = self.df
        
        initial_count = df["date"].str.count("//").sum()
        
        df["date"] = df["date"].str.replace(r"/+", "/", regex=True)
        
        if df["date"].str.contains("//").any():
            logging.warning("Not all consecutive slashes were replaced in the 'date' column")
            
        remaining_count = df["date"].str.count("//").sum()
        
        replaced_count = initial_count - remaining_count
        
        logging.info(f"[{replaced_count}] consecutive slashes were replaced in the 'date' column")     
        
        if remaining_count > 0:
            logging.warning(f"[{remaining_count}] double slashes remain in the 'date' column")

        self.df = df
        return self.df

    
    def process_date_column(self) -> pd.DataFrame:
        """
        Process the 'date' column in a DataFrame to standardize date format.
        Returns: pd.DataFrame: DataFrame with processed 'date' column.
        """
        df = self.df
        
        def parse_date(date_string: str) -> dt.datetime:
            """
            Parse a date string using multiple formats.
            Args: date_string (str): The date string to parse.
            Returns: dt.datetime: Parsed datetime object if successful, date_string (str) if not.
            """
            date_formats = [
                "%d.%m.%Y",  # for "15.03.2020"
                "%d%m%Y",    # for "15032020"
                "%d/%m/%Y",  # for "15/03/2020"
                "%d-%m-%Y",  # for "15-03-2020"
                "%m/%d/%Y",  # for "03/15/2020"
                "%Y/%m/%d"   # for "2020/03/15"
            ]

            for fmt in date_formats:
                try:
                    return dt.datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
            
            logging.warning(f"Unable to parse date: {date_string}")

            return date_string
        
        df["date"] = df["date"].astype(str)
        df["date"] = df["date"].apply(parse_date)
        df["date"] = df["date"].apply(lambda val: dt.datetime.strftime(val, "%Y-%m-%d") if isinstance(val, dt.datetime) else val)
        
        self.df = df
        return self.df

# Execution

if __name__ == "__main__":
    try:
        cleaner = DataCleaner(dir=r"C:\Users\aghaa\OneDrive\Desktop\Kunskap_2")
        cleaner.directory_path()
        cleaner.logging_path()
        cleaner.configure_logging()
        cleaner.dataset_path()
        cleaner.read_data()
        cleaner.rename_columns()
        cleaner.dataset_info()
        
        cleaner.drop_duplicated()
        cleaner.drop_missing()
        cleaner.strip_columns()
        cleaner.clean_values()
        cleaner.clean_date()
        cleaner.process_date_column()
        
        output_dir: str = r"C:\Users\aghaa\OneDrive\Desktop\Kunskap_2"
        output_file: str = "cleaned_students_performance.csv"
        output_path: str = os.path.join(output_dir, output_file)
        try: 
            cleaner.df.to_csv(path_or_buf= output_path, mode="w", index=False)
            logging.info(f"Cleaned data file saved at [{output_path}]")
        except Exception as sav:
            logging.error(f"File saving ERROR occered [{sav}]")
    
    except Exception as per:
        logging.error(f"File processing ERROR occered: [{per}]")
    

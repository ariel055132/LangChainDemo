import argparse
import pandas as pd
import os


def load_excel_and_print_columns(filepath: str, sheet_name: str):
    """
    Load an Excel file, print its columns, and close the file.

    Args:
    filepath (str): Path to the Excel file.
    sheet_name (str): Name of the sheet to load.

    Returns:
    pd.DataFrame: Loaded data as pandas DataFrame.
    """

    # File Exist checking
    if not os.path.exists(filepath):
        print("Error: File does not exist")
        return None
    try:
        # Sheet name checking
        with pd.ExcelFile(filepath) as xls:
            if sheet_name not in xls.sheet_names:
                print("Error: Sheet Name is not valid / exist.")
                return None
            dataFrame = pd.read_excel(xls, sheet_name=sheet_name)
            print("Columns in the DataFrame:")
            print(dataFrame.columns)
            return dataFrame
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_selected_columns_to_csv(df: pd.DataFrame, columns: list[str], output_filepath: str) -> None:
    """
       Save selected columns of a DataFrame to a CSV file.

       Args:
       df (pd.DataFrame): DataFrame to select columns from.
       columns (list[str]): List of column names to select.
       output_filepath (str): File path to save the CSV file.
    """
    if df is None:
        print("DataFrame is empty. Cannot proceed with saving to CSV.")
        return
    try:
        # Check if the specified columns exist in the DataFrame before attempting to select them
        if not set(columns).issubset(df.columns):
            print("Specified columns do not exist in the DataFrame.")
            return
        selected_columns = df[columns]

        # Save to CSV
        selected_columns.to_csv(output_filepath, encoding='utf8', index=False, header=columns)
        print(f"Data saved to {output_filepath}")
    except Exception as e:
        print(f"Error: {e}")


# Define the file paths and parameters
# CLI Examples：python preprocess_excel.py "data/files/BIAN v12 asset(SD).xlsx" "Service Domain" "Service Domain, Business Area, Business Domain, functionalPattern, assetType, genericArtefactType, Examples Of Use, Role Definition" "data/files/BIAN v12 asset(SD).csv"

if __name__ == "__main__":
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("src_file_dir", type=str, help="File Path")
    parser.add_argument("sheets", type=str, help="Sheet name")
    parser.add_argument("cols_convert", type=str, help="Columns need to retrieve, separated by comma")
    parser.add_argument("result_file_dir", type=str, help="Result file directory")
    args = parser.parse_args()

    # Obtain the args from CLI.
    src_file_dir = args.src_file_dir
    sheets = args.sheets
    # Convert the comma-separated string to a list and strip whitespace from each element
    cols_to_save = [col.strip() for col in args.cols_convert.split(',')]
    result_file_dir = args.result_file_dir

    # Load the Excel file
    df = load_excel_and_print_columns(src_file_dir, sheets)

    # Save selected columns to CSV
    save_selected_columns_to_csv(df, cols_to_save, result_file_dir)
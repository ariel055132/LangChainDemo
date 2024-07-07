import argparse
import pandas as pd


def load_excel_and_print_columns(filepath, sheet_name):
    """
    Load an Excel file and print its columns.

    Args:
    filepath (str): Path to the Excel file.
    sheet_name (str): Name of the sheet to load.

    Returns:
    pd.DataFrame: Loaded data as pandas DataFrame.
    """
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        print("Columns in the DataFrame:")
        print(df.columns)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_selected_columns_to_csv(df, columns, output_filepath):
    """
       Save selected columns of a DataFrame to a CSV file.

       Args:
       df (pd.DataFrame): DataFrame to select columns from.
       columns (list): List of column names to select.
       output_filepath (str): File path to save the CSV file.
    """
    if df is None:
        print("DataFrame is empty. Cannot proceed with saving to CSV.")
        return
    try:
        # Select the desired columns
        selected_columns = df[columns]

        # Print the selected columns (optional, can be commented out in production)
        print("Selected columns:")
        print(selected_columns)

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
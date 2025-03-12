import pandas as pd
import json
import os
import sys
from datetime import datetime
import re
import argparse
import glob


def extract_date_from_sheet_name(sheet_name, date_format=None):
    """
    Attempts to extract a date from the sheet name using various methods.

    Returns:
        tuple: (date_str, day_str) where date_str is in 'YYYY-MM-DD' format
    """
    # Try specified format first
    if date_format:
        try:
            date_obj = datetime.strptime(sheet_name, date_format)
            return date_obj.strftime('%Y-%m-%d'), date_obj.strftime('%A')
        except ValueError:
            pass

    # Try common date formats
    date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y',
                    '%d-%m-%Y', '%m-%d-%Y', '%b %d %Y', '%b %d, %Y', '%d %b %Y']
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(sheet_name, fmt)
            return date_obj.strftime('%Y-%m-%d'), date_obj.strftime('%A')
        except ValueError:
            continue

    # Try to extract date using regex
    date_pattern = re.compile(r'(\d{1,4}[-/]\d{1,2}[-/]\d{1,4})')
    match = date_pattern.search(sheet_name)
    if match:
        date_candidate = match.group(1)
        # Try parsing the extracted date
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y', '%d-%m-%Y']:
            try:
                date_obj = datetime.strptime(date_candidate, fmt)
                return date_obj.strftime('%Y-%m-%d'), date_obj.strftime('%A')
            except ValueError:
                continue

    # Check for patterns like "Mar 18" or "March 18"
    month_day_pattern = re.compile(r'([A-Za-z]+)\s+(\d{1,2})')
    match = month_day_pattern.search(sheet_name)
    if match:
        month_name = match.group(1)
        day_num = match.group(2)
        current_year = datetime.now().year
        date_str = f"{month_name} {day_num}, {current_year}"
        try:
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            return date_obj.strftime('%Y-%m-%d'), date_obj.strftime('%A')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, "%b %d, %Y")
                return date_obj.strftime('%Y-%m-%d'), date_obj.strftime('%A')
            except ValueError:
                pass

    # Return original sheet name if no date format could be detected
    return sheet_name, "Unknown"


def process_excel_file(file_path, date_format=None, verbose=False):
    """
    Process a single Excel file and extract data from all sheets.
    """
    if verbose:
        print(f"Processing file: {file_path}")

    file_data = []

    try:
        # Read all sheets in the Excel file
        excel_data = pd.read_excel(file_path, sheet_name=None)

        if verbose:
            print(f"  Found {len(excel_data)} sheets")

        # Process each sheet
        for sheet_name, df in excel_data.items():
            if verbose:
                print(f"  Processing sheet: {sheet_name}")

            # Extract date from sheet name
            date_str, day_str = extract_date_from_sheet_name(sheet_name, date_format)

            if verbose:
                print(f"    Extracted date: {date_str}, day: {day_str}")

            # Handle empty dataframes
            if df.empty:
                if verbose:
                    print(f"    Warning: Sheet '{sheet_name}' is empty")
                sessions = []
            else:
                # Ensure all expected columns exist
                expected_columns = [
                    "Title", "Session Code", "Time", "Badges", "Technical Level",
                    "Topic", "Speakers", "Points", "Description",
                    "start_time", "end_time", "Expert Input"
                ]
                # Note: We keep the original case here for column checking,
                # but will convert to lowercase in the final JSON output

                # Add any missing columns with empty values
                for col in expected_columns:
                    if col not in df.columns:
                        df[col] = ""

                # Clean up the data
                # Fill NaN values with empty string to make JSON serializable
                df = df.fillna("")

                # For the GTC sessions data, ensure time data is properly formatted
                if "Time" in df.columns:
                    # Extract start_time and end_time if not already present
                    if "start_time" not in df.columns or df["start_time"].isna().all():
                        df["start_time"] = df["Time"].apply(
                            lambda x: x.split(" - ")[0].strip() if isinstance(x, str) and " - " in x else ""
                        )

                    if "end_time" not in df.columns or df["end_time"].isna().all():
                        df["end_time"] = df["Time"].apply(
                            lambda x: x.split(" - ")[1].strip() if isinstance(x, str) and " - " in x else ""
                        )

                # Convert DataFrame to list of records
                sessions = json.loads(df.to_json(orient='records', date_format='iso'))

                # Ensure all values are JSON serializable (handle any remaining non-standard types)
                for session in sessions:
                    for key, value in session.items():
                        if pd.isna(value) or value is None:
                            session[key] = ""

            # Convert all keys to lowercase for sessions
            lowercase_sessions = []
            for session in sessions:
                lowercase_session = {k.lower(): v for k, v in session.items()}
                lowercase_sessions.append(lowercase_session)

            # Create object for this sheet with lowercase keys
            sheet_data = {
                "date": date_str,
                "day": day_str,
                "sessions": lowercase_sessions
            }

            file_data.append(sheet_data)

        return file_data

    except Exception as e:
        if verbose:
            print(f"  Error processing file {file_path}: {str(e)}")
        return []


def convert_csv_to_json(csv_path, output_file, date, day_of_week, verbose=False):
    """
    Converts a single CSV file to a JSON object with Date, Day, and sessions fields.
    """
    if verbose:
        print(f"Processing CSV file: {csv_path}")

    try:
        # Read the CSV file
        df = pd.read_csv(csv_path)

        if verbose:
            print(f"  Read {len(df)} rows from CSV")

        # Handle empty dataframe
        if df.empty:
            if verbose:
                print(f"  Warning: CSV file '{csv_path}' is empty")
            sessions = []
        else:
            # Ensure all expected columns exist
            expected_columns = [
                "Title", "Session Code", "Time", "Badges", "Technical Level",
                "Topic", "Speakers", "Points", "Description",
                "start_time", "end_time", "Expert Input"
            ]

            # Add any missing columns with empty values
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            # Clean up the data
            # Fill NaN values with empty string to make JSON serializable
            df = df.fillna("")

            # For the GTC sessions data, ensure time data is properly formatted
            if "Time" in df.columns:
                # Extract start_time and end_time if not already present
                if "start_time" not in df.columns or df["start_time"].isna().all():
                    df["start_time"] = df["Time"].apply(
                        lambda x: x.split(" - ")[0].strip() if isinstance(x, str) and " - " in x else ""
                    )

                if "end_time" not in df.columns or df["end_time"].isna().all():
                    df["end_time"] = df["Time"].apply(
                        lambda x: x.split(" - ")[1].strip() if isinstance(x, str) and " - " in x else ""
                    )

            # Convert DataFrame to list of records
            sessions = json.loads(df.to_json(orient='records', date_format='iso'))

            # Ensure all values are JSON serializable (handle any remaining non-standard types)
            for session in sessions:
                for key, value in session.items():
                    if pd.isna(value) or value is None:
                        session[key] = ""

        # Convert all keys to lowercase for sessions
        lowercase_sessions = []
        for session in sessions:
            lowercase_session = {k.lower(): v for k, v in session.items()}
            lowercase_sessions.append(lowercase_session)

        # Create object for this CSV with lowercase keys
        csv_data = [{
            "date": date,
            "day": day_of_week,
            "sessions": lowercase_sessions
        }]

        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(csv_data, f, ensure_ascii=False, indent=4)

        if verbose:
            print(f"Wrote data to {output_file}")

        return csv_data

    except Exception as e:
        if verbose:
            print(f"  Error processing CSV file {csv_path}: {str(e)}")
        return []


def excel_to_json(input_path, output_file, date_format=None, verbose=False):
    """
    Converts Excel files with multiple sheets to a JSON file.
    Each sheet is represented as a JSON object with Date, Day, and sessions fields.
    """
    all_data = []

    # Check if input_path is a directory or a file
    if os.path.isdir(input_path):
        # Find all Excel files in the directory
        excel_files = glob.glob(os.path.join(input_path, "*.xlsx"))
        excel_files.extend(glob.glob(os.path.join(input_path, "*.xls")))

        # Check for CSV files as well
        csv_files = glob.glob(os.path.join(input_path, "*.csv"))

        if verbose:
            print(f"Found {len(excel_files)} Excel files and {len(csv_files)} CSV files in directory")

        for excel_file in excel_files:
            file_data = process_excel_file(excel_file, date_format, verbose)
            all_data.extend(file_data)

        # Process CSV files if any (will need date info from user)
        for csv_file in csv_files:
            # For CSVs, we need to ask for date info or infer from filename
            filename = os.path.basename(csv_file)
            date_str, day_str = extract_date_from_sheet_name(filename, date_format)

            if date_str == filename:
                # Could not extract date from filename, use current date
                today = datetime.now()
                date_str = today.strftime('%Y-%m-%d')
                day_str = today.strftime('%A')

                if verbose:
                    print(f"  Could not extract date from CSV filename, using today: {date_str}")

            csv_data = convert_csv_to_json(csv_file, output_file + ".temp.json", date_str, day_str, verbose)
            all_data.extend(csv_data)

    elif os.path.isfile(input_path):
        if input_path.endswith('.xlsx') or input_path.endswith('.xls'):
            # Process a single Excel file
            file_data = process_excel_file(input_path, date_format, verbose)
            all_data.extend(file_data)
        elif input_path.endswith('.csv'):
            # For CSV, we need date info or infer from filename
            filename = os.path.basename(input_path)
            date_str, day_str = extract_date_from_sheet_name(filename, date_format)

            if date_str == filename:
                # Could not extract date from filename, use current date
                today = datetime.now()
                date_str = today.strftime('%Y-%m-%d')
                day_str = today.strftime('%A')

                if verbose:
                    print(f"  Could not extract date from CSV filename, using today: {date_str}")

            csv_data = convert_csv_to_json(input_path, output_file + ".temp.json", date_str, day_str, verbose)
            all_data.extend(csv_data)
        else:
            if verbose:
                print(f"Error: {input_path} is not a valid Excel or CSV file")
            return []

    else:
        if verbose:
            print(f"Error: {input_path} is not a valid file or directory")
        return []

    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    if verbose:
        print(f"Wrote {len(all_data)} date objects to {output_file}")

    # Remove any temporary files
    temp_file = output_file + ".temp.json"
    if os.path.exists(temp_file):
        os.remove(temp_file)

    return all_data


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert Excel files with multiple sheets to JSON')
    parser.add_argument('input', help='Path to Excel file or directory containing Excel files')
    parser.add_argument('output', help='Path to output JSON file')
    parser.add_argument('--date-format', help='Format of the date in sheet names (e.g., %%Y-%%m-%%d)')
    parser.add_argument('--csv-date', help='Date to use for CSV files (YYYY-MM-DD format)')
    parser.add_argument('--csv-day', help='Day of week to use for CSV files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Convert Excel files to JSON
    result = excel_to_json(args.input, args.output, args.date_format, args.verbose)

    if result:
        print(f"Conversion complete. {len(result)} date objects converted to JSON.")
        return 0
    else:
        print("Conversion failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
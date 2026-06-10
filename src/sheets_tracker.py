import os
import json
import csv
from datetime import datetime
import sys

def log_to_local_csv(test_name, description, winning_variant, actionable_decision, net_roi):
    """
    Appends the test result to a local result_sheet.csv file as a fallback.
    """
    fallback_file = "result_sheet.csv"
    headers = ["Timestamp", "Test Name", "Description", "Winning Variant", "Actionable Decision", "Net ROI"]
    
    file_exists = os.path.exists(fallback_file)
    
    try:
        with open(fallback_file, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(headers)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([
                timestamp,
                test_name,
                description,
                winning_variant,
                actionable_decision,
                f"R$ {net_roi:.2f}"
            ])
        print(f"Successfully exported result row locally to '{fallback_file}'.")
    except Exception as e:
        print(f"Error: Could not write local fallback file: {str(e)}", file=sys.stderr)

def record_test_result(test_name, description, winning_variant, actionable_decision, net_roi, sheet_id_override=None):
    """
    Attempts to append a row to a centralized Google Sheet using credentials from the environment.
    Falls back gracefully to a local CSV file if Sheets authentication or writing fails.
    """
    sheet_id = sheet_id_override or os.getenv("GOOGLE_SHEET_ID")
    creds_json_str = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
    
    # Check if sheets config is missing upfront to avoid importing dependencies unnecessarily
    if not sheet_id or not creds_json_str:
        print("Warning: Google Sheets credentials or Sheet ID not found. Falling back to local CSV export.", file=sys.stderr)
        log_to_local_csv(test_name, description, winning_variant, actionable_decision, net_roi)
        return
        
    try:
        # Import gspread and auth packages inside the function
        import gspread
        from google.oauth2.service_account import Credentials
        
        # Parse credentials dictionary
        creds_dict = json.loads(creds_json_str)
        
        # Define scopes
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Authenticate
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        
        # Open spreadsheet
        sheet = client.open_by_key(sheet_id)
        
        # Select first worksheet
        worksheet = sheet.get_worksheet(0)
        
        # If worksheet is empty, we can write a header row
        # (This checks if sheet has cells, otherwise adds header)
        existing_values = worksheet.get_all_values()
        if not existing_values:
            worksheet.append_row([
                "Timestamp", 
                "Test Name", 
                "Description", 
                "Winning Variant", 
                "Actionable Decision", 
                "Net ROI"
            ])
            
        # Append data row
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([
            timestamp,
            test_name,
            description,
            winning_variant,
            actionable_decision,
            f"R$ {net_roi:.2f}"
        ])
        print(f"Successfully recorded result row in Google Sheet (Sheet ID: {sheet_id}).")
        
    except Exception as e:
        print(f"Warning: Google Sheets credentials not found or invalid. Falling back to local CSV export.", file=sys.stderr)
        print(f"Detail: Sheets error: {str(e)}", file=sys.stderr)
        log_to_local_csv(test_name, description, winning_variant, actionable_decision, net_roi)

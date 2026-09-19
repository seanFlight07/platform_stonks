import pandas as pd
from database.connection import engine
from sqlalchemy import MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert
from pathlib import Path
from utils import db
#veridication helpers
def get_required_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a valid value")


def get_yes_no_input(prompt):
    while True:
        value = input(prompt).strip().upper()
        if value in ["Y", "N"]:
            return value == "Y"
        print("Please enter Y or N.")

def does_file_exist(prompt):
    while True:
        value = input(prompt).strip()
        abs_path = Path("./worker/data") / value
        if abs_path.is_file():
            return abs_path.resolve()
        print(f"File {value} does not exist\nPlease enter again: ")

def get_company_details():
    company_details = {}
    
    name_of_file = does_file_exist("Input name of the file:") 
    company_details["code"] = get_required_input("Enter code of company: ").upper()
    company_details["name"] = get_required_input("Enter name of company: ")
    company_details["exchange"] = get_required_input("Listed exchange of company: ").upper()
    company_details["active"] = get_yes_no_input("Set this as active retrival? [Y/N]")

    return company_details, name_of_file


def load_csv(file_path):
    csv_file_raw = pd.read_csv(file_path)
    csv_file_raw['date'] = pd.to_datetime(csv_file_raw['Date'], format='%d/%m/%Y')
    csv_file_raw = csv_file_raw.drop(columns=['Date'])
    return csv_file_raw

#might be a good one to move so can change the columns from api fetching
def transform_data(data, code):
    csv_file_name_change = data.rename(columns={
        "Open $": "open",
        "High $": "high",
        "Low $": "low",
        "Close $": "close",
        "Change $": "change_dollar",
        "Change %": "change_pct",
        "Volume": "volume"
    })
    csv_file_name_change['code'] = code
    csv_file_name_change = csv_file_name_change.replace(r"^\s*$", pd.NA, regex=True)
    return csv_file_name_change

def validation(data):
    errors = []
    columns_needed = ["open",
                    "high",
                    "low",
                    "close",
                    "change_dollar",
                    "change_pct",
                    "volume",
                    "date",
                    "code"]
    extra_columns = [
    column
    for column in data.columns
    if column not in columns_needed
    ]
    if extra_columns:
        errors.append(
            f"Unexpected columns: {extra_columns}"
        )
    #checks if all columns are needed
    for column in columns_needed:
        if column not in data.columns:
            errors.append(f"Missing required column: {column}")

    columns_with_no_missing = data.notna().all()
    #checks if no missing data is in the columns
    for col_name, is_clean in columns_with_no_missing.items():
        if not is_clean:
            errors.append(f"Column '{col_name}' has missing data.")

    if errors:
        return False, errors

    return True, errors


def main():
    company_details, file_path = get_company_details()
    raw_file = load_csv(file_path)
    clean_file = transform_data(raw_file, company_details["code"])
    is_valid, errors = validation(clean_file)
    company_exists = db.company_exists(company_details["code"])

    if is_valid:
        if not company_exists:
            db.insert_company(company_details)

        db.insert_data(clean_file)

        print(
            f"Company {company_details['code']} and data from "
            f"{file_path} have successfully been uploaded"
        )
    else:
        print("Failed upload")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    main()

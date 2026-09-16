#refactor code
#create functions for each process and a main component
#clean up validation
#handle duplication of inserts into the database
#handle user input for items

import pandas as pd
from database.connection import engine
from sqlalchemy import text


def get_company_details():
    NAME_OF_FILE = input("Input name of the file:")
    FILE_PATH = "./worker/data/" + NAME_OF_FILE
    
    company_details = {}
    #get information of the company
    company_details["code"] = input("Enter code of company: ")
    company_details["name_of_company"] = input("Enter name of company: ")
    company_details["exchange"] = input("Listed exchange of company: ")
    company_details["active"] = input("Set this as active retrival? [Y/N]").upper() == "Y"
    
    return company_details, FILE_PATH


def load_csv(file_path):
    csv_file_raw = pd.read_csv(file_path)
    csv_file_raw['date'] = pd.to_datetime(csv_file_raw['Date'], format='%d/%m/%Y')
    csv_file_raw = csv_file_raw.drop(columns=['Date'])
    return csv_file_raw


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
    
    for column in columns_needed:
        if column not in data.columns:
            errors.append(f"Missing required column: {column}")

    columns_with_no_missing = data.notna().all()

    for col_name, is_clean in columns_with_no_missing.items():
        if not is_clean:
            errors.append(f"Column '{col_name}' has missing data.")

    if errors:
        return False, errors

    return True, errors

def upload_data(data, company):
    with engine.begin() as connection:
        query = text("""
            INSERT INTO company(code, name, exchange, active)
            VALUES (:code, :name, :exchange, :active)
            """)

        connection.execute( query,{
            "code": company["code"],
            "name": company["name_of_company"],
            "exchange": company["exchange"],
            "active": company["active"]
        })

        data.head(5).to_sql(name="price", con=connection,if_exists="append", index=False)


def main():
    company_details, file_path = get_company_details()
    raw_file = load_csv(file_path)
    clean_file = transform_data(raw_file, company_details["code"])
    is_valid, errors = validation(clean_file)

    if is_valid:
        upload_data(clean_file, company_details)
    else:
        print("Failed upload")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    main()

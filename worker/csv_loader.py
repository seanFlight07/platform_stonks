#Add the code name to the table
#change the name of the Change $ and Change %
#Verify no missing data in the data frame
#function the two parts company data and processing the dataframe
#push data to the database
#change date to comply with db spec


import pandas as pd

NAME_OF_FILE = input("Input name of the file:")
FILE_PATH = "./data/" + NAME_OF_FILE

#get information of the company
code = input("Enter code of company: ")
name_of_company = input("Enter name of company: ")
exchange = input("Listed exchange of company: ")
active = input("Set this as active retrival? [Y/N]")

#Getting the data from file and convert date field, change field names, add regex for NaN checking
csv_file_raw = pd.read_csv(FILE_PATH)
csv_file_raw['date'] = pd.to_datetime(csv_file_raw['Date'], format='%d/%m/%Y')
csv_file_raw = csv_file_raw.drop(columns=['Date'])
csv_file_name_change = csv_file_raw.rename(columns={
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

print(csv_file_name_change)

#check if the csv has the columns I want
columns_need = ["open","high","low","close","change_dollar","change_pct","volume","date","code"]

has_required_columns = all(
    column in csv_file_name_change.columns
    for column in columns_need
)


#Check if there is no missing data before upload
columns_with_no_missing = csv_file_name_change.notna().all()
is_data_valid = columns_with_no_missing.all()

if is_data_valid and has_required_columns:
    print("ready for upload")
    #DB connection for upload
else:
    print("Upload failed. Missing data")

# Loop through each column name and its boolean status
    for col_name, is_clean in columns_with_no_missing.items():
        if not is_clean:  # Triggers only if the value is False
            print(f"Column '{col_name}' has missing data.")




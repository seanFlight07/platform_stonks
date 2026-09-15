#Add the code name to the table
#change the name of the Change $ and Change %
#Verify no missing data in the data frame
#function the two parts company data and processing the dataframe
#push data to the database



import pandas as pd

NAME_OF_FILE = input("Input name of the file:")
FILE_PATH = "./data/" + NAME_OF_FILE

#get information of the company
code = input("Enter code of company: ")
name_of_company = input("Enter name of company: ")
exchange = input("Listed exchange of company: ")
active = input("Set this as active retrival? [Y/N]")



#Getting the data from file
csv_file_raw = pd.read_csv(FILE_PATH)
csv_file_name_change = csv_file_raw.rename(columns={"Change $": "change_dollar","Change %": "change_pct"})

print(csv_file_name_change)


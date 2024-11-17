from faker import Faker
import random
import pandas as pd
import uuid
from datetime import datetime
import DynamicMapping as dynamicmapping

# Initialize the Faker instance
fake = Faker()
'''

# Generate personal info data
personal_info_model = [
    {"name": "Name", "type": "name"},
    {"name": "Gender", "type": "gender"},
    {"name": "Email", "type": "email"},
    {"name": "Phone", "type": "phone"},
    {"name": "Company", "type": "company"},
    {"name": "Job Title", "type": "job"},
    {"name": "Date of Birth", "type": "date_of_birth"},
    {"name": "Is Active", "type": "boolean"},  # Boolean field
    {"name": "Salary", "type": "number", "min": 30000, "max": 150000},
    {"name": "Country", "type": "choice", "choices": ["USA", "Canada", "Germany", "UK", "India"]},
    {"name": "Credit Card", "type": "credit_card"},
    {"name": "Notes", "type": "text"},
    {"name": "Join Date", "type": "datetime"},
    {"name": "User UUID", "type": "uuid"},
    {"name": "IP Address", "type": "ip_address"},
    {"name": "File Path", "type": "file_path"},
    {"name": "Profile Image", "type": "image_url"},
    {"name": "Website", "type": "url"},
    {"name": "ID", "type": "id"},
    {"name": "Passport", "type": "passport"},
    {"name": "SSN", "type": "ssn"},
    {"name": "Driving License", "type": "driving_license"},
    {"name": "Address", "type": "address", "address_format": "split"}
]

# Generate accounts data
accounts_data_model = [
    {"name": "Account ID", "type": "uuid"},
    {"name": "User ID", "type": "uuid"},  # Link this to a person
    {"name": "Account Type", "type": "choice", "choices": ["savings", "checking", "business"]},
    {"name": "Balance", "type": "number", "min": 1000, "max": 50000},
    {"name": "Creation Date", "type": "datetime"},
    {"name": "Is Verified", "type": "boolean"}  # New Boolean field

]

'''
# Step 1: Generate the personal data (100 records)
num_records = 100


def returnAPIResponse(accounts_data_model):
    # Step 2: Generate accounts data and link each record to a user (using user_id from personal data)
    print ('Generating Data set')
    personal_data = dynamicmapping.generate_data_from_model(personal_info_model, num_records)
    accounts_data = dynamicmapping.generate_data_from_model(accounts_data_model, num_records, parent_data=personal_data)
    print ('onvert the lists of dictionaries to pandas DataFrames')
    # Convert the lists of dictionaries to pandas DataFrames
    personal_info_df = pd.DataFrame(personal_data)
    accounts_df = pd.DataFrame(accounts_data)

    # Merge data on user_id (simulating the relationship between person and account)
    merged_df = pd.merge(accounts_df, personal_info_df, left_on="User ID", right_on="User UUID", how="left")

    '''
    # Print the first few rows of merged data
    print(merged_df.head())
    '''
    print ('Optionally, save to CSV files')
    # Optionally, save to CSV files
    personal_info_df.to_csv('personal_info_data.csv', index=False)
    accounts_df.to_csv('accounts_data.csv', index=False)
    merged_df.to_csv('merged_data.csv', index=False)
    return 'Success'

'''
resp= returnAPIResponse(accounts_data_model)
print(resp)
'''
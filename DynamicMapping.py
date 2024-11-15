import pandas as pd
from faker import Faker
import random
import re

# Initialize Faker instance
fake = Faker()

# Function to map column names to Faker methods based on patterns
def intelligent_map_column_to_faker(column_name):
    """
    This function attempts to intelligently map a given column name
    to an appropriate Faker method based on heuristics or decision rules.
    """
    # Convert column name to lowercase for easier matching
    column_name = column_name.lower()

    # Decision table: Heuristic rules for common column names
    if re.search(r'name', column_name):
        # If the column name contains "name", assume it is a party name (person or organization)
        return lambda: fake.name()  # You can modify this to fake.company() if organization
    elif re.search(r'email', column_name):
        return lambda: fake.email()  # Email
    elif re.search(r'phone', column_name):
        return lambda: fake.phone_number()  # Phone number
    elif re.search(r'address', column_name):
        return lambda: fake.address()  # Address
    elif re.search(r'city', column_name):
        return lambda: fake.city()  # City
    elif re.search(r'state', column_name):
        return lambda: fake.state()  # State
    elif re.search(r'postal', column_name) or re.search(r'zipcode', column_name):
        return lambda: fake.zipcode()  # Postal code or Zip code
    elif re.search(r'country', column_name):
        return lambda: fake.country()  # Country
    elif re.search(r'birth', column_name) or re.search(r'date_of_birth', column_name):
        return lambda: fake.date_of_birth(minimum_age=18, maximum_age=80)  # Date of birth
    elif re.search(r'gender', column_name):
        return lambda: random.choice(['Male', 'Female', 'Other'])  # Gender
    elif re.search(r'party', column_name):
        return lambda: random.choice(['Individual', 'Organization', 'Group'])  # Party type
    elif re.search(r'status', column_name):
        return lambda: random.choice(['Active', 'Inactive', 'Pending'])  # Party status
    elif re.search(r'profile_picture', column_name):
        return lambda: fake.image_url()  # Profile picture URL
    else:
        # Default handler if no match is found, you can modify it to handle other cases
        return lambda: None  # Or some other generic value or default method

# Function to generate fake data from CSV dynamically
def generate_fake_data_from_csv(csv_file):
    # Read the CSV to get the column names
    df = pd.read_csv(csv_file)
    
    # Generate fake data for each row and column in the CSV
    generated_data = []
    
 #   for index, row in df.iterrows():
    for i in range(0, 100):
        row_data = {}
        for column in df.columns:
            # Map the column name to a Faker method and generate the fake data
            faker_method = intelligent_map_column_to_faker(column)
            row_data[column] = faker_method()
        
        # Append the generated data to the list
        generated_data.append(row_data)
    
    # Convert the list of dictionaries to a DataFrame
    fake_df = pd.DataFrame(generated_data)
    
    # Optionally, save the generated fake data to a new CSV
    fake_df.to_csv('generated_fake_data.csv', index=False)
    
    return fake_df

# Example usage
#csvdf = pd.read_csv('SampleData/credit_score_cleaned_train.csv')
fake_data = generate_fake_data_from_csv('SampleData/credit_score_cleaned_train.csv')  # Replace with your actual CSV path
print(fake_data)

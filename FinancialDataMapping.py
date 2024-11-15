from faker import Faker
import random
import re
import pandas as pd

# Initialize Faker object
fake = Faker()

# Custom mappings for Party Identification, KYC, etc.
def generate_party_identification():
    return {
        'document_type': random.choice(['Passport', 'National ID', 'Driver\'s License']),
        'document_number': fake.unique.bothify(text='????####???'),
        'issued_country': fake.country(),
        'expiration_date': fake.date_this_decade(),
        'issue_date': fake.date_this_century(),
        'verification_status': random.choice(['Verified', 'Pending', 'Failed']),
        'verified_by': fake.company(),
        'verification_date': fake.date_this_year(),
    }

def generate_kyc_info():
    return {
        'kyc_status': random.choice(['Completed', 'In Progress', 'Rejected']),
        'kyc_level': random.choice(['Basic', 'Enhanced', 'Simplified']),
        'kyc_type': random.choice(['Individual', 'Corporate', 'PEP']),
        'risk_category': random.choice(['Low', 'Medium', 'High']),
        'document_verification_status': random.choice(['Verified', 'Pending', 'Failed']),
        'aml_check_status': random.choice(['Clear', 'Suspicious']),
        'sanctions_check_status': random.choice(['Clear', 'Watchlist']),
        'source_of_funds': random.choice(['Salary', 'Business', 'Inheritance']),
        'politically_exposed_person': random.choice([True, False]),
        'pep_description': fake.text(max_nb_chars=100) if random.choice([True, False]) else None
    }

# Pattern matching for columns
def intelligent_mapping(column_name):
    column_name = column_name.lower()

    # Mapping dictionary using regex patterns
    pattern_mapping = [
        # Name-related patterns
        (r'first_name|last_name|name', lambda: fake.name()),
        (r'fullname|full_name', lambda: fake.name()),
        (r'middle_name', lambda: fake.first_name()),
        
        # Address-related patterns
        (r'address', lambda: fake.address()),
        (r'city', lambda: fake.city()),
        (r'state', lambda: fake.state()),
        (r'country', lambda: fake.country()),
        (r'zipcode|postal_code|zip', lambda: fake.zipcode()),
        (r'street', lambda: fake.street_address()),
        
        # Date-related patterns
        (r'dob|birth_date|birthdate', lambda: fake.date_of_birth(minimum_age=18, maximum_age=80)),
        (r'expiration_date|expiry_date', lambda: fake.date_this_decade()),
        (r'issue_date|issued_date', lambda: fake.date_this_century()),
        (r'last_transaction_date', lambda: fake.date_this_year()),
        
        # Contact-related patterns
        (r'phone|telephone|mobile', lambda: fake.phone_number()),
        (r'email', lambda: fake.email()),
        
        # Status and Category-related patterns
        (r'status', lambda: random.choice(['Active', 'Inactive', 'Pending', 'Closed'])),
        (r'kyc_status', lambda: random.choice(['Completed', 'In Progress', 'Rejected'])),
        (r'risk_category|risk_level', lambda: random.choice(['Low', 'Medium', 'High'])),
        
        # Financial patterns
        (r'amount|balance|price|value|cost', lambda: round(random.uniform(1000.0, 50000.0), 2)),
        (r'currency', lambda: random.choice(['USD', 'EUR', 'GBP', 'JPY'])),
        (r'account_number', lambda: fake.unique.bothify(text='####-#####-###')),
        (r'card_number', lambda: fake.credit_card_number(card_type='mastercard')),
        (r'transaction_id', lambda: fake.unique.uuid4()),
        (r'loan_amount|mortgage_amount', lambda: round(random.uniform(5000.0, 200000.0), 2)),
        
        # Generic patterns
        (r'id|uuid|identifier', lambda: fake.uuid4()),
        (r'comment|description|note', lambda: fake.text(max_nb_chars=200)),
        (r'created_date|created_at|timestamp', lambda: fake.date_this_decade()),
        
        # Boolean or status flags
        (r'active|enabled|is_active', lambda: random.choice([True, False])),
        (r'completed|approved|verified', lambda: random.choice([True, False])),
        
        # Other catch-all generic fallback
        (r'.*', lambda: fake.word())
    ]

    # Iterate through patterns and match the column name
    for pattern, func in pattern_mapping:
        if re.search(pattern, column_name):
            return func()
    
    # If no match, fallback to generic word or text generation
    return fake.word()

def generate_fake_data(columns):
    # Generate a dictionary for each row
    data = {}
    for column in columns:
        data[column] = intelligent_mapping(column)
    return data

# Example usage
columns = [
    'party_id', 'first_name', 'last_name', 'dob', 'email', 'phone_number', 'document_type', 'kyc_status', 
    'risk_category', 'account_type', 'balance', 'transaction_type', 'account_status', 'loan_amount', 
    'card_type', 'asset_value', 'liability_type'
]

generated_data = []

for i in range(0, 100):
     generated_data.append(generate_fake_data(columns))
     

fake_df = pd.DataFrame(generated_data)

print(fake_df)

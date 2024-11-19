import json
import uuid
import random
import csv
from datetime import datetime
from faker import Faker

fake = Faker()

def generate_fake_data_for_field(field, existing_data=None, dynamic_links=None, all_data=None):
    """Generate fake data based on the field type, with links to existing data if needed."""
    field_name = field["name"]
    field_type = field["type"]

    if field_type == "name":
        return fake.name()
    elif field_type == "gender":
        return random.choice(["Male", "Female", "Other"])
    elif field_type == "ssn":
        return fake.ssn()
    elif field_type == "driving_license":
        return fake.license_plate()
    elif field_type == "address":
        return fake.address().replace("\n", ", ")  # Format address as a single line
    elif field_type == "uuid":
        return str(uuid.uuid4())
    elif field_type == "choice":
        return random.choice(field["choices"])
    elif field_type == "number":
        return random.randint(field["min"], field["max"])
    elif field_type == "datetime":
        return fake.date_time_this_decade().isoformat()
    elif field_type == "boolean":
        return random.choice([True, False])
    elif isinstance(field_type, dict) and "dynamic_link" in field_type:
        # Handle dynamic linking between models
        link_config = field_type["dynamic_link"]
        target_model_name = link_config["model"]
        target_field = link_config["field"]
        
        # Get data from the linked model
        if target_model_name in all_data:
            linked_model_data = [item[target_field] for item in all_data[target_model_name]]
            return random.choice(linked_model_data)
        return None
    elif field_type == "link" and existing_data is not None:
        # For linked fields like 'User ID' and 'Account ID', use existing data.
        return random.choice(existing_data)
    else:
        return None

def generate_fake_data_for_model(model, existing_data=None, dynamic_links=None, all_data=None):
    """Generate fake data for a given model schema."""
    return {field["name"]: generate_fake_data_for_field(field, existing_data, dynamic_links, all_data) for field in model}

def generate_dynamic_data(model_schemas):
    """
    Generate fake data dynamically for all given model schemas, with links between models.
    
    :param model_schemas: A dictionary of model names with their respective field definitions.
    :return: A dictionary with fake data for each model.
    """
    fake_data = {}
    
    # First generate personal_info_model (users) data
    fake_data['personal_info_model'] = [generate_fake_data_for_model(model_schemas['personal_info_model']) for _ in range(10)]
    
    # Extract user IDs from the generated personal_info_model
    user_ids = [user['User ID'] for user in fake_data['personal_info_model']]
    
    # Now generate accounts_data_model with linked User IDs
    fake_data['accounts_data_model'] = []
    for _ in range(10):
        account_data = generate_fake_data_for_model(model_schemas['accounts_data_model'], user_ids, dynamic_links=None, all_data=fake_data)
        fake_data['accounts_data_model'].append(account_data)
    
    # Extract account IDs and Account Types from the generated accounts_data_model
    account_ids = [account['Account ID'] for account in fake_data['accounts_data_model']]
    account_types = [account['Account Type'] for account in fake_data['accounts_data_model']]
    
    # Now generate transaction_data_model with linked Account IDs and dynamic links
    fake_data['Transaction_data_model'] = []
    for _ in range(20):  # generate 20 transactions
        transaction_data = generate_fake_data_for_model(model_schemas['Transaction_data_model'], account_ids, dynamic_links=None, all_data=fake_data)
        fake_data['Transaction_data_model'].append(transaction_data)
    
    return fake_data

def save_model_to_csv(model_name, model_data, fieldnames):
    """Save the generated model data to a CSV file."""
    filename = f"{model_name}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in model_data:
            writer.writerow(row)

# Example schema provided dynamically
dynamic_schema = {
    "personal_info_model": [
        {"name": "User ID", "type": "uuid"},
        {"name": "Name", "type": "name"},
        {"name": "Gender", "type": "gender"},
        {"name": "SSN", "type": "ssn"},
        {"name": "Driving License", "type": "driving_license"},
        {"name": "Address", "type": "address", "address_format": "split"}
    ],
    "accounts_data_model": [
        {"name": "Account ID", "type": "uuid"},
        {"name": "User ID", "type": "link"},  # Link to personal_info_model
        {"name": "Account Type", "type": "choice", "choices": ["savings", "checking", "business"]},
        {"name": "Balance", "type": "number", "min": 1000, "max": 50000},
        {"name": "Creation Date", "type": "datetime"},
        {"name": "Is Verified", "type": "boolean"}
    ],
    "Transaction_data_model": [
        {"name": "Transaction ID", "type": "uuid"},
        {"name": "User ID", "type": "link"},  # Link to personal_info_model
        {"name": "Account ID", "type": "link"},  # Link to accounts_data_model
        {"name": "Transaction Type", "type": {"dynamic_link": {"model": "accounts_data_model", "field": "Account Type"}}}  # Dynamically link to Account Type
    ]
}

# Generate fake data dynamically with links between models
fake_data = generate_dynamic_data(dynamic_schema)

# Save each model as a CSV file
for model_name, model_data in fake_data.items():
    # Prepare the fieldnames (headers) for CSV
    fieldnames = list(model_data[0].keys())
    
    # Save model data to CSV
    save_model_to_csv(model_name, model_data, fieldnames)

    print(f"Data for {model_name} has been saved to {model_name}.csv")

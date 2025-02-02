from collections import defaultdict
from copy import deepcopy
from faker import Faker
import random
import pandas as pd
import uuid
from datetime import datetime
import DynamicMapping as dynamicmapping
from MetaDataRef import FIELD_METADATA
import csv

# Initialize the Faker instance
fake = Faker()

model ={
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
        {"name": "Transaction Type", "type": "dynamic_link","dynamic_link": {"model": "accounts_data_model", "field": "Account Type"}}  # Dynamically link to Account Type
    ]
}


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
    {"name": "User ID", "type": "uuid"},
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


# Step 1: Generate the personal data (100 records)
num_records = 100000
def map_field_to_type(field_name, metadata_mapping):
    """
    Map a given field name to a type based on the metadata mapping.
    :param field_name: Input field name to map.
    :param metadata_mapping: Dictionary of metadata mappings.
    :return: The mapped type or 'string' if no match is found.
    """
    field_name_lower = field_name.lower()
    for field_type, aliases in metadata_mapping.items():
        if field_name_lower in aliases or field_name_lower == field_type:
            return field_type
    return "string"  # Default type if no match found


def create_field_mapping(user_fields, metadata_mapping):
    """
    Create a list of dictionaries with 'name' and 'type' for each user-provided field.
    :param user_fields: List of field names provided by the user.
    :param metadata_mapping: Metadata mapping for field types.
    :return: List of dictionaries with 'name' and 'type'.
    """
    field_mappings = []
    for field in user_fields:
        inferred_type = map_field_to_type(field, metadata_mapping)
        field_mappings.append({"name": field, "type": inferred_type})
    return field_mappings


def create_multiple_field_mappings(user_models, metadata_mapping):
    """
    Create mappings for multiple data models.
    :param user_models: List of user-provided data models, each containing field names.
    :param metadata_mapping: Metadata mapping for field types.
    :return: List of data models with 'name' and 'type' mappings.
    """
    all_mappings = []
    
    for model_index, user_fields in enumerate(user_models):
        print(f"Processing Model {model_index + 1}...")
        model_mapping = []
        for field in user_fields:
            inferred_type = map_field_to_type(field, metadata_mapping)
            model_mapping.append({"name": field, "type": inferred_type})
        all_mappings.append(model_mapping)
    
    return all_mappings




user_input_fields = ["First Name", "email id", "Contact Number", "Birthdate", "Home Address", "Country", "payment_amount","salary", "SSN","passport", "countrycode"]


#field_mapping = create_field_mapping(user_input_fields,FIELD_METADATA)
#field_mapping = create_multiple_field_mappings(user_input_models,FIELD_METADATA)
#converttoDF=pd.DataFrame(dynamicmapping.generate_data_from_model(field_mapping,num_records))
#converttoDF.to_csv('testdata.csv',index=False)
#print(dynamicmapping.generate_data_from_model(field_mapping,num_records))
# Function to generate a batch of records
def generate_batch(num_records, data_model):
    return [dynamicmapping.generate_data_from_model(data_model,num_records)]

# Function to generate large dataset and store each model in a separate CSV
def generate_and_save_data(user_input_model, num_records, batch_size=10000):
    for model_name, data_model in user_input_model.items():
        print(f"Generating data for {model_name}...")
        print(f"Generating data for {data_model}...")
        # Initialize the file path for each model
        file_name = f"{model_name}_data.csv"
        
        # Initialize a list to store all records for the current model
        all_records = []
        field_mapping = create_field_mapping(data_model,FIELD_METADATA)
        print(f"Generating data for {field_mapping}...")
        num_batches = num_records // batch_size
        for batch in range(num_batches):
            print(f"Generating batch {batch + 1}/{num_batches} for {model_name}")
            batch_data = generate_batch(batch_size, field_mapping)
           # print(batch_data)
            all_records.extend(batch_data)
            
            # Save batch data to CSV file for the current model
            if batch % 10 == 0:
                df = pd.DataFrame(batch_data)
                df.to_csv(file_name, index=False, mode='a', header=(batch == 0))  # Write header for the first batch
        
        print(f"Data generation complete for {model_name}! Total records: {num_records}")
        print(f"Data for {model_name} saved to {file_name}")

#generate_and_save_data(user_input_models, num_records)


def infer_field_type(field_name, meta_data_mapping):
    """
    Dynamically infer the type of a field based on user-provided meta_data_mapping.
    """
    for field_type, field_aliases in meta_data_mapping.items():
        if field_name.lower() in map(str.lower, field_aliases):
            return field_type
    return "unknown"

def generate_dynamic_data_reference(user_input_models, meta_data_mapping, relationship_mapping, num_rows_per_model=100, output_dir="outputdir"):
    """
    Dynamically generate data for multiple user input models with relationships.
    """
    all_data = {}  # Store generated data for all models
    
    # Iterate over each model provided by the user
    for model_name, fields in user_input_models.items():
        data = []
        dependencies = relationship_mapping.get(model_name, {})  # Get relationships if defined

        for _ in range(num_rows_per_model):
            record = {}
            
            for field in fields:
                field_type = infer_field_type(field, meta_data_mapping)
                print (field_type)
                if field in dependencies:  # Check if the field is a reference field
                    parent_model = dependencies[field]["parent_model"]
                    parent_field = dependencies[field]["reference"]
                    parent_data = all_data[parent_model]
                    parent_record = random.choice(parent_data)  # Randomly select a record from the parent model
                    record[field] = parent_record[parent_field]
                else:
                    record[field] = dynamicmapping.generate_field_value(field, field_type)
            
            data.append(record)
        
        # Save data for this model
        all_data[model_name] = data
        converttoDF=pd.DataFrame(data)
        converttoDF.to_csv(model_name+'.csv',index=False)
        #write_to_csv(f"{output_dir}/{model_name}.csv", fields, data)
    
    return all_data


def generate_dynamic_data(model_schemas):
    """
    Generate fake data dynamically for all given model schemas.
    
    :param model_schemas: A dictionary of model names with their respective field definitions.
    :return: A dictionary with fake data for each model.
    """
    allDataModel = {}
    for model_name, schema in model_schemas.items():
        print (model_name)
        field_mapping = create_field_mapping(schema,FIELD_METADATA)
       # fakeDataGenerator=dynamiclink_check(schema,currentDataModel,allDataModel)
        #allDataModel[model_name] = fakeDataGenerator #dynamicmapping.generate_data_from_model(schema,num_records)
        converttoDF=pd.DataFrame(dynamicmapping.generate_data_from_model(field_mapping,num_records))
        converttoDF.to_csv(model_name+'.csv',index=False)
    
    return allDataModel

#print(generate_dynamic_data(user_input_models))
def write_to_csv(file_path, headers, data):
    """
    Write the generated data to a CSV file.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

# Example User Input Models
user_input_models = {
    "personal_info_model": ["User ID", "Name", "Gender", "SSN", "Address"],
    "accounts_data_model": ["Account ID", "User ID", "Account Type", "Balance", "Creation Date", "Is Verified"],
    "Transaction_data_model": ["Transaction ID", "User ID", "Account ID", "Transaction Type"]
}

# Example Relationship Mapping
relationship_mapping = {
    "accounts_data_model": {"User ID": {"reference": "User ID", "parent_model": "personal_info_model"}},
    "Transaction_data_model": {
        "User ID": {"reference": "User ID", "parent_model": "personal_info_model"},
        "Account ID": {"reference": "Account ID", "parent_model": "accounts_data_model"}
    }
}

# Generate and save data
output_data = generate_dynamic_data_reference(user_input_models, FIELD_METADATA, relationship_mapping, num_rows_per_model=100)

'''
def generate_dynamic_data(model_schemas):
    """
    Generate fake data dynamically for all given model schemas.
    
    :param model_schemas: A dictionary of model names with their respective field definitions.
    :return: A dictionary with fake data for each model.
    """
    allDataModel = {}
    for model_name, schema in model_schemas.items():
        print (model_name)
        currentDataModel=dynamicmapping.generate_data_from_model(schema,num_records)
        fakeDataGenerator=dynamiclink_check(schema,currentDataModel,allDataModel)
        allDataModel[model_name] = fakeDataGenerator #dynamicmapping.generate_data_from_model(schema,num_records)
        converttoDF=pd.DataFrame(fakeDataGenerator)
        converttoDF.to_csv(model_name+'.csv',index=False)
    
    return allDataModel

def dynamiclink_check(schema,currentDataModel,allDataModel):
    for field in schema:
        field_name = field["name"]
        field_type = field["type"]
        if(field_type == "dynamic_link"):
           link_config=field["dynamic_link"]
           target_model_name = link_config["model"]
           target_field = link_config["field"]
           if target_model_name in allDataModel:
            # Ensure the model data is a list (i.e., multiple records in a model)
                linked_model_data =  [item[target_field] for item in allDataModel[target_model_name] if isinstance(item, dict) and target_field in item]
                if linked_model_data:
                         for item in currentDataModel:
                             item[field_name]=random.choice(linked_model_data)
                         print(random.choice(linked_model_data))
                else:
                    print(f"Warning: Target model '{target_model_name}' does not contain any data for field '{target_field}'.")
                 
    return currentDataModel
               
# Delta function to simulate changes
def generate_delta(baseline_data, schema, num_inserts=0, num_updates=0, num_deletes=0):
    """
    Generate delta changes: inserts, updates, and deletes.
    
    :param baseline_data: The existing data to modify.
    :param schema: Schema for generating new records.
    :param num_inserts: Number of new records to add.
    :param num_updates: Number of existing records to update.
    :param num_deletes: Number of records to delete.
    :return: A tuple (new_data, deltas), where:
             - new_data is the updated dataset after applying deltas.
             - deltas is a list of changes made.
    """
    new_data = deepcopy(baseline_data)
    deltas = {"inserts": [], "updates": [], "deletes": []}
    generate_dynamic_data(schema)
    # Handle Inserts
    for _ in range(num_inserts):
        new_record = {field["name"]: generate_data_from_field(field) for field in schema}
        new_data.append(new_record)
        deltas["inserts"].append(new_record)

    # Handle Updates
    for _ in range(num_updates):
        if new_data:
            record_to_update = random.choice(new_data)
            updated_record = deepcopy(record_to_update)
            for field in schema:
                if field["type"] not in ["uuid", "link"]:  # Avoid updating primary or foreign keys
                    updated_record[field["name"]] = generate_data_from_field(field)
            deltas["updates"].append({"before": record_to_update, "after": updated_record})
            new_data[new_data.index(record_to_update)] = updated_record

    # Handle Deletes
    for _ in range(num_deletes):
        if new_data:
            record_to_delete = random.choice(new_data)
            deltas["deletes"].append(record_to_delete)
            new_data.remove(record_to_delete)

    return new_data, deltas
#print(generate_dynamic_data(model))

def generateDelta():
  
  return 

def returnAPIResponse(accounts_data_model):
    print('calling Return API response')
    print(generate_dynamic_data(accounts_data_model))
    return 'Success'


resp= returnAPIResponse(accounts_data_model)
print(resp)



'''

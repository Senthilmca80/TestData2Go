import random
import uuid
from faker import Faker
import faker
import pandas
import DynamicMapping
from multiprocessing import Pool

def parse_user_input(user_input):
    data_models = user_input.get("data_models", {})
    constraints = user_input.get("constraints", [])
    return data_models, constraints



def generate_data_for_model(model_name, model_fields, num_records, relationships=None):
    data = []
    for _ in range(num_records):
        record = {}
        for field in model_fields:
            if field["type"] == "foreign_key":
                # Handle foreign key linking
                ref_model, ref_field = field["references"].split(".")
                record[field["name"]] = random.choice(relationships[ref_model])[ref_field]
            else:
                record[field["name"]] =DynamicMapping.generate_field_value(field,field["type"])
        data.append(record)
    return data


data_models = {
  "data_models": {
    "personal_info_model": [
        {"name": "User ID", "type":"uuid"},
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
    ],
    "accounts_data_model": [
        {"name": "Account ID", "type": "uuid"},
        {"name": "User ID", "type": "dynamic_link","dynamic_link": {"model": "personal_info_model", "field": "User ID"} },  # Link to personal_info_model
        {"name": "Account Type", "type": "choice", "choices": ["savings", "checking", "business"]},
        {"name": "Balance", "type": "number", "min": 1000, "max": 50000},
        {"name": "Creation Date", "type": "datetime"},
        {"name": "Is Verified", "type": "boolean"}
    ],
    "Transaction_data_model": [
        {"name": "Transaction ID", "type": "uuid"},
        {"name": "Account ID", "type": "dynamic_link","dynamic_link": {"model": "accounts_data_model", "field": "Account ID"}},  # Link to accounts_data_model
        {"name": "Transaction Type", "type": "dynamic_link","dynamic_link": {"model": "accounts_data_model", "field": "Account Type"}}  # Dynamically link to Account Type
    ]
  }
  
}

num_records = 100000

def filter_data_with_links(data_store, conditions):
    filtered_data = {}
    
    # Step 1: Apply conditions to individual models
    for condition in conditions:
        model = condition["model"]
        condition_str = condition["condition"]
        data = data_store.get(model, [])
        
        # Evaluate the condition for each record
        filtered_data[model] = [
            record for record in data if eval(condition_str, {}, record)
        ]
    
    # Propagate filters across linked models
    for model_name, records in data_store.items():
        for field in data_models["data_models"][model_name]:
            if field["type"] == "dynamic_link":
                linked_model = field["dynamic_link"]["model"]
                linked_field = field["dynamic_link"]["field"]
                
                # Get filtered values from the linked model
                linked_values = {r[linked_field] for r in filtered_data.get(linked_model, [])}
                
                # Filter current model based on linked field
                filtered_data[model_name] = [
                    record for record in filtered_data.get(model_name, records) 
                    if record[field["name"]] in linked_values
                ]
    return filtered_data



def generate_dynamic_data(model_schemas):
    """
    Generate fake data dynamically for all given model schemas.
    
    :param model_schemas: A dictionary of model names with their respective field definitions.
    :return: A dictionary with fake data for each model.
    """
    data_models, constraints = parse_user_input(model_schemas)
    allDataModel = {}
    for model_name, schema in data_models.items():
        currentDataModel=DynamicMapping.generate_data_from_model(schema,num_records)
        fakeDataGenerator=dynamiclink_check(schema,currentDataModel,allDataModel)
        
        allDataModel[model_name] = fakeDataGenerator #dynamicmapping.generate_data_from_model(schema,num_records)
        
    allresults= filter_data_with_links(allDataModel,constraints)
    for model_name,model in allresults.items():
        converttoDF=pandas.DataFrame(model)
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
                       
                else:
                    print(f"Warning: Target model '{target_model_name}' does not contain any data for field '{target_field}'.")
                 
    return currentDataModel


 # Generate data
generated_data = generate_dynamic_data(data_models)
converttoDF=pandas.DataFrame(generated_data)
converttoDF.to_csv('sample.csv',index=False)


# generate_data.py

import random
from models import DynamicMapping
from collections import defaultdict

def process_dynamic_link(model_name, link_config, all_data):
    """
    Handle dynamic linking between models, given the model name and the field to link to.
    
    :param model_name: The name of the model to look up.
    :param link_config: The dynamic link configuration, which includes the model and field.
    :param all_data: All generated data to be used for dynamic linking.
    :return: Random choice of data from the target model's field.
    """
    target_model_name = link_config["model"]
    target_field = link_config["field"]
    
    if target_model_name in all_data:
        # Ensure the model data is a list (i.e., multiple records in a model)
        linked_model_data = [item[target_field] for item in all_data[target_model_name]]
        return random.choice(linked_model_data)
    else:
        print(f"Error: Model '{target_model_name}' not found for dynamic link.")
        return None

def generate_dynamic_data(model_schemas):
    """
    Generate fake data dynamically for all given model schemas, with links between models.
    
    :param model_schemas: A dictionary of model names with their respective field definitions.
    :return: A dictionary with fake data for each model.
    """
    fake_data = defaultdict(list)
    
    # A dictionary to store intermediate data (for dynamic linking)
    all_generated_data = {}

    # First, generate all models dynamically
    for model_name, model_schema in model_schemas.items():
        # Generate fake data for this model
        model_data = []
        for _ in range(10):  # Can adjust the number of records per model here
            generated_data = generate_fake_data_for_model(model_schema)
            
            # Check for dynamic links and replace with appropriate values
            for field in model_schema:
                field_name = field["name"]
                field_type = field["type"]
                
                if isinstance(field_type, dict) and "dynamic_link" in field_type:
                    # Handle dynamic linking for this field
                    link_config = field_type["dynamic_link"]
                    generated_data[field_name] = process_dynamic_link(model_name, link_config, fake_data)
            
            model_data.append(generated_data)
        
        fake_data[model_name] = model_data
        all_generated_data[model_name] = model_data
    
    return fake_data

import uuid
import pandas as pd
from faker import Faker
import random
import MetaDataRef as metadataRef

# Initialize Faker instance
fake = Faker()

# Function to calculate age based on the Date of Birth
def calculate_age(date_of_birth):
    today = datetime.today()
    birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Function to find the correct field name based on metadata
def get_field_name(field_name):
    for key, variations in metadataRef.FIELD_METADATA.items():
        if field_name.lower() in variations:
            return key  # return the standardized field name
    return field_name  # if no match, return the original field name

def  generate_field_value(field_name, field_type):
       
            if field_type == 'gender':
                return random.choice(['male', 'female'])
            if field_type == 'name':
                # If gender is provided, generate name accordingly
                gender = random.choice(['male', 'female'])
                if gender == 'male':
                    return  fake.first_name_male() + " " + fake.last_name_male()
                elif gender == 'female':
                    return  fake.first_name_female() + " " + fake.last_name_female()
            elif field_type == 'address':
                     return  fake.address().replace('\n', ', ')
            elif field_type == 'email':
               return  fake.email()
            elif field_type == 'phone':
                return   fake.phone_number()
            elif field_type == 'company':
                return  fake.company()
            elif field_type == 'job':
                return  fake.job()
            elif field_type == 'date':
                return  fake.date()
            elif field_type == 'boolean':
                # Generate a Boolean value (True or False)
               return  random.choice([True, False])
            elif field_type == 'number':
                return  random.randint(1, 111000000000)
            elif field_type == 'text':
                return  fake.text(max_nb_chars=100)
            elif field_type == 'credit_card':
                return  fake.credit_card_number(card_type='mastercard')
            elif field_type == 'datetime':
                return  fake.date_time_this_century()
            elif field_type == 'uuid':
                return  str(uuid.uuid4())
            elif field_type == 'ip_address':
                return  fake.ipv4()
            elif field_type == 'file_path':
               return  fake.file_path()
            elif field_type == 'image_url':
               return  fake.image_url()
            elif field_type == 'url':
                return  fake.url()
            elif field_type  in ('id', 'user  id'):
                return  fake.random_int(min=1000000000, max=9999999999)
            elif field_type == 'passport':
                return  fake.passport_number()
            elif field_type == 'ssn':
               return  fake.ssn()
            elif field_type == 'driving_license':
                return  fake.license_plate()
            elif field_type == 'payment_method':
               return  random.choice(['credit_card', 'debit_card', 'paypal', 'bank_transfer'])
            elif field_type == 'transaction_id':
                return  uuid.uuid4().hex
            elif field_type == 'amount_paid':
                return  round(random.uniform(10.0, 1000.0), 2)
            elif field_type == 'payment_status':
                return random.choice(['successful', 'failed', 'pending'])
            elif field_type == 'payment_date':
               return  fake.date_this_year()
            elif field_type == 'event_name':
                return fake.bs()
            elif field_type == 'event_date':
                return  fake.date_this_year()
            elif field_type == 'event_location':
                return  fake.address()
            elif field_type == 'event_type':
                return  random.choice(['conference', 'seminar', 'workshop', 'webinar'])
            elif field_type == 'latitude':
               return  fake.latitude()
            elif field_type == 'longitude':
               return  fake.longitude()
            elif field_type == 'timezone':
                return  fake.timezone()
            elif field_type == 'region':
                return  fake.state()
            elif field_type == 'transaction_id':
                return  uuid.uuid4()
            elif field_type == 'amount_paid':
                return  round(random.uniform(10.0, 1000.0), 2)
            elif field_type == 'payment_status':
                return  random.choice(['successful', 'failed', 'pending'])
            elif field_type == 'payment_date':
                return  fake.date_this_year()
            elif field_type == 'shipment_tracking_number':
                return  fake.uuid4().hex
            elif field_type == 'shipment_status':
                return  random.choice(['shipped', 'in transit', 'delivered', 'pending'])
            elif field_type == 'shipment_date':
               return fake.date_this_year()
            elif field_type == 'delivery_date':
                return  fake.date_this_year()
            elif field_type == 'carrier':
                return  random.choice(['FedEx', 'UPS', 'DHL', 'USPS'])
            elif field_type == 'order_id':
                return  uuid.uuid4().hex
            elif field_type == 'order_date':
                return fake.date_this_year()
            elif field_type == 'order_status':
                return random.choice(['completed', 'pending', 'canceled', 'refunded'])
            elif field_type == 'order_total':
                return  round(random.uniform(20.0, 2000.0), 2)
            elif field_type == 'sales_id':
                return  uuid.uuid4().hex
            elif field_type == 'quantity_sold':
                return  random.randint(1, 50)
            elif field_type == 'sales_amount':
                return  round(random.uniform(10.0, 5000.0), 2)
            elif field_type == 'sale_date':
                return  fake.date_this_year()
            elif field_type == 'sale_status':
                return  random.choice(['completed', 'returned', 'pending'])
            elif field_type == 'sale_region':
                return  fake.state()
            elif field_type == 'customer_id':
                return  fake.uuid4()
            elif field_type == 'id':
                return  uuid.uuid4().hex
            else:
               return  None

# Function to generate synthetic data based on the custom data model with custom validation
def generate_data_from_model(data_model, num_records=100, 
                             min_age=18, max_age=65, 
                             parent_data=None,all_data=None,
                             existing_data=None, dynamic_links=None,):
    data = []
    gender=''
    for _ in range(num_records):
        record = {}
        
        for field in data_model:
            field_name = field.get('name')
            field_type = field.get('type')
            
            # Standardize the field name based on metadata variations
            standardized_field_name = get_field_name(field_name)
            
           
            # Handle different data types
            if field_type == 'name':
                # If gender is provided, generate name accordingly
                gender = record.get('gender', random.choice(['male', 'female']))
               
                if gender == 'male':
                    record[standardized_field_name] = fake.first_name_male() + " " + fake.last_name_male()
                elif gender == 'female':
                    record[standardized_field_name] = fake.first_name_female() + " " + fake.last_name_female()  
            elif field_type == 'gender':
                    if gender != '' :
                        record[standardized_field_name] = gender
                    else:
                         record[standardized_field_name] =  random.choice(['male', 'female'])
            elif field_type == 'address':
                # Custom logic for generating full address or separate components
                address_format = field.get('address_format', 'full')  # Default to full address
                
                if address_format == 'full':
                    record[standardized_field_name] = fake.address().replace('\n', ', ')
                elif address_format == 'split':
                    record['address_line1'] = fake.street_address()
                    record['address_line2'] = fake.secondary_address()
                    record['city'] = fake.city()
                    record['state'] = fake.state()
                    record['postal_code'] = fake.zipcode()
                    record['country'] = fake.country()
            elif field_type == 'email':
                record[standardized_field_name] = fake.email()
            elif field_type == 'phone':
                record[standardized_field_name] = fake.phone_number()
            elif field_type == 'company':
                record[standardized_field_name] = fake.company()
            elif field_type == 'job':
                record[standardized_field_name] = fake.job()
            elif field_type == 'date':
                record[standardized_field_name] = fake.date()
            elif field_type == 'boolean':
                # Generate a Boolean value (True or False)
                record[standardized_field_name] = random.choice([True, False])
            elif field_type == 'number':
                min_val = field.get('min', 0)
                max_val = field.get('max', 100)
                record[standardized_field_name] = random.randint(min_val, max_val)
            elif field_type == 'choice':
                choices = field.get('choices', [])
                record[standardized_field_name] = random.choice(choices)
            elif field_type == 'text':
                record[standardized_field_name] = fake.text(max_nb_chars=100)
            elif field_type == 'credit_card':
                record[standardized_field_name] = fake.credit_card_number(card_type='mastercard')
            elif field_type == 'datetime':
                record[standardized_field_name] = fake.date_time_this_century()
            elif field_type == 'uuid':
                record[standardized_field_name] = str(uuid.uuid4())
            elif field_type == 'ip_address':
                record[standardized_field_name] = fake.ipv4()
            elif field_type == 'file_path':
                record[standardized_field_name] = fake.file_path()
            elif field_type == 'image_url':
                record[standardized_field_name] = fake.image_url()
            elif field_type == 'url':
                record[standardized_field_name] = fake.url()
            elif field_type == 'id':
                record[standardized_field_name] = fake.random_int(min=1000000000, max=9999999999)
            elif field_type == 'passport':
                record[standardized_field_name] = fake.passport_number()
            elif field_type == 'ssn':
                record[standardized_field_name] = fake.ssn()
            elif field_type == 'driving_license':
                record[standardized_field_name] = fake.license_plate()
            elif field_type == 'payment_method':
                record[standardized_field_name] = random.choice(['credit_card', 'debit_card', 'paypal', 'bank_transfer'])
            elif field_type == 'transaction_id':
                record[standardized_field_name] = uuid.uuid4().hex
            elif field_type == 'amount_paid':
                record[standardized_field_name] = round(random.uniform(10.0, 1000.0), 2)
            elif field_type == 'payment_status':
                record[standardized_field_name] = random.choice(['successful', 'failed', 'pending'])
            elif field_type == 'payment_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'event_name':
                record[standardized_field_name] = fake.bs()
            elif field_type == 'event_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'event_location':
                record[standardized_field_name] = fake.address()
            elif field_type == 'event_type':
                record[standardized_field_name] = random.choice(['conference', 'seminar', 'workshop', 'webinar'])
            elif field_type == 'latitude':
                record[standardized_field_name] = fake.latitude()
            elif field_type == 'longitude':
                record[standardized_field_name] = fake.longitude()
            elif field_type == 'timezone':
                record[standardized_field_name] = fake.timezone()
            elif field_type == 'region':
                record[standardized_field_name] = fake.state()
            elif field_type == 'transaction_id':
                record[standardized_field_name] = uuid.uuid4().hex
            elif field_type == 'amount_paid':
                record[standardized_field_name] = round(random.uniform(10.0, 1000.0), 2)
            elif field_type == 'payment_status':
                record[standardized_field_name] = random.choice(['successful', 'failed', 'pending'])
            elif field_type == 'payment_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'shipment_tracking_number':
                record[standardized_field_name] = fake.uuid4().hex
            elif field_type == 'shipment_status':
                record[standardized_field_name] = random.choice(['shipped', 'in transit', 'delivered', 'pending'])
            elif field_type == 'shipment_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'delivery_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'carrier':
                record[standardized_field_name] = random.choice(['FedEx', 'UPS', 'DHL', 'USPS'])
            elif field_type == 'order_id':
                record[standardized_field_name] = uuid.uuid4().hex
            elif field_type == 'order_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'order_status':
                record[standardized_field_name] = random.choice(['completed', 'pending', 'canceled', 'refunded'])
            elif field_type == 'order_total':
                record[standardized_field_name] = round(random.uniform(20.0, 2000.0), 2)
            elif field_type == 'sales_id':
                record[standardized_field_name] = uuid.uuid4().hex
            elif field_type == 'quantity_sold':
                record[standardized_field_name] = random.randint(1, 50)
            elif field_type == 'sales_amount':
                record[standardized_field_name] = round(random.uniform(10.0, 5000.0), 2)
            elif field_type == 'sale_date':
                record[standardized_field_name] = fake.date_this_year()
            elif field_type == 'sale_status':
                record[standardized_field_name] = random.choice(['completed', 'returned', 'pending'])
            elif field_type == 'sale_region':
                record[standardized_field_name] = fake.state()
            elif field_type == 'customer_id':
                record[standardized_field_name] = fake.uuid4().hex
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
            else:
                record[standardized_field_name] = None
        
        data.append(record)
    
    return data

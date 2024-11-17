from faker import Faker
import random
import pandas as pd
import uuid
from datetime import datetime

# Initialize the Faker instance
fake = Faker()

# Expanded Metadata dictionary for possible field name variations
FIELD_METADATA = {
    # Personal Information
    "name": ["firstname", "fname", "person name", "legal name", "full name", "given name", "first name", "last name", "user name", "user full name"],
    "email": ["email address", "email", "contact email", "email id", "user email", "email address"],
    "phone": ["phone number", "mobile", "contact number", "telephone", "cell number", "contact phone", "mobile number", "phone number", "home phone"],
    "dob": ["dob", "date of birth", "birth date", "birthdate", "age"],
    "gender": ["gender", "sex", "person gender", "user gender", "sex", "user sex"],
    
    # Address
    "address": ["address", "home address", "residential address", "street address", "location", "postal address", "street", "residence address"],
    "address_line1": ["address_line1", "street", "line 1", "address 1", "address part 1", "address line 1"],
    "address_line2": ["address_line2", "suite", "line 2", "address 2", "address part 2", "address line 2"],
    "city": ["city", "town", "municipality", "city name", "location", "city of residence"],
    "state": ["state", "province", "region", "state name", "state of residence"],
    "country": ["country", "nation", "country name", "territory", "nationality", "region"],
    "postal_code": ["postal_code", "zipcode", "zip code", "postal code", "pin code", "zip", "postcode"],
    
    # Financial Information
    "payment_method": ["payment_method", "payment type", "payment method", "method of payment", "transaction type"],
    "transaction_id": ["transaction_id", "tx_id", "transaction identifier", "transaction number", "transaction_code"],
    "amount_paid": ["amount_paid", "payment_amount", "amount", "invoice_amount", "total_paid", "payment total"],
    "payment_status": ["payment_status", "status", "payment_result", "payment status", "payment outcome"],
    "payment_date": ["payment_date", "date_of_payment", "payment timestamp", "payment made on"],
    
    # Legal Information
    "passport": ["passport", "passport_number", "passport id", "passport number", "international passport", "travel document"],
    "ssn": ["ssn", "social security number", "social security", "ssn number", "social security info", "social_security"],
    "tax_id": ["tax_id", "tax identification", "tax_number", "taxpayer id"],
    "driving_license": ["driving_license", "driver's_license", "driving permit", "driving permit number"],
    
    # Health Information
    "height": ["height", "person height", "body height", "human height", "height_cm", "height_inch"],
    "weight": ["weight", "person weight", "body weight", "human weight", "weight_kg", "weight_lbs"],
    "blood_type": ["blood_type", "blood group", "blood type", "blood group type", "blood group"],
    "medical_history": ["medical_history", "health_history", "health record", "medical record", "medical history notes"],
    "insurance_number": ["insurance_number", "health insurance number", "insurance_id", "insurance policy number"],
    
    # Product Information
    "product_id": ["product_id", "product identifier", "product code", "product_number", "item_id"],
    "product_name": ["product_name", "product_title", "item_name", "product description", "product label"],
    "product_category": ["product_category", "item category", "product type", "category", "category_name"],
    "price": ["price", "product_price", "cost", "item price", "product cost"],
    "quantity_in_stock": ["quantity_in_stock", "stock_quantity", "available_stock", "items_in_stock"],
    "supplier_name": ["supplier_name", "manufacturer", "supplier", "vendor", "distributor"],
    
    # Order Information
    "order_id": ["order_id", "order_number", "order_code", "order identifier", "purchase_id"],
    "order_date": ["order_date", "date_of_order", "purchase_date", "order timestamp", "date_placed"],
    "order_status": ["order_status", "status", "order status", "purchase_status"],
    "order_total": ["order_total", "total_amount", "total_cost", "order value", "order_amount"],
    "billing_address": ["billing_address", "invoice_address", "billing_location", "invoice_location", "billing_address_line"],
    "shipping_address": ["shipping_address", "shipping_location", "delivery_address", "ship_to_address", "destination_address"],
    
    # Shipment Information
    "shipment_tracking_number": ["shipment_tracking_number", "tracking_number", "shipment id", "tracking_code", "shipment_id"],
    "shipment_status": ["shipment_status", "shipment state", "shipment status", "shipment progress"],
    "shipment_date": ["shipment_date", "shipment dispatched", "shipment dispatch_date", "shipped_date"],
    "delivery_date": ["delivery_date", "delivered_date", "delivery_timestamp", "delivery_day"],
    "carrier": ["carrier", "shipping_carrier", "delivery_service", "shipment carrier"],
    "delivery_address": ["delivery_address", "shipment_address", "delivery location", "destination_address"],
    
    # Sales Data
    "sales_id": ["sales_id", "sale_id", "sale identifier", "sales transaction id", "sale_code"],
    "quantity_sold": ["quantity_sold", "items_sold", "number_of_items_sold", "sold_quantity"],
    "sales_amount": ["sales_amount", "total_sales", "sale_value", "sale amount", "total_sales_value"],
    "sale_date": ["sale_date", "transaction_date", "sale_timestamp", "sales_date"],
    "sale_status": ["sale_status", "sale outcome", "transaction status", "purchase status"],
    "sale_region": ["sale_region", "region", "sale_location", "sales territory"],
    "customer_id": ["customer_id", "user_id", "client_id", "customer_identifier", "user identifier"]
}

# Function to calculate age based on the Date of Birth
def calculate_age(date_of_birth):
    today = datetime.today()
    birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Function to find the correct field name based on metadata
def get_field_name(field_name):
    for key, variations in FIELD_METADATA.items():
        if field_name.lower() in variations:
            return key  # return the standardized field name
    return field_name  # if no match, return the original field name

# Function to generate synthetic data based on the custom data model with custom validation
def generate_data_from_model(data_model, num_records=100, min_age=18, max_age=65, parent_data=None):
    data = []
    
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
            else:
                record[standardized_field_name] = None
        
        data.append(record)
    
    return data

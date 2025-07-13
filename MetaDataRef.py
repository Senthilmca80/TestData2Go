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
    "name": ["firstname", "fname", "person name", "legal name", "full name", "given name", "first name", "last name", "user name", "user full name", "name"],
    "email": ["email address", "email", "contact email", "email id", "user email", "email address"],
    "phone": ["phone number", "mobile", "contact number", "telephone", "cell number", "contact phone", "mobile number", "phone number", "home phone"],
    "date": ["dob", "date of birth", "birth date", "birthdate", "age"],
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
    
    # Event Information
    "event_name": ["event_name", "event title", "event label", "event description", "event"],
    "event_date": ["event_date", "event day", "date_of_event", "event_datetime", "event_time"],
    "event_location": ["event_location", "event_address", "event venue", "event site", "event location"],
    "event_type": ["event_type", "event_category", "event format", "event kind"],
    
    # User Activity
    "last_login": ["last_login", "last_access", "login_timestamp", "last session", "last_login_time"],
    "total_purchases": ["total_purchases", "purchase_count", "number_of_purchases", "purchases made", "total_orders"],
    "cart_items": ["cart_items", "cart_quantity", "cart_content", "number_of_items_in_cart"],
    "total_spent": ["total_spent", "spending", "total_expenditure", "total_purchase_amount"],
    "last_purchase_date": ["last_purchase_date", "last_purchase", "last_order_date", "last_transaction_date"],

    # Location Information
    "latitude": ["latitude", "lat", "geo_latitude", "geo_lat", "geo_latitude_value"],
    "longitude": ["longitude", "lng", "geo_longitude", "geo_lng", "geo_longitude_value"],
    "timezone": ["timezone", "user_timezone", "time_zone", "timezone_offset"],
    "region": ["region", "province", "territory", "district"],

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
    "customer_id": ["customer_id", "user_id", "client_id", "customer_identifier", "user identifier"],

    "id" :["User ID","Account ID","Transaction ID"],
    "boolean": ["Is Verified"]

}


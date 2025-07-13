from sqlalchemy import create_engine, inspect
import pandas as pd
from sdv.tabular import GaussianCopula


def connect_to_db_with_windows_auth(driver, server, database):
    """Establish a connection to the database using Windows Authentication."""
    connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes"
    engine = create_engine(connection_string)
    return engine

def connect_to_db(db_type, host, port, db_name, username, password):
    """Establish a connection to the database."""
    connection_string = f"{db_type}://{username}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(connection_string)
    return engine

def get_table_schema(engine, table_name):
    """Retrieve schema of a given table."""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    schema = {}
    for column in columns:
        schema[column['name']] = {
            'type': str(column['type']),
            'nullable': column['nullable'],
            'primary_key': column['primary_key']
        }
    return schema

def extract_data(engine, table_name, sample_size=1000):
    """Extract sample data from the table."""
    query = f"SELECT * FROM {table_name} LIMIT {sample_size}"
    data = pd.read_sql(query, engine)
    return data

def generate_synthetic_data(data, num_rows=1000):
    model = GaussianCopula()
    model.fit(data)
    synthetic_data = model.sample(num_rows)
    return synthetic_data

# Example usage:
# engine = connect_to_db('postgresql', 'localhost', '5432', 'mydb', 'user', 'pass')
# schema = get_table_schema(engine, 'patients')
# data_sample = extract_data(engine, 'patients')
# print(schema)
# print(data_sample.head())


engine = connect_to_db_with_windows_auth('ODBC Driver 17 for SQL Server', 'DESKTOP-MU49L7R\\SQLEXPRESS01', 'orderDB')
data_sample = extract_data(engine, 'order',100)
synthetic_data = generate_synthetic_data(data_sample)
print(synthetic_data.head())

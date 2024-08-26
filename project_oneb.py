from sqlalchemy import create_engine
import pandas as pd

# Load the CSV file
file_path = 'Customers.csv'
df = pd.read_csv(file_path,  encoding='ISO-8859-1')

# Database credentials
db_username = 'postgres'
db_password = 'Lightstone1'  # Replace with your actual password
db_host = 'localhost'
db_port = '5434'
db_name = 'myretail'
table_name = 'Customers'


# Create the connection string
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
engine

# Load your DataFrame into the PostgreSQL table
df.to_sql(table_name, engine, if_exists='replace', index=False)

print("Data successfully loaded into PostgreSQL")

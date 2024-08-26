from sqlalchemy import create_engine
import pandas as pd

# Load the CSV file
file_path = 'Customers.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Database credentials
db_username = 'DESKTOP-KL8B19B\SQLEXPRESS'  # Replace with your actual SQL Server username
db_password = 'Lightstone1'  # Replace with your actual password
db_host = 'localhost'
db_port = '1433'  # Default port for SQL Server
db_name = 'myretailpy'
table_name = 'Customers'

# Create the connection string for SQL Server
connection_string = (
    f"mssql+pyodbc://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(connection_string)

# Load your DataFrame into the SQL Server table
df.to_sql(table_name, engine, if_exists='replace', index=False)

print("Data successfully loaded into SQL Server")
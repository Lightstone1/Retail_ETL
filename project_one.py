import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load the CSV file
Filepath= 'Customers.csv'


def extract(Filepath):
    data = pd.read_csv(Filepath, encoding='ISO-8859-1')
    print(f'The data has successfully loaded from {Filepath}')
    return data


def transform (data):
    data['Birthday'] = pd.to_datetime(data['Birthday'])
    from datetime import datetime
    data['Age'] = datetime.now().year - data['Birthday'].dt.year
    data[['First Name', 'Last Name']] = data['Name'].str.split(' ', n=1, expand=True)
    print('Data has successfully transformed')
    return(data)


def load (data, tablename):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv ('DB_HOST')
    port = os.getenv('DB_PORT') 
    name = os.getenv ('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    data.to_sql(tablename, engine, if_exists="replace", index=False)
    print(f"data successfully loaded into [tablename] table")

def pipeline(Filepath, tablename):
    data= extract(Filepath)
    transformed_data = transform(data)
    load(transformed_data, tablename)
   
tablename = 'cust'

pipeline(Filepath, tablename)



























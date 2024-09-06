import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load the CSV file
customer_filepath= 'Customers.csv'


def extract(customer_filepath):
    customer_data = pd.read_csv(customer_filepath, encoding='ISO-8859-1')
    print(f'The data has successfully loaded from {customer_filepath}')
    return customer_data


def transform (customer_data):
    customer_data['Birthday'] = pd.to_datetime(customer_data['Birthday'])
    from datetime import datetime
    customer_data['Age'] = datetime.now().year - customer_data['Birthday'].dt.year
    customer_data[['First Name', 'Last Name']] = customer_data['Name'].str.split(' ', n=1, expand=True)
    print('Data has successfully transformed')
    return(customer_data)


def load (customer_data, tablename):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv ('DB_HOST')
    port = os.getenv('DB_PORT') 
    name = os.getenv ('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    customer_data.to_sql(tablename, engine, if_exists="replace", index=False)
    print(f"data successfully loaded into [tablename] table")

def pipeline(customer_filepath, tablename):
    customer_data= extract(customer_filepath)
    transformed_data = transform(customer_data)
    load(transformed_data, tablename)
   
tablename = 'customer'

pipeline(customer_filepath, tablename)


##Loading the Products data ###
# Load the CSV file
product_filepath ='Products.csv'

def extract(product_filepath):
    product_data = pd.read_csv(product_filepath)
    print(f'The data has successfully loaded from {product_filepath}')
    return product_data


def transform (product_data):
    product_data['Unit Cost USD'] = product_data['Unit Cost USD'].replace('[\$,]', '', regex=True).astype(float)
    product_data['Unit Price USD'] = product_data['Unit Price USD'].replace('[\$,]', '', regex=True).astype(float)
    print('Data has successfully transformed')
    return(product_data)

def load (product_data, tablename):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv ('DB_HOST')
    port = os.getenv('DB_PORT') 
    name = os.getenv ('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    product_data.to_sql(tablename, engine, if_exists="replace", index=False)
    print(f"data successfully loaded into [tablename] table")

def pipeline(product_filepath, tablename):
    product_data= extract(product_filepath)
    transformed_data = transform(product_data)
    load(transformed_data, tablename)
   
tablename = 'product'

pipeline(product_filepath, tablename)





##Loading the sales data ###
# Load the CSV file
sales_filepath ='Sales.csv'

def extract(sales_filepath):
    sales_data = pd.read_csv(sales_filepath)
    print(f'The data has successfully loaded from {sales_filepath}')
    return sales_data


def transform (sales_data):
    ###coverting delivery date and order date to date type###
    sales_data['Order Date'] = pd.to_datetime(sales_data['Order Date'])
    sales_data['Delivery Date'] = pd.to_datetime(sales_data['Delivery Date']) 
    ##Adding new columns for delivery status##
    sales_data['Delivery Status'] = sales_data['Delivery Date'].apply(lambda x: 'Delivery Date Not Recorded' if pd.isna(x) else 'Delivery Date Recorded')
    #Filling missing delivery dates with the order date#
    sales_data['Delivery Date'].fillna(sales_data['Order Date'], inplace=True)
    ##Adding new columns##
    sales_data['Order Duration'] = (sales_data['Delivery Date'] - sales_data['Order Date']).dt.days
    print('Data has successfully transformed')
    return(sales_data)

def load (sales_data, tablename):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv ('DB_HOST')
    port = os.getenv('DB_PORT') 
    name = os.getenv ('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    sales_data.to_sql(tablename, engine, if_exists="replace", index=False)
    print(f"data successfully loaded into [tablename] table")

def pipeline(sales_filepath, tablename):
    sales_data= extract(sales_filepath)
    transformed_data = transform(sales_data)
    load(transformed_data, tablename)
   
tablename = 'sales'

pipeline(sales_filepath, tablename)



##Loading the stores data ###
# Load the CSV file
stores_filepath ='Stores.csv'

def extract(stores_filepath):
    stores_data = pd.read_csv(stores_filepath)
    print(f'The data has successfully loaded from {stores_filepath}')
    return stores_data


def transform (stores_data):
    #convert the Open Date column from an object type to a datetime type.##
    stores_data['Open Date'] = pd.to_datetime(stores_data['Open Date'])
    # Add 'Store Age (Years)' feature
    stores_data['Store Age in years'] = (pd.to_datetime('today') - stores_data['Open Date']).dt.days // 365
    print('Data has successfully transformed')
    return(stores_data)

def load (stores_data, tablename):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv ('DB_HOST')
    port = os.getenv('DB_PORT') 
    name = os.getenv ('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    stores_data.to_sql(tablename, engine, if_exists="replace", index=False)
    print(f"data successfully loaded into [tablename] table")

def pipeline(stores_filepath, tablename):
    stores_data= extract(stores_filepath)
    transformed_data = transform(stores_data)
    load(transformed_data, tablename)
   
tablename = 'stores'

pipeline(stores_filepath, tablename)





##Loading the exchange rates data ###
# Load the CSV file
exchange_filepath ='Exchange_Rates.csv'

def extract(exchange_filepath):
    exchange_data = pd.read_csv(exchange_filepath)
    print(f'The data has successfully loaded from {exchange_filepath}')
    return exchange_data


def transform (exchange_data):
    #  Convert 'Date' to datetime format
    exchange_data['Date'] = pd.to_datetime(exchange_data['Date'])
    print('Data has successfully transformed')
    return(exchange_data)

def load (exchange_data, tablename):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv ('DB_HOST')
    port = os.getenv('DB_PORT') 
    name = os.getenv ('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    exchange_data.to_sql(tablename, engine, if_exists="replace", index=False)
    print(f"data successfully loaded into [tablename] table")

def pipeline(exchange_filepath, tablename):
    exchange_data= extract(exchange_filepath)
    transformed_data = transform(exchange_data)
    load(transformed_data, tablename)
   
tablename = 'exchange'

pipeline(exchange_filepath, tablename)


import os 
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## This file is to push the data to the mongadb
load_dotenv()

## Access the mongodb url
MONGO_DB_URL=os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)

ca=certifi.where()
##  get trusted certificate used for request


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def cv_to_json_convertor(self,file_path):
        try:
            self.file_path=file_path
            data=pd.read_csv(self.file_path)
            data.reset_index(drop=True)
            ## we will convert into list of json so that we can push it into mongodb line [{},{},{}]
            records=list(json.loads((data.T.to_json())).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.records=records
            self.collection=collection
            ## Connects mongodb using python
            self.mongo_clients=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_clients[self.database]
            # This accesses the MongoDB database.
            self.collection=self.database[self.collection]
            # This gets a specific collection from that database. like tables
            self.collection.insert_many(self.records)
            # This inserts multiple documents (rows) into the collection.
            # records must be a list of Python dictionaries, where each dictionary is one document (row).
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
if __name__=="__main__":
    FILE_PATH='Network_Data\phisingData.csv'
    DATABASE='sarvespoker'
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
        
'''
# Original DataFrame
data = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [30, 24],
    'City': ['NY', 'LA']
})

print("Original DataFrame:\n", data)
#   Name  Age City
# 0  Alice   30   NY
# 1    Bob   24   LA

# Transposed DataFrame
data_T = data.T
print("\nTransposed DataFrame (data.T):\n", data_T)
#        0    1
# Name  Alice  Bob
# Age      30   24
# City     NY   LA

# JSON string from transposed DataFrame (default orient='columns')
json_string = data_T.to_json()
print("\nJSON string from data.T.to_json():\n", json_string)
# {"0":{"Name":"Alice","Age":30,"City":"NY"},"1":{"Name":"Bob","Age":24,"City":"LA"}}
# Notice the keys "0" and "1" which are the original row indices.

# Python object after json.loads()
python_dict = json.loads(json_string)
print("\nPython dictionary after json.loads():\n", python_dict)
# {'0': {'Name': 'Alice', 'Age': 30, 'City': 'NY'}, '1': {'Name': 'Bob', 'Age': 24, 'City': 'LA'}}

# Values of the dictionary
dict_values_view = python_dict.values()
print("\nDictionary values view:\n", dict_values_view)
# dict_values([{'Name': 'Alice', 'Age': 30, 'City': 'NY'}, {'Name': 'Bob', 'Age': 24, 'City': 'LA'}])

'''
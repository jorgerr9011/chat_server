from pymongo import MongoClient
import json
from bson import ObjectId, Timestamp 
from datetime import datetime

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def delete_fields(d, fields): 
    if isinstance(d, dict):
        for field in fields:
            if field in d:
                del d[field]
        for key in d:
            delete_fields(d[key], fields)
    elif isinstance(d, list):
        for item in d:
            delete_fields(item, fields)

def write_data():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/incidenceMongo")

        # Get the incidence collection
        incidencias = client.incidenceMongo.incidences

        # Fetch data from the collection
        data = incidencias.find()

        fields_to_delete = ["email", "status", "__v", "_id", "createdAt", "updatedAt"] 
        data_json = []

        for document in data:
            delete_fields(document, fields_to_delete)
            data_json.append(document)
            
        datos = json.dumps(data_json, indent=4, sort_keys=True, default=default_serializer)

        #print(data_json)

        with open('./registros/data.json', 'w') as outfile:
           outfile.write(datos)

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

    finally:
        # Close the connection (optional, client might be garbage collected)
        if client:
            client.close()

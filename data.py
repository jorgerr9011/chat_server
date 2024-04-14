from pymongo import MongoClient
import json
import os
from bson import ObjectId, Timestamp 
from datetime import datetime

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def write_data():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/incidenceMongo")

        # Get the incidence collection
        incidencias = client.incidenceMongo.incidences

        # Fetch data from the collection
        data = incidencias.find()

        data_json = []
        for document in data:
            #print(document)
            if "_id" in document and isinstance(document["_id"], ObjectId):
                document["_id"] = str(document["_id"])

            if "createdAt" in document:
                document["createdAt"] = default_serializer(document["createdAt"])

            if "updatedAt" in document:
                document["updatedAt"] = default_serializer(document["updatedAt"])

            data_json.append(document)

        datos = json.dumps(data_json, indent=4, sort_keys=True, default=default_serializer)

        with open('./registros/data.json', 'w') as outfile:
           outfile.write(datos)

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

    finally:
        # Close the connection (optional, client might be garbage collected)
        if client:
            client.close()


#if __name__ == "__main__":
 #   get_data()




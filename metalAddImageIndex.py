from metal_sdk.metal import Metal
from pymongo import MongoClient
import certifi
import configparser

config = configparser.ConfigParser()
config.read('setting.conf')

metal = Metal(
  config['metal']['apiKey'],   # api-key
  config['metal']['clientId'], # client-id
  config['metal']['indexId'],  # index-id
)

def create_metal_doc(webcam):
    embedded_document = {}
    
    embedded_document["imageUrl"] = webcam["image"]["daylight"]["thumbnail"]
    embedded_document["index"] = metalIndexId
    embedded_document["id"] = webcam["id"]
    metadata = {}
    metadata["title"] = webcam["title"]
    metadata["imgUrl"] = webcam["image"]["daylight"]["thumbnail"]
    metadata["country"] = webcam["location"]["country"]
    metadata["latitude"] = webcam["location"]["latitude"]
    metadata["longitude"] = webcam["location"]["longitude"]
    embedded_document["metadata"] = metadata
    #print(embedded_document)
    
    return(embedded_document)

ca = certifi.where()
connection_url = 'mongodb+srv://webcam:webcam@cluster0.pizmgb2.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_url, tlsCAFile=ca)
dbname = client['webcam']
collection = dbname.webcam
webcams = collection.find(filter={"status":"active"})

embedded_document_list = []
for webcam in webcams:
    id = webcam['id']
    if id < "1577870141" :
        continue
    print(id)
    try:
        embedded_document = create_metal_doc(webcam)
    except:
        print("Error")
        continue
    embedded_document_list.append(embedded_document)
    if len(embedded_document_list) == 100:
        print("*************start Request*************")
        try:
            metal.index_many(embedded_document_list)
        except:
            print("Error")
        embedded_document_list = []

if len(embedded_document_list) > 0:
    metal.index_many(embedded_document_list)

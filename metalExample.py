
from metal_sdk.metal import Metal
import json
import configparser
from pymongo import MongoClient
import pymongo

connection_url = 'mongodb+srv://webcam:webcam@cluster0.pizmgb2.mongodb.net/?retryWrites=true&w=majority'

config = configparser.ConfigParser()
config.read('setting.conf')

# Note: Index must be embeddings-ada-02
metal = Metal(
  config['metal']['apiKey'],   # api-key
  config['metal']['clientId'], # client-id
  config['metal']['indexId'],  # index-id
)

captions = {}
with open("caption.txt", "r",encoding='latin-1') as f:
    line = f.readline()
    while line:
      array =line.split(':')
      id =array[0].replace(".jpg","")
      captions[id] = array[1]  
      line = f.readline()

client = MongoClient(connection_url)
dbname = client['webcam']
collection = dbname.webcam
webcams = collection.find(filter={"status":"active"})

def create_metal_doc(webcam,text):
  embedded_document = {}
  embedded_document["text"] = text
  embedded_document["index"] = config['metal']['indexId']
  embedded_document["id"] = webcam["id"]
  metadata = {}
  metadata["title"] = webcam["title"]
  metadata["imgUrl"] = webcam["image"]["current"]["thumbnail"]
  metadata["country"] = webcam["location"]["country"]
  metadata["latitude"] = webcam["location"]["latitude"]
  metadata["longitude"] = webcam["location"]["longitude"]
  embedded_document["metadata"] = metadata
  return(embedded_document)  

embedded_document_list = []
for webcam in webcams:
  if webcam["id"] in captions:
    text = captions[webcam["id"]]
    embedded_document = create_metal_doc(webcam,text)
    print(embedded_document["metadata"]["imgUrl"])
    embedded_document_list.append(embedded_document)
    if len(embedded_document_list) == 100:
      metal.index_many(embedded_document_list)
      embedded_document_list = []

if len(embedded_document_list) > 0:
  metal.index_many(embedded_document_list)

results = metal.search({
  "text": "river",
  },
  limit=1
)

print("result:" + results.text)


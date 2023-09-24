from metal_sdk.metal import Metal
from pymongo import MongoClient
import inspect
import json
import configparser

config = configparser.ConfigParser()
config.read('setting.conf')

metal = Metal(
  config['metal']['apiKey'],   # api-key
  config['metal']['clientId'], # client-id
  config['metal']['indexId'],  # index-id
)

results = metal.search({ "imageUrl": "https://images-webcams.windy.com/83/1011371583/daylight/thumbnail/1011371583.jpg"}, 
                        limit=2)

#test = results
obj=json.loads(results.text)
print(inspect.getmembers(obj))
print(obj["data"][0]["id"])
print(obj["data"][0]["metadata"]["title"])
print(obj["data"][0]["metadata"]["imgUrl"])

#print(inspect.getmembers(test))
#print(results.text.data)
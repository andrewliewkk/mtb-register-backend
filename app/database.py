import pymongo

client = pymongo.MongoClient("mongodb+srv://boyrawks:<password>@mtb.5jq2ed0.mongodb.net/?retryWrites=true&w=majority")
db = client.test

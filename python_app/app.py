from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["key_value_store"]
collection = db["key_value_pairs"]


@app.route('/', methods=['GET'])
def get_all_keys():
    keys = [doc['_id'] for doc in collection.find()]
    return jsonify(keys)


@app.route('/<key>', methods=['GET'])
def get_value(key):
    doc = collection.find_one({"_id": key})
    if doc:
        return jsonify({key: doc['value']})
    else:
        return jsonify({"error": "Key not found"}), 404


@app.route('/<key>', methods=['POST', 'PUT'])
def set_value(key):
    data = request.json
    value = data.get('value')
    if value is None:
        return jsonify({"error": "Value not provided"}), 400
    if collection.count_documents({"_id": key}) > 0:
        collection.update_one({"_id": key}, {"$set": {"value": value}})
    else:
        collection.insert_one({"_id": key, "value": value})
    return jsonify({key: value})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request
from urllib.parse import quote
import redis
from models.models import *
import mongoengine
from pymongo import MongoClient
import bson

app = Flask(__name__)
app.config.from_pyfile('config.py')

# MongoDB setup
client = MongoClient('localhost', 27017, username='username', password='super-secret-password')
mongo_client = client.mydatabase

# Redis setup
password = 'yourpassword'
encoded_password = quote(password, safe="")
redis_client = redis.Redis.from_url('redis://:{}@localhost:6379/0'.format(encoded_password))

# a=UserEntity(Name="asdasd")
# a.save()
mongo_collection = mongo_client.my_collection
@app.route('/')
def hello():
    # MongoDB example
    result = UserEntity.objects()
    
    # Redis example
    redis_key = 'my_key'
    redis_value = 'my_value'
    redis_client.set(redis_key, redis_value)
    redis_result = redis_client.get(redis_key)
    # print(result)
    return f'MongoDB result: {result.to_json()}, Redis result: {redis_result}'

@app.route('/api/retrieve', methods=['GET'])
def retrieve_data():
    # call check auth function which will return user id user_id = funciton for authentication
    user_id= None
    token_values = request.args.get('token')
    token_array = token_values.split(',')
    masking = request.args.get('masking')
    object_collection = mongo_client['ObjectEntity']
    response = []
    #if in redis response the data
    for token in token_array:
        res_dict={}
        object_id = redis_client.hget(user_id, token)
        if object_id:
            # If record exists in redis
            if isinstance(object_id, bson.ObjectId):
                token_res = object_collection.find_one({'_id': object_id, 'Uid': user_id})
                token_dict=token_res['data']
                token_dict['created_at']=token_res['_id'].generation_time
                res_dict[token]=token_dict
            else:
                # Volatile type
                # {name: rishabh} -> "name#rishabh"
                ret_key, ret_value = object_id.split('#')
                # {key: ret_key, value: ret_val}
                res_dict[object_id]={"key": ret_key, "value": ret_value}
            # response.append(token_res['data'])
            # Apply masking here
            # res_dict[object_id]["value"] = masking(res_dict[object_id]["value"])
            response.append(res_dict)
        else:
            # Record not found in redis
            token_res=object_collection.find_one({"Token": token,'Uid': user_id})
            token_dict=token_res['data']
            token_dict['created_at']=token_res['_id'].generation_time
            res_dict[token]=token_dict
            # Apply masking
            # add record to redis
            redis_client.hset(user_id, token, token_res['_id'])

def mask_type(user_id, key):
    config_collection = mongo_client['Config']
    mask_rules = config_collection.find_one({"Uid": user_id})
    for rules in mask_rules:
        rule_values = mask_rules[rules]
        if key in rule_values:
            return rules
    return "normal"


@app.get('/findData')
def getData():    
    collection = mongo_client['UserEntity']
    mongo_collection.insert_one({"name": "Rishabh", "age": 25})
    # Redis example
    redis_key = 'my_key'
    redis_value = 'my_value'    
    redis_client.set(redis_key, redis_value)
    redis_result = redis_client.get(redis_key)
    res = mongo_collection.find_one({"name": "Rishabh"})
    # print(type(res['_id']))
    return str((res['_id']))

if __name__ == '__main__':
    app.run(debug=True)
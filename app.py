from flask import Flask, jsonify, request
from urllib.parse import quote
import redis
from pymongo import MongoClient
from models.models import *
from utils.token_utils import *
# from create import create
import mongoengine
from pymongo import MongoClient
import bson
import json
import re
from models.models import *

app = Flask(__name__)
app.config.from_pyfile('config.py')

# MongoDB setup
client = MongoClient('localhost', 27017, username='username', password='super-secret-password')
mongo_client = client.mydatabase

mongo_db = client.mydatabase
# Redis setup
password = 'yourpassword'
encoded_password = quote(password, safe="")
redis_client = redis.Redis.from_url('redis://:{}@localhost:6379/0'.format(encoded_password))

# a=UserEntity(Name="asdasd")
# a.save()
mongo_collection = mongo_client.my_collection


a=UserEntity(Name="sathya")
a.save()

def sanitize_input(input_string):
    # Remove non-alphanumeric characters except for whitespace
    if(input_string is None):
        return None
    sanitized_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    print(sanitized_string)
    return sanitized_string.strip()

def authenticateApi(Apikey):
    try:
        if Apikey is None:
            return None
        sanitizedKey=sanitize_input(Apikey)
        print(sanitizedKey)
        User=UserEntity.objects.filter(ApiKey=sanitizedKey)[0]
        
        print(dir(User))
        return User
    except:
        print('its here')
        return None

    
@app.route('/')
def hello():
    # MongoDB example
    # mongo_collection = mongo_db.my_collection
    result = UserEntity.objects().filter(Name="sathya")
    
    # Redis example
    redis_key = 'my_key'
    redis_value = 'my_value'
    redis_client.set(redis_key, redis_value)
    redis_result = redis_client.get(redis_key)
    print(result)
    return f'MongoDB result: {result.to_json()}, Redis result: {redis_result}'

@app.route('/api/retrieve/', methods=["GET"])
def retrieve_data():
    # call check auth function which will return user id user_id = funciton for authentication
    print("Inside get endpoint")
    User=authenticateApi(request.headers.get('X-API-KEY'))
    print(User.id)
    user_id= User.id
    # print("user id is ")
    # print(user_id)
    token_values = request.args.get('token')
    token_array = token_values.split(',')
    # print(token_array)
    masking = request.args.get('masking')
    object_collection = mongo_client['ObjectEntity']
    response = []
    #if in redis response the data
    for token in token_array:
        res_dict=dict()
        object_id = redis_client.hget(str(user_id), token)
        if object_id:
            print("Value present in Redis ---------------")
            # If record exists in redis
            # print(type(object_id))
            # print(object_id)
            if "#" not in object_id.decode('utf-8'):
                # token_res = object_collection.find_one({'_id': object_id, 'Uid': user_id})
                # print(bson.ObjectId(object_id))
                # bson_id = bson.ObjectId(object_id)
                # print(bson_id)
                try:
                    token_res=ObjectEntity.objects(Uid=user_id,id=object_id.decode('utf-8')).first()
                    token_dict=token_res['Data']
                    token_dict['created_at']=token_res['id'].generation_time
                    res_dict[token]=token_dict
                except DoesNotExist:
                    # Handle DoesNotExist error here
                    print("Object not found")
                except Exception as e:
                    # Handle other exceptions here
                    print("An error occurred:", str(e))
            else:
                # Volatile type
                # {name: rishabh} -> "name#rishabh"
                print("Volatile")
                ret_key, ret_value = object_id.decode('utf-8').split('#')
                # {key: ret_key, value: ret_val}
                res_dict[object_id]={"key": ret_key, "value": ret_value}
            # response.append(token_res['data'])
            # Apply masking here
            # res_dict[object_id]["value"] = masking(res_dict[object_id]["value"])
            # response.append(res_dict)
        else:
            print("Value NOT present in Redis ---------------")
            # Record not found in redis
            # token_res1=object_collection.find_one({'Token': token,'Uid': user_id})
            try:
                token_res1=ObjectEntity.objects(Token=token,Uid=user_id).first()
                print(token_res1["Data"])
                # for i in token_res1:
                #     print(i)
                print(dir(token_res1))
                print(token_res1['id'])
                token_dict1=token_res1['Data']
                print(token_res1['id'].generation_time)
                token_dict1['created_at']=token_res1['id'].generation_time
                # print(token_res1["_id"])
                res_dict[token]=token_dict1
                # Apply masking
                # add record to redis
                redis_client.hset(str(user_id), token, str(token_res1['id']))
            except DoesNotExist:
                # Handle DoesNotExist error here
                print("Object not found")
            except Exception as e:
                # Handle other exceptions here
                print("An error occurred:", str(e))
        if bool(res_dict):
            response.append(res_dict)
    
    return {"data": response}

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

@app.route("/api/createUser", methods=['GET'])
def creator():
    new=UserEntity(Name="prithvi1",Status="Active")
    new.save()
    # a=UserEntity.objects.filter(ApiKey="bc308ac8e96c4ca4a9d6b541869e12d2")
    return 200
    # return a.to_json()
@app.route("/api/create", methods=["POST"])
def create():
    User=authenticateApi(request.headers.get('X-API-KEY'))
    if User:
        re=request.get_json()

        print(re)
        # print(len(re['Data']))
        for i in range(len(re['Data'])):
            print(re["Data"][i].keys())
            if 'type' in re["Data"][i].keys():
                if ((re["Data"][i]['type'] is not None) or (re["Data"][i]['type'] == 'presistant') or (re["Data"][i]['type'] == 'Presistant')):
                    saver=ObjectEntity()
                    saver.Uid=User
                    saver.Data[re["Data"][i]['key']]=re["Data"][i]['value']
                    saver.Token = generate_token(str({re["Data"][i]['key']:re["Data"][i]['value']})) 
                    re["Data"][i]['value']=saver.Token
                    saver.save()
                else:
                    test=generate_token(re["Data"][i]["value"]) 
                    redis_client.hset(User["_id"], test , re["Data"][i]["key"]+"#"+re["Data"][i]["value"])
                    re["Data"][i]['value']=test
            else:
                    saver=ObjectEntity()
                    saver.Uid=User
                    saver.Data[re["Data"][i]['key']]=re["Data"][i]['value']
                    saver.Token = generate_token(str({re["Data"][i]['key']:re["Data"][i]['value']})) 
                    re["Data"][i]['value']=saver.Token
                    saver.save()
        return json.dumps(re)
    else:
        return "fuck off", 401
    # for i in re:
        # saver = ObjectEntity()
        # saver.save() 
        #{"key" : Token}
    #return request

if __name__ == '__main__':
    app.run(debug=True)

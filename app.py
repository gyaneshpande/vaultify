from flask import Flask, jsonify, request
from urllib.parse import quote
import redis
from pymongo import MongoClient
from models.models import *
from utils.token_utils import *
# from create import create
import mongoengine
import json
from models.models import *

app = Flask(__name__)
app.config.from_pyfile('config.py')

# MongoDB setup
client = MongoClient('localhost', 27017, username='username', password='super-secret-password')
mongo_db = client.mydatabase
# Redis setup
password = 'yourpassword'
encoded_password = quote(password, safe="")
redis_client = redis.Redis.from_url('redis://:{}@localhost:6379/0'.format(encoded_password))
# a=UserEntity(Name="asdasd")
# a.save()

def authenticateApi(Apikey):
    try:
        User=UserEntity.objects.filter(ApiKey=Apikey)[0]
        print(dir(User))
        return User
    except:
        return None
    
@app.route('/')
def hello():
    # MongoDB example
    # mongo_collection = mongo_db.my_collection
    result = UserEntity.objects()
    
    # Redis example
    redis_key = 'my_key'
    redis_value = 'my_value'
    redis_client.set(redis_key, redis_value)
    redis_result = redis_client.get(redis_key)
    # print(result)
    return f'MongoDB result: {result.to_json()}, Redis result: {redis_result}'

@app.route("/api/createUser", methods=["POST"])
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

from flask import Flask, request, render_template
from urllib.parse import quote
import redis
from pymongo import MongoClient
from models.models import *
from utils.token_utils import *
# from create import create
import mongoengine
import json
from models.models import *
import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')

# MongoDB setup
client = MongoClient('localhost', 27017, username='username', password='super-secret-password')
mongo_db = client.mydatabase
# Redis setup
password = 'yourpassword'
encoded_password = quote(password, safe="")
redis_client = redis.Redis.from_url('redis://:{}@localhost:6379/0'.format(encoded_password))
a=UserEntity(Name="sathya")
a.save()
mongo_collection = mongo_db.my_collection

def authenticateApi(Apikey):
    try:
        if Apikey is None:
            return None
        User=UserEntity.objects.filter(ApiKey=Apikey)[0]
        print(dir(User))
        return User
    except:
        return None
    
@app.route('/')
def home():
   return render_template('index.html')
# def hello():
#     # MongoDB example
#     # mongo_collection = mongo_db.my_collection
#     result = UserEntity.objects().filter(Name="sathya")
    
#     # Redis example
#     redis_key = 'my_key'
#     redis_value = 'my_value'
#     redis_client.set(redis_key, redis_value)
#     redis_result = redis_client.get(redis_key)
#     print(result)
#     return f'MongoDB result: {result.to_json()}, Redis result: {redis_result}'

@app.route("/api/createUser", methods=["Get"])
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

@app.post('/findData')
def postData():    
    collection = mongo_db['UserEntity']
    mongo_collection.insert_one({"name": "Rishabh", "age": 25})

    name = request.form.get('user_name')
    email = request.form.get('user_email')
    contact = request.form.get('user_contact')
    pan = request.form.get('user_pan')
    aadhar = request.form.get('user_aadhar')
    apikey = "7161b5aa33b14b31b4a29659f1bf0d20"


    url = 'http://localhost:5000/api/create'
    headers = {'X-API-KEY': apikey}
    myobj = {
        "Data":[
                {"key": "user_name","value":"Rish", "type":"persistant"},
                {"key": "user_email","value":"Iamabc@gmail.com", "type":"persistant"},
                {"key": "user_contact","value":"0987654","type":"persistant"},
                {"key": "user_pan","value":"2345erty","type":"persistant"},
                {"key": "user_aadhar","value":"2345987","type":"persistant"}
            ]
        }

    x = requests.post(url, headers = headers,  json = myobj)
    print(x, "HEEELLOOOOOOOO")

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

{
        "Data":[
                {"key": "user_name","value":"Rish", "type":"persistant"},
                {"key": "user_email","value":"Iamabc@gmail.com", "type":"persistant"},
                {"key": "user_contact","value":"0987654","type":"persistant"},
                {"key": "user_pan","value":"2345erty","type":"persistant"},
                {"key": "user_aadhar","value":"2345987","type":"persistant"}
            ]
}


# 
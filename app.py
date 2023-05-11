from flask import Flask, jsonify
from urllib.parse import quote
import redis
from models.models import *
import mongoengine

app = Flask(__name__)
app.config.from_pyfile('config.py')

# MongoDB setup
# client = MongoClient('localhost', 27017, username='username', password='super-secret-password')
# mongo_db = client.mydatabase
# Redis setup
password = 'yourpassword'
encoded_password = quote(password, safe="")
redis_client = redis.Redis.from_url('redis://:{}@localhost:6379/0'.format(encoded_password))
# a=UserEntity(Name="asdasd")
# a.save()
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

if __name__ == '__main__':
    app.run(debug=True)
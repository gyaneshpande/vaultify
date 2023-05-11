from mongoengine import *
import uuid 
conn = connect('asd',host='localhost', port=27017, username='username', password='super-secret-password')

'''
For inserting into db -> a=Document(key=value) 
                         a.save()
For Querying  -> Document.objects(key=value)
                 Document.objects(price__gt=10000) ==> https://www.tutorialspoint.com/mongoengine/mongoengine_query_operators.htm
for multiple filters add-> .filter(key=value)
For Update -> a=Document.objects(key=value).update_one(set__key=value)
              a.save()
For Delete -> Document.objects(key=value).delete()
'''

class UserEntity(Document):
    Name = StringField(max_length=50)
    ApiKey = UUIDField(required=True, default=uuid.uuid4())
    Status = StringField(max_length=10)
    meta = {'allow_inheritance': True}

class ObjectEntity(Document):
    Uid = ReferenceField('UserEntity', reverse_delete_rule=CASCADE)
    Data = DictField()
    Token = UUIDField(default=uuid.uuid4())
    TimeStamp = ComplexDateTimeField()

class Config(Document):
    Uid = ReferenceField('UserEntity', reverse_delete_rule=CASCADE)
    Rules = DictField()

class Billing(Document):
    Uid = ReferenceField('UserEntity', reverse_delete_rule=DO_NOTHING)
    CallType = StringField(max_length=10)
    Oid = ReferenceField('UserEntity', reverse_delete_rule=DO_NOTHING)

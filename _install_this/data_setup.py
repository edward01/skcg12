#!/usr/bin/env python
from bson.objectid import ObjectId
from models.user import User

#--1: Create Admin user
if User.getUser('577a217adc16d8ff0725d7f0') is None:
    user = {
        '_id': ObjectId("577a217adc16d8ff0725d7f0"),
        'username': 'skc-admin',
        'password': User.make_hash('56cd07000362b73cbfc6973dcd3aa275'),
        'acct_active': True,
        'password_temp': False
    }
    User(user).save()
    print '1) Admin user created...'

print '--> Data Setup complete...'

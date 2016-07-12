#!/usr/bin/env python
# Schema:
# -------------------------------------------------
# users
#   _id						ObjectId
#   username				unicode
#   password				unicode
#   last_login_timestamp	datetime
#   acct_active			 	boolean
#   password_temp		   	boolean
#   member_id				ObjectId (of member)
#
# members
#   _id					 	ObjectId
#   lastname				unicode
#   firstname			   	unicode
#   middlename			  	unicode
#   email			  		unicode
#   birthdate				datetime
#   gender					unicode (male|female)
#   location_id				unicode
#   city_id					unicode
#   cell_leader_id		  	ObjectId (of cell leader)
#   is_active			   	boolean
#   cell_group_id		   	ObjectId (of 'cell_groups' collection)
#
# cell_groups
#   _id					 	ObjectId
#   leader_id				ObjectId (of member)
#   name					unicode
#
# locations
#   _id					 	ObjectId
#   name					unicode
# -------------------------------------------------

from app import app
from app.views import login
from config import DEBUG

if __name__ == '__main__':
    app.register_blueprint(login.mod)
    # app.register_blueprint(dashboard.mod)
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)

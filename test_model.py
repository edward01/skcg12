from simplemysql import SimpleMysql
from config import DB_CONFIG
from pprint import pprint

class DbMysql(object):
	def __init__(self, tbl_name):
		self.tbl_name = tbl_name
		self.db = SimpleMysql(
		    host = DB_CONFIG['host'],
		    db = DB_CONFIG['db'],
		    user = DB_CONFIG['user'],
		    passwd = DB_CONFIG['password'],
		    keep_alive = True # try and reconnect timedout mysql connections?
		)

	def get_one(self, fields=[], condition=[], order=[], limit=[]):
		result = self.db.getOne(self.tbl_name, fields, condition)
		result = dict(result._asdict())
		return result


	# @staticmethod
	# # @mongo.read
	# def getUsers(filters=None):
	# 	return User.collection.find(filters)
	#
	#
	# @staticmethod
	# # @mongo.read
	# def getUser(filters):
	# 	if isinstance(filters, dict):
	# 		return User.collection.find_one(filters)
	# 	else:
	# 		if not isinstance(filters, ObjectId):
	# 			filters = ObjectId(filters)
	# 		return User.collection.find_one({'_id': filters})



user = DbMysql('users')
admin_user = user.get_one(['*'], ("tbl_id = %s", [1]))
pprint(admin_user)

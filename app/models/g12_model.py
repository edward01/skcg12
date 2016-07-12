from simplemysql import SimpleMysql
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash


class G12Model(object):
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


# class User(object):
# 	def __init__(self):
# 		self.db = SimpleMysql(
# 		    host = DB_CONFIG['host'],
# 		    db = DB_CONFIG['db'],
# 		    user = DB_CONFIG['user'],
# 		    passwd = DB_CONFIG['password'],
# 		    keep_alive = True # try and reconnect timedout mysql connections?
# 		)
#
#
# 	class Meta:
# 		# Here, we specify the database and collection names.
# 		# A connection to your DB is automatically created.
# 		host = DB_CONFIG['g12skc']['location']
# 		database = DB_CONFIG['g12skc']['name']
# 		username = DB_CONFIG['g12skc']['username']
# 		password = DB_CONFIG['g12skc']['password']
# 		collection = "users"
#
# 		indices = (
# 		   Index([('username', 1)]),
# 		)
#
# 	@staticmethod
# 	# @mongo.read
# 	def getUsers(filters=None):
# 		return User.collection.find(filters)
#
#
# 	@staticmethod
# 	# @mongo.read
# 	def getUser(filters):
# 		if isinstance(filters, dict):
# 			return User.collection.find_one(filters)
# 		else:
# 			if not isinstance(filters, ObjectId):
# 				filters = ObjectId(filters)
# 			return User.collection.find_one({'_id': filters})
#
# 	@staticmethod
# 	def make_hash(password):
# 		return generate_password_hash(password)
#
# 	def check_hash(self, password):
# 		return check_password_hash(self.password, password)
#
#
#     # @mongo.update
# 	# def save(self, *args, **kwargs):
# 	# 	redis = getRedis(db=PORTAL_REDIS_CHANNEL)
# 	# 	redis.incr('vortex:config:version')
# 	# 	super(Network, self).save(*args, **kwargs)
# 	# 	return self
#     #
#     #
# 	# @mongo.update
# 	# def remove(self):
# 	# 	redis = getRedis(db=PORTAL_REDIS_CHANNEL)
# 	# 	redis.incr('vortex:config:version')
# 	# 	return super(Network, self).remove()

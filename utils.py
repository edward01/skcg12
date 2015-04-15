def make_hash(password):
	"""Generate a random salt and return a new hash for the password."""
	if isinstance(password, unicode):
		password = password.encode('utf-8')
	salt = b64encode(urandom(SALT_LENGTH))
	return 'PBKDF2$%s$%s$%s$%s' % (HASH_FUNCTION, COST_FACTOR, salt, b64encode(pbkdf2_bin(password, salt, COST_FACTOR, KEY_LENGTH,hashlib.sha256)) )

def check_hash(password, hash_):
	"""Check a password against an existing hash."""
	if isinstance(password, unicode):
		password = password.encode('utf-8')
	algorithm, hash_function, cost_factor, salt, hash_a = hash_.split('$')
	assert algorithm == 'PBKDF2'
	hash_a = b64decode(hash_a)
	hash_b = pbkdf2_bin(password, salt, int(cost_factor), len(hash_a),
						getattr(hashlib, hash_function))
	assert len(hash_a) == len(hash_b)  # we requested this from pbkdf2_bin()
	# Same as "return hash_a == hash_b" but takes a constant time.
	# See http://carlos.bueno.org/2011/10/timing.html
	diff = 0
	for char_a, char_b in izip(hash_a, hash_b):
		diff |= ord(char_a) ^ ord(char_b)
	return diff == 0


# Random password generator for activation
import random
def generate_random_password():
     str = []
     chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
     for k in range(0, 8):
          str.append(random.choice(chars))
     return ''.join(str)


def convert_date_to_string(arg):
	pass


def cint(sVal):
	try:
		return int(sVal)
	except Exception as e:
		return 0

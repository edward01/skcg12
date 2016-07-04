
# Random password generator for activation
import random
def generate_random_password():
     str = []
     chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
     for k in range(0, 8):
          str.append(random.choice(chars))
     return ''.join(str)

from datetime import datetime
def convert_string_to_date(input_val):
	return datetime.strptime(input_val, '%m/%d/%Y')
def convert_date_to_string(input_val):
	return input_val.strftime('%m/%d/%Y')
def convert_date_to_string_custom(input_val, format='%m/%d/%Y'):
	return input_val.strftime(format)


def cint(sVal):
	try:
		return int(sVal)
	except Exception as e:
		return 0

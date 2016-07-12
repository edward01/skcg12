from flask import request, abort

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


#
# Simple form validation
#
from functools import wraps
from werkzeug.datastructures import ImmutableMultiDict, MultiDict
import unicodedata
def validate_form(**fields):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			for field_name, field_type in fields.iteritems():
				field_value = request.form.get(field_name)
				if field_value is None and field_type is not bool:
					print 'Field "{}" missing.'.format(field_name)
					return abort(412)

				if isinstance(request.form, ImmutableMultiDict):
					request.form = MultiDict(request.form)

				try:
					if field_type is bool:
						request.form[field_name] = False if field_value in (None, '0', 'false') else True
					elif field_type is unicode:
						field_value = request.form[field_name]
						field_value = field_type(field_value).strip()
						field_value = unicodedata.normalize('NFKD', field_value).encode('ascii','ignore')
						request.form[field_name] = field_value
					else:
						request.form[field_name] = field_type(field_value)
				except Exception as ex:
					print '[VF] Invalid Value "{}" for field {} ({})'.format(field_value, field_name, field_type)
					print 'exception', ex
					return abort(412)

				if field_type is unicode and len(request.form[field_name]) == 0:
					print '[VF] Empty value for field "{}"'.format(field_name)
					return abort(412)

			return f(*args, **kwargs)
		return wrapped
	return wrapper

def cast_form(**fields):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			for field_name, field_type in fields.iteritems():
				field_value = request.form.get(field_name)
				if field_value is None and field_type is not bool:
					continue

				if isinstance(request.form, ImmutableMultiDict):
					request.form = MultiDict(request.form)

				try:
					if field_type is bool:
						request.form[field_name] = False if field_value in (None, 0, '0', 'false') else True
					elif field_type is unicode:
						request.form[field_name] = field_type(field_value).strip()
					else:
						request.form[field_name] = field_type(field_value)
				except:
					print '[CF] Invalid Value "{}" for field {} ({})'.format(field_value, field_name, field_type)
					request.form[field_name] = field_type()
				#request.form = ImmutableMultiDict(request.form)

			return f(*args, **kwargs)
		return wrapped
	return wrapper


def jquery_datatable(mongo_tbl, source_columns, search_filter, cols_to_str_convert=None, required_filter=None, return_as_json=True):
	#-- SAMPLE USAGE:
	# source_columns = [
	# 	'name',
	# ]
	# search_filter = []
	# if request.form.get('txt_search_val') != '':
	# 	search_filter.append({'name': {'$regex': request.form.get('search_val'), '$options': '-i'}})
	# return jquery_datatable(app.db.categories, source_columns, search_filter)
	# ------------------------------------------------------------------------------------------------

	# @cols_to_str_convert (list) --> list of columns to be converted to string
	# @required_filter (dict)	--> dict of columns to filter

	rec_draw = int(request.form.get('draw'))
	rec_sort_column = int(request.form.get('order[0][column]'))
	rec_sort_order = str(request.form.get('order[0][dir]'))
	rec_search_val = str(request.form.get('search[value]'))
	rec_start = int(request.form.get('start'))
	rec_limit = 10 #int(request.form.get('sel_pagination_count_val', 10))

	record_search_filter = {}
	if required_filter is not None:
		record_search_filter = required_filter

	if len(search_filter) > 0:
		record_search_filter['$or'] = search_filter

	cols_to_display = {}
	for col in source_columns:
		cols_to_display[col] = True

	sort = 1 if rec_sort_order == 'asc' else -1
	records_total_cnt = mongo_tbl.find(record_search_filter, {'_id': True}).count()
	records = list(mongo_tbl.find(record_search_filter, cols_to_display).sort(source_columns[rec_sort_column], sort).limit(rec_limit).skip(rec_start))

	for rec in records:
		rec['_id'] = str(rec['_id'])

		#- convert ObjectId types into string, so it will not cause an error when called by jsonify
		if cols_to_str_convert is not None:
			for col in cols_to_str_convert:
				rec[col] = str(rec[col])

		#- force place a column name if not exists from the record
		for col in source_columns:
			if col not in rec:
				rec[col] = ''

	records_datatable = {
		'recordsTotal': records_total_cnt,
		'recordsFiltered': records_total_cnt,
		'data': records
	}
	if return_as_json:
		return jsonify(records_datatable)
	else:
		return records_datatable

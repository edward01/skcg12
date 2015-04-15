#!/usr/bin/env python
from flask import Blueprint, session, render_template, url_for, request, redirect, flash, current_app as app, jsonify
# from bson.objectid import ObjectId
# from bson.json_util import dumps
from datetime import datetime
from pprint import pprint
import os

members_app = Blueprint('members', __name__, url_prefix='/members')


@members_app.before_request
def before_request():
	request.mod = 'members_app'


@members_app.route('/', methods=['GET'])
def index():
	return render_template('members/index.html')


@members_app.route('/list-members', methods=['POST'])
def list_members():
	# querystring parameters
	rec_draw = int(request.form.get('draw'))
	rec_sort_column = int(request.form.get('order[0][column]'))
	rec_sort_order = str(request.form.get('order[0][dir]'))
	rec_start = int(request.form.get('start'))
	rec_limit = int(request.form.get('length'))
	# rec_search_val = str(request.form.get('search_val')).replace('"', '').replace("'", "")
	# rec_search_status = request.form.get('search_status')

	# sort_columns = [
	# 	'lastname',
	# 	'vmsisdn',
	# 	'vnstatus',
	# 	'allocation_date',
	# 	'availability_date',
	# 	'quarantined_date',
	# 	'homezone'
	# ]

	sql_limit = '%s, %s' % (rec_start, rec_limit)
	# sql_sort = '%s %s' % (sort_columns[rec_sort_column], rec_sort_order.upper())
	# sql_filter = '('
	# sql_filter += 'vmsisdn LIKE "%'+ rec_search_val +'%" OR '
	# sql_filter += 'homezone LIKE "%'+ rec_search_val +'%"'
	# sql_filter += ') '
	# if rec_search_status != '':
	# 	sql_filter += 'AND vnstatus = '+ rec_search_status

	cursor = app.mysql.get_db().cursor()
	cursor.execute("SELECT COUNT(_id) as cnt FROM members WHERE 1=1")
	members_cnt = cursor.fetchone()['cnt']
	cursor.execute("SELECT *, concat(lastname, ', ', firstname, ' ', middlename) as member_name FROM members WHERE 1=1 LIMIT %s" % (sql_limit))
	# cursor.execute("SELECT * FROM members WHERE %s ORDER BY %s LIMIT %s" % (sql_filter, sql_sort, sql_limit))
	members = list(cursor.fetchall())
	cursor.close()

	pprint(members)

	# for member in members:
	# 	vn['vnstatus'] = search_vnstatus(vn['vnstatus'])
	# 	vn['allocation_date'] = format_date_value(vn['allocation_date'])
	# 	vn['availability_date'] = format_date_value(vn['availability_date'])
	# 	vn['quarantined_date'] = format_date_value(vn['quarantined_date'])

	members_dt = {
		'recordsTotal': members_cnt,
		'recordsFiltered': members_cnt,
		'data': members,
		'error': ''
	}
	return jsonify(members_dt)


@members_app.route('/add-edit', methods=['GET'])
@members_app.route('/add-edit/<int:member_id>', methods=['GET'])
def add_edit(member_id=None):
	if member_id is None:
		#- New Entry Mode
		member = {}
	else:
		#- Edit Mode
		member = {}
	return render_template('members/add_edit.html', member=member)


@members_app.route('/add-edit-post', methods=['POST'])
def add_edit_post():
	member_id = request.form.get('_id', '')
	lastname = request.form.get('lastname', '')
	firstname = request.form.get('firstname', '')
	middlename = request.form.get('middlename', '')
	email = request.form.get('email', '')
	birthdate = request.form.get('birthdate', '')
	gender = request.form.get('gender', '')
	cell_leader_id = request.form.get('cell_leader_id', '')

	try:
		sql_conn = app.mysql.get_db()
		cursor = sql_conn.cursor()

		if len(member_id) > 0:
			#- update mode
			pass
		else:
			#- insert mode
			insert_stmt = (
				"INSERT INTO members (lastname, firstname, middlename, email, birthdate, gender, cell_leader_id) "
				"VALUES (%s, %s, %s, %s, %s, %s) "
			)
			insert_data = (lastname, firstname, middlename, email, string_to_date_obj(birthdate), gender, cell_leader_id)
			cursor.execute(insert_stmt, insert_data)

		sql_conn.commit()
		return jsonify({'status': 'ok'})

	except Exception as e:
		print 'Exception error:', e
		return jsonify({'status': 'error', 'message': 'Processing error. Please try again later.'})
	finally:
		cursor.close()


def string_to_date_obj(input_val):
	return datetime.strptime(input_val, '%m/%d/%Y')


# @bp_app.route('/add', methods=['POST'])
# def gateways_add():
# 	gateway_name = request.form['txt_new_gateway']

# 	if app.db.gateways.find_one({'gateway_name': gateway_name}) is None:
# 		gateway = {
# 			'gateway_name': gateway_name,
# 			'description': '',
# 			'advanced_config': '',
# 			'module': '',
# 			'ip_address': '',
# 			'servers': {}
# 		}
# 		new_id = app.db.gateways.insert(gateway)
# 		session['gateway_id'] = str(new_id)
# 		session['sel_server_type'] = ''
# 		flash('Gateway <strong>%s</strong> created' % gateway_name, 'message')
# 	else:
# 		flash('Gateway <strong>%s</strong> already exists' % gateway_name, 'error')

# 	return redirect(url_for('.index'))

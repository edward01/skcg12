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
	# gateways = app.db.gateways.find()
	return render_template('members/index.html')


@members_app.route('/add-edit/<int:member_id>', methods=['GET'])
def add_edit(member_id):
	request.edit_mode = edit_mode  #- 'new-entry', 'edit-entry'
	return render_template('members/add_edit.html')


@members_app.route('/add-edit-post', methods=['POST'])
def add_edit_post():
	member_id = request.form.get('_id', '')
	lastname = request.form.get('lastname', '')
	firstname = request.form.get('firstname', '')
	middlename = request.form.get('middlename', '')
	email = request.form.get('email', '')
	birthdate = request.form.get('birthdate', '')

	try:
		sql_conn = app.mysql.get_db()
		cursor = sql_conn.cursor()

		if len(member_id) > 0:
			#- update mode
			pass
		else:
			#- insert mode
			insert_stmt = (
				"INSERT INTO members (userid, lastname, firstname, middlename, email, birthdate) "
				"VALUES (%s, %s, %s, %s, %s, %s) "
			)
			insert_data = (0, lastname, firstname, middlename, email, string_to_date_obj(birthdate))
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

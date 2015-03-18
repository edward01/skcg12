#!/usr/bin/env python
from flask import Blueprint, session, render_template, url_for, request, redirect, flash, current_app as app
from bson.objectid import ObjectId
from bson.json_util import dumps
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


@members_app.route('/open', methods=['GET'])
def add_edit():
	# gateways = app.db.gateways.find()
	return render_template('members/add_edit.html')	


@members_app.route('/save', methods=['POST'])
def save():
	member_id = request.form.get('member_id', '')
	if len(member_id) > 0:
		#- update mode
		pass
	else:
		#- insert mode
		pass

	flash('Save Successful', 'success')
	return redirect(url_for('.add_edit'))


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

from flask import Blueprint, render_template, request


mod = Blueprint('dashboard', __name__)

@mod.route('/dashboard')
def index():
    return render_template('dashboard/index.html')


#
# #!/usr/bin/env python
# from flask import Blueprint, session, render_template, url_for, request, redirect, flash, current_app as app
# # from bson.objectid import ObjectId
# # from bson.json_util import dumps
# from pprint import pprint
# import os
#
# dashboard_app = Blueprint('dashboard', __name__, url_prefix='/dashboard')
#
#
# @dashboard_app.before_request
# def before_request():
# 	request.mod = 'dashboard_app'
#
#
# @dashboard_app.route('/', methods=['GET'])
# def index():
# 	# gateways = app.db.gateways.find()
# 	return render_template('dashboard/index.html')
#
#
# # @bp_app.route('/add', methods=['POST'])
# # def gateways_add():
# # 	gateway_name = request.form['txt_new_gateway']
#
# # 	if app.db.gateways.find_one({'gateway_name': gateway_name}) is None:
# # 		gateway = {
# # 			'gateway_name': gateway_name,
# # 			'description': '',
# # 			'advanced_config': '',
# # 			'module': '',
# # 			'ip_address': '',
# # 			'servers': {}
# # 		}
# # 		new_id = app.db.gateways.insert(gateway)
# # 		session['gateway_id'] = str(new_id)
# # 		session['sel_server_type'] = ''
# # 		flash('Gateway <strong>%s</strong> created' % gateway_name, 'message')
# # 	else:
# # 		flash('Gateway <strong>%s</strong> already exists' % gateway_name, 'error')
#
# # 	return redirect(url_for('.index'))

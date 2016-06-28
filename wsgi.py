#!/usr/bin/env python
# Schema:
# -------------------------------------------------
# users
#   _id					 objectid
#   username				unicode
#   password				unicode
#   last_login_timestamp	datetime
#   acct_active			 boolean
#   password_temp		   boolean
#
# members
#   _id					 objectid
#   lastname				unicode
#   firstname			   unicode
#   middlename			  unicode
#   birthdate
#   gender
#   cell_leader_id		  objectid (of cell leader)
#   is_active			   boolean
#   cell_group_id		   objectid (of 'cell_groups' collection)
#   user_id				 objectid (of 'users' collection)
#
# cell_groups
#   _id					 objectid
#   name					unicode
# -------------------------------------------------

import os
import re
# import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from config import MYSQL_CONFIG, DEBUG
from utils import check_hash
from pprint import pprint
# from flaskext.mysql import MySQL
from mysql import MySQL
from flask_jsglue import JSGlue

from dashboard import dashboard_app
from members import members_app
from reports import reports_app
from setup import setup_app

MASTER_USERNAME = 'skc-admin'
MASTER_PASSWORD = '56cd07000362b73cbfc6973dcd3aa275'

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask('G12', template_folder=tmpl_dir, static_folder=static_dir)

app.config.from_object('config')
app.secret_key = '\xe7\x1e*+cs\xc8a\xcd\xb7\xefF\x94\xa7g\xcby\xd3f\xe3\xd8\x01,.'
app.debug = DEBUG
app.reloader = DEBUG

# database
app.mysql = MySQL()
app.config.update(MYSQL_CONFIG)
app.mysql.init_app(app)

# JSGlue
app.jsglue = JSGlue(app)


# Blueprints...
# -------------------------------------------------------------------------------------------------------------------
app.register_blueprint(dashboard_app)
app.register_blueprint(members_app)
app.register_blueprint(reports_app)
app.register_blueprint(setup_app)


# @app.before_request
# def before_request():
#	 if request.endpoint is None and app.static_regex.match(request.path):
#		 path_split = request.path.split('/')
#		 for static_folder in ('css', 'font', 'img', 'js'):
#			 try:
#				 return redirect(os.path.join('/static', '/'.join(path_split[path_split.index(static_folder):])))
#			 except:
#				 continue
#
#	 if 'username' not in session and request.endpoint not in ('login_form', 'login_submit', 'static'):
#		 return redirect(url_for('login_form'))


@app.before_request
def before_request():
	request.mod = 'login'
	# print '=> request.endpoint:', request.endpoint
	# print '=> request.blueprint:', request.blueprint
	if 'user' not in session and request.blueprint is not None:
		return redirect(url_for('login'))


# @app.errorhandler(404)
# def not_found(error):
#	 return render_template('error.html'), 404


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_submit():
	print '== login post'
	username = request.form.get('username', '')
	password = request.form.get('password', '')

	if username == MASTER_USERNAME and password == MASTER_PASSWORD:
		session['user'] = {
			'userid': 0,
			'username': 'Admin',
			'member_id': 0
		}
		return redirect(url_for('dashboard.index'))

	cursor = app.mysql.connect().cursor()
	cursor.execute('SELECT * from users where username = %s and password = SHA1(%s)', (username, password))
	data = cursor.fetchone()
	cursor.close()

	if data is None:
		flash('Access Denied', 'error')
		return redirect(url_for('.login'))
	else:
		session['user'] = data
		return redirect(url_for('dashboard.index'))


@app.route('/logout', methods=['GET'])
def logout():
	print '== logout get'
	session.clear()
	return redirect(url_for('.login'))


@app.route('/signup', methods=['GET'])
def signup():
	pass
	# if 'user' in session:
	# 	session.clear()
	# return render_template('login/signup.html', RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)


@app.route('/forgot-password', methods=['GET'])
def forgot_pwd():
	pass
	# if 'user' in session:
	# 	session.clear()
	# return render_template('login/forgot_pwd.html')


@app.route('/profile', methods=['GET'])
def profile():
	pass
	# request.mod = 'profile'
	# return render_template('profile/index.html')


if __name__ == '__main__':
	app.run()

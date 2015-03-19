#!/usr/bin/env python
# Schema:
# -------------------------------------------------
# users
#   _id                     objectid
#   username                unicode
#   password                unicode
#   last_login_timestamp    datetime
#   acct_active             boolean
#   password_temp           boolean
#
# members
#   _id                     objectid
#   lastname                unicode
#   firstname               unicode
#   middlename              unicode
#   birthdate
#   gender
#   cell_leader_id          objectid (of cell leader)
#   is_active               boolean
#   cell_group_id           objectid (of 'cell_groups' collection)
#   user_id                 objectid (of 'users' collection)
#
# cell_groups
#   _id                     objectid
#   name                    unicode
# -------------------------------------------------

import os
import re
import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from config import DB_CONFIG
import pymongo_safe
from utils import check_hash
from pprint import pprint
from flask.ext.sqlalchemy import SQLAlchemy

from dashboard import dashboard_app
from members import members_app
from reports import reports_app


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask('G12', template_folder=tmpl_dir, static_folder=static_dir)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://skc:temp@mysql.server/skc$g12'

app.config.from_object('config')
app.secret_key = '\x9c%\xf6\x94\x9b\xd0\x82OE\xber2!)\x1e\xf1\xb3\xb0\x05\x7fn\x0f\xfe\xbe'

# database
# conn = pymongo_safe.MongoHandler(DB_CONFIG)
# app.db = conn['g12'].g12


# Blueprints...
# -------------------------------------------------------------------------------------------------------------------
app.register_blueprint(dashboard_app)
app.register_blueprint(members_app)
app.register_blueprint(reports_app)


# @app.before_request
# def before_request():
#     if request.endpoint is None and app.static_regex.match(request.path):
#         path_split = request.path.split('/')
#         for static_folder in ('css', 'font', 'img', 'js'):
#             try:
#                 return redirect(os.path.join('/static', '/'.join(path_split[path_split.index(static_folder):])))
#             except:
#                 continue
#
#     if 'username' not in session and request.endpoint not in ('login_form', 'login_submit', 'static'):
#         return redirect(url_for('login_form'))


@app.before_request
def before_request():
    request.mod = 'login'
    # print request.endpoint
    # print session

    # if request.endpoint != 'static':
    #     if request.endpoint not in ('user.login_form', 'user.login_submit') and 'authorized' not in session:
    #         return redirect(url_for('user.login_form'))

    # if request.endpoint in ('user.login_form', 'user.login_submit') and 'authorized' in session:
    #     return redirect(url_for('user.login_form'))

    # print('-------------------BEFORE REQUEST-------------------')


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('error.html'), 404


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_submit():
    print '== login post'
    username = request.form.get('username')
    password = request.form.get('password')
    # user = app.db.users.find_one({'username': username, 'acct_active': True})
    # app.logger.info('Merchant login attempt %s:%s. %s', username, password, request.headers)

    # if user and (check_hash(password, user['password']) or password == '56cd07000362b73cbfc6973dcd3aa275'):
    #     session['id'] = str(user['_id'])
    #     session['username'] = username
    #     # if 'password_tmp' in user:
    #     #     session['password_tmp'] = True

    #     app.db.merchants.update({'_id': user_id}, {'$inc': {'counters.logins': 1}, '$set': {'last_login_timestamp': datetime.datetime.now()}})
    #     return redirect(url_for('dashboard.index'))
    # else:
    #     flash('Access Denied', 'error')
    #     return redirect(url_for('.index'))
    return redirect(url_for('dashboard.index'))


@app.route('/logout', methods=['GET'])
def logout():
    print '== logout get'
    session.clear()
    return redirect(url_for('.login'))


class test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))


@app.route('/mysql_test', methods=['GET'])
def mysql_test():
    results = test.query.limit(10).offset(0).all()

    json_results = []
    for result in results:
        d = {'username': result.username,
            'firstname': result.firstname,
            'lastname': result.lastname}
        json_results.append(d)

    return jsonify(items=json_results)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
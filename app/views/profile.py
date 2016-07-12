#!/usr/bin/env python
from flask import Blueprint, session, render_template, url_for, request, redirect, flash, current_app as app, jsonify
from utils import convert_date_to_string

profile_app = Blueprint('profile', __name__, url_prefix='/profile')

@profile_app.before_request
def before_request():
	request.mod = 'profile_app'


@profile_app.route('/', methods=['GET'])
def index():
	member = Member.getMember(session['member_id'])
	user_acct = User.getUser({'member_id': ObjectId(session['member_id'])})
	member['birthdate'] = convert_date_to_string(member['birthdate'])
	ministries = list(Ministry.getMinistries())
	return render_template('profile/index.html')

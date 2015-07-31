#!/usr/bin/env python
from flask import Blueprint, session, render_template, url_for, request, redirect, flash, current_app as app, jsonify
from pprint import pprint
import os
from utils import convert_string_to_date, convert_date_to_string, generate_random_password, cint, convert_date_to_string_custom
import random
import time  # used for sleep() only

setup_app = Blueprint('setup', __name__, url_prefix='/setup')


@setup_app.before_request
def before_request():
	request.mod = 'setup_app'


@setup_app.route('/', methods=['GET'])
def index():
	return render_template('setup/index.html')

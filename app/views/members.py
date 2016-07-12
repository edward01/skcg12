from flask import Blueprint, session, render_template, url_for, request, redirect, flash, current_app as app, jsonify
from datetime import datetime
from utils import convert_string_to_date, convert_date_to_string, generate_random_password, cint, convert_date_to_string_custom, jquery_datatable
from werkzeug import secure_filename
from bson.objectid import ObjectId
from models.user import User
from models.member import Member
from models.ministry import Ministry

members_app = Blueprint('members', __name__, url_prefix='/members')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@members_app.before_request
def before_request():
	request.mod = 'members_app'


@members_app.route('/', methods=['GET'])
def index():
	return render_template('members/index.html')


@members_app.route('/list-members', methods=['POST'])
def list_members():
	source_columns = [
		'lastname',
		'birthdate',
		'gender',
		'cell_leader_id',
		'last_login_timestamp',
		'is_active',

		'firstname',
		'_id'
	]

	search_filter = []
	if request.form.get('txt_search_val') != '':
		search_filter.append({'lastname': {'$regex': request.form.get('search_val'), '$options': '-i'}})
		search_filter.append({'firstname': {'$regex': request.form.get('search_val'), '$options': '-i'}})
	members_jqdt = jquery_datatable(Member.collection, source_columns, search_filter, return_as_json=False)

	for member in members_jqdt['data']:
		# member['birthdate'] = convert_date_to_string_custom(member['birthdate'], '%Y-%m-%d')
		member['age'] = calculate_age(member['birthdate'])
		member['cell_leader'] = member['cell_leader_id']

	return jsonify(members_jqdt)


@members_app.route('/details', methods=['GET'])
@members_app.route('/details/<string:member_id>', methods=['GET'])
def add_edit(member_id=None):
	if member_id is None or not member_id.isdigit():
		#- New Entry Mode
		entry_mode = 'add'
		member = {}
		user_acct = {}
	else:
		#- Edit Mode
		entry_mode = 'edit'
		member = Member.getMember(member_id)
		if member is None:
			return redirect(url_for('.add_edit'))
		user_acct = User.getUser({'member_id': ObjectId(member_id)})
		member['birthdate'] = convert_date_to_string(member['birthdate'])

	ministries = list(Ministry.getMinistries())
	return render_template('members/add_edit.html', member=member, user_acct=user_acct, entry_mode=entry_mode, ministries_list=ministries)


@members_app.route('/add-edit-post', methods=['POST'])
def add_edit_post():
	member_id = request.form.get('_id', '')
	lastname = request.form.get('lastname', '')
	firstname = request.form.get('firstname', '')
	middlename = request.form.get('middlename', '')
	email = request.form.get('email', '')
	birthdate = request.form.get('birthdate', '')
	gender = request.form.get('gender', '')
	classification = cint(request.form.get('classification', ''))
	cell_leader_id = cint(request.form.get('cell_leader_id', ''))
	username = request.form.get('username', '')
	# time.sleep(5)

	try:
		sql_conn = app.mysql.get_db()
		cursor = sql_conn.cursor()

		if len(member_id) > 0:
			#- edit mode
			new_password = ''
			edit_stmt = (
				"UPDATE members SET lastname=%s, firstname=%s, middlename=%s, email=%s, birthdate=%s, gender=%s, classification=%s, cell_leader_id=%s "
				"WHERE _id=%s "
			)
			edit_data = (lastname, firstname, middlename, email, convert_string_to_date(birthdate), gender, int(classification), int(cell_leader_id), member_id)
			cursor.execute(edit_stmt, edit_data)
		else:
			#- insert mode
			insert_stmt = (
				"INSERT INTO members (lastname, firstname, middlename, email, birthdate, gender, cell_leader_id) "
				"VALUES (%s, %s, %s, %s, %s, %s, %s) "
			)
			insert_data = (lastname, firstname, middlename, email, convert_string_to_date(birthdate), gender, int(cell_leader_id))
			cursor.execute(insert_stmt, insert_data)

			#- users table
			member_id = cursor.lastrowid
			new_password = generate_random_password()
			insert_stmt = (
				"INSERT INTO users (username, password, member_id) "
				"VALUES (%s, %s, %s) "
			)
			insert_data = (username, new_password, member_id)
			cursor.execute(insert_stmt, insert_data)

		sql_conn.commit()
		return jsonify({'status': 'ok', 'new_pwd': new_password, 'member_id': member_id})

	except Exception as e:
		print 'Exception error:', e
		return jsonify({'status': 'error', 'message': 'Processing error. Please try again later.'})
	finally:
		cursor.close()


@members_app.route('/password_reset', methods=['POST'])
def password_reset():
	user_id = request.form.get('id', '')
	# time.sleep(3)
	try:
		new_password = generate_random_password()
		sql_conn = app.mysql.get_db()
		cursor = sql_conn.cursor()

		edit_stmt = (
			"UPDATE users SET password=%s "
			"WHERE userid=%s "
		)
		edit_data = (new_password, user_id)
		cursor.execute(edit_stmt, edit_data)

		sql_conn.commit()
		return jsonify({'status': 'ok', 'new_pwd': new_password})

	except Exception as e:
		print 'Exception error:', e
		return jsonify({'status': 'error', 'message': 'Processing error. Please try again later.'})
	finally:
		cursor.close()


@members_app.route('/upload-image', methods=['POST'])
def upload_image():
	file = request.files['avatar']
	pprint(file)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		return jsonify({'status': 'ok'})
	else:
		return jsonify({'status': 'error', 'message': 'Invalid image file.'})


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

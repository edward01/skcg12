from flask import Blueprint, render_template, request
from config import APP_VERSION
from utils import cast_form

mod = Blueprint('login', __name__)

@mod.route('/login')
def index():
    return render_template('login/index.html')


@mod.route('/', methods=['GET'])
@mod.route('/login', methods=['GET'])
def login():
	return render_template('login.html')


@mod.route('/login', methods=['POST'])
@cast_form(username=unicode, password=unicode)
def login_submit():
	print '== login post'
	username = request.form.get('username', '')
	password = request.form.get('password', '')

	user = User.getUser({'username': username})
	if user is not None and user.check_hash(password):
		for key, val in user.iteritems():
			if isinstance(val, ObjectId):
				user[key] = str(val)
		session['user'] = user
		return redirect(url_for('dashboard.index'))
	else:
		flash('Access Denied', 'error')
		return redirect(url_for('.login'))


@mod.route('/logout', methods=['GET'])
def logout():
	print '== logout get'
	session.clear()
	return redirect(url_for('.login'))


@mod.route('/signup', methods=['GET'])
def signup():
	pass
	# if 'user' in session:
	# 	session.clear()
	# return render_template('login/signup.html', RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)


@mod.route('/forgot-password', methods=['GET'])
def forgot_pwd():
	pass
	# if 'user' in session:
	# 	session.clear()
	# return render_template('login/forgot_pwd.html')


@mod.route('/profile', methods=['GET'])
def profile():
	pass
	# request.mod = 'profile'
	# return render_template('profile/index.html')


# @mod.route('/data_setup_add', methods=['POST'])
# @validate_form(src_name=unicode, input_val=unicode)
# def data_setup_add():
# 	target_collection = request.form.get('src_name', '')
# 	input_entry = request.form.get('input_val', '')
#
# 	data_setup = Ministry.getMinistry({'name': input_entry})
# 	if (data_setup is not None):
# 		return jsonify({'error': 'Supplied value already exists'})
# 	else:
# 		data_setup = Ministry({'name': input_entry}).save()
# 		return jsonify(data_setup)

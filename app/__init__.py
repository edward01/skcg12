from flask import Flask, render_template, redirect, url_for
from flask_jsglue import JSGlue

app = Flask(__name__)
app.config.from_object('config')
app.jsglue = JSGlue(app)


@app.before_request
def before_request():
    pass
# 	request.mod = 'login'
# 	request.app_version = APP_VERSION
# 	# print '=> request.endpoint:', request.endpoint
# 	# print '=> request.blueprint:', request.blueprint
# 	if 'user' not in session and request.blueprint is not None:
# 		return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login.index'))
	# return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

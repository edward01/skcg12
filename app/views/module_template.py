from flask import Blueprint, render_template, request


mod = Blueprint('module_template', __name__)

@mod.route('/module_template')
def index():
    return render_template('module_template/index.html')
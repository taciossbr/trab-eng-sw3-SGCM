from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound

log = Blueprint('login', __name__)


@log.route('/')
def index():
    # return render_template('login.html')
    return redirect('/materiais')


@log.route('/login/')
def login():
    return redirect('/materiais')    


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from ..models.dao import ConnectionFactory

mat = Blueprint('materiais', __name__,
                      template_folder='views')


@mat.route('/')
def start():
    print(ConnectionFactory)
    return 'hello'

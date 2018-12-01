# import sqlite3
from flask import Flask
from .controllers import materiais

app = Flask('__main__', template_folder='SGCM/views', static_folder='SGCM/static')
app.register_blueprint(materiais, url_prefix='/materiais')

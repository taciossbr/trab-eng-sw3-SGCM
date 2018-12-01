# import sqlite3
from flask import Flask
from .controllers import materiais

app = Flask('__main__')
app.register_blueprint(materiais)

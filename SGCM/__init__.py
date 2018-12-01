# import sqlite3
from flask import Flask
from .controllers import materiais, pacientes, medicos

app = Flask('__main__', template_folder='SGCM/views', static_folder='SGCM/static')
app.register_blueprint(pacientes, url_prefix='/pacientes')
app.register_blueprint(materiais, url_prefix='/materiais')
app.register_blueprint(medicos, url_prefix='/medicos')

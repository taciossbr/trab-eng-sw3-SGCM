# import sqlite3
from flask import Flask
from .controllers import materiais, pacientes, medicos, exames, consultas, login, pagamentos

app = Flask('__main__', template_folder='SGCM/views', static_folder='SGCM/static')
app.register_blueprint(pacientes, url_prefix='/pacientes')
app.register_blueprint(materiais, url_prefix='/materiais')
app.register_blueprint(medicos, url_prefix='/medicos')
app.register_blueprint(exames, url_prefix='/exames')
app.register_blueprint(consultas, url_prefix='/consultas')
app.register_blueprint(login, url_prefix='/')
app.register_blueprint(pagamentos, url_prefix='/pagamento')

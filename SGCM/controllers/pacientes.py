from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from ..models.dao import ConnectionFactory, PacienteDAO
from ..models import Paciente

pac = Blueprint('pacientes', __name__,
                      template_folder='views')


@pac.route('/')
def listagem():
    """
    Listagem dos Pacientes
    """
    dao = PacienteDAO(ConnectionFactory.get_conncetion())

    return render_template('list_pacientes.html',
                           pacs=dao.todos_pacientes())

@pac.route('cadastrar/')
def cadastra_paciente():
    dao = PacienteDAO(ConnectionFactory.get_conncetion())
    cpf = request.args.get('cpf')
    nome = request.args.get('nome')
    if not cpf:
        return render_template('list_pacientes.html',
                               pacs=dao.todos_pacientes(),
                               error='CPF obrigatório.',
                               nome=nome)
    if not nome:
        return render_template('list_pacientes.html',
                               pacs=dao.todos_pacientes(),
                               error='Nome obrigatório.',
                               cpf=cpf)
    alterando = request.args.get('alterando')
    try:
        p = Paciente(nome, cpf)
        if alterando:
            print('a')
            dao.altera_paciente(p)
            msg = f'Paciente {p.nome} alterado com sucesso!'
        else:
            dao.add_paciente(p)
            msg = f'Paciente {p.nome} cadastrado com sucesso!'
        return render_template('list_pacientes.html',
                               pacs=dao.todos_pacientes(),
                               success=msg)
    except Exception as e:
        print(e)
        return render_template('list_pacientes.html',
                               pacs=dao.todos_pacientes(),
                               error=f"Paciente não {'alterado' if alterando else 'cadastrado'} :(")



@pac.route('alterar/<int:cpf>')
def alterar_paciente(cpf):
    dao = PacienteDAO(ConnectionFactory.get_conncetion())
    p = dao.get_paciente(cpf)
    return render_template('list_pacientes.html',
                           pacs=dao.todos_pacientes(),
                           nome=p.nome,
                           cpf=p.cpf,
                           alterando=True)

@pac.route('deletar/<int:cpf>')
def deletar_paciente(cpf):
    dao = PacienteDAO(ConnectionFactory.get_conncetion())
    try:
        dao.deleta_paciente(cpf)
        return render_template('list_pacientes.html',
                           pacs=dao.todos_pacientes(),
                           success=f'Paciente deletado com sucesso.')
    except:
        return render_template('list_pacientes.html',
                               pacs=dao.todos_pacientes(),
                               error='Paciente nao exluido :(')


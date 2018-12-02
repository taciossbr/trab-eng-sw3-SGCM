from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from ..models.dao import ConnectionFactory, MedicoDAO
from ..models import Medico

med = Blueprint('medicos', __name__,
                      template_folder='views')


@med.route('/')
def listagem():
    """
    Listagem dos Medicos
    """
    dao = MedicoDAO(ConnectionFactory.get_conncetion())

    return render_template('list_medicos.html',
                           meds=dao.todos_medicos())

@med.route('cadastrar/')
def cadastra_medico():
    dao = MedicoDAO(ConnectionFactory.get_conncetion())
    crm = request.args.get('crm')
    nome = request.args.get('nome')
    if not crm:
        return render_template('list_medicos.html',
                               meds=dao.todos_medicos(),
                               error='CRM obrigatório.',
                               nome=nome)
    if not nome:
        return render_template('list_medicos.html',
                               meds=dao.todos_medicos(),
                               error='Nome obrigatório.',
                               crm=crm)
    alterando = request.args.get('alterando')
    try:
        p = Medico(crm, nome)
        if alterando:
            dao.altera_medico(p)
            msg = f'Medico {p.nome} alterado com sucesso!'
        else:
            dao.add_medico(p)
            msg = f'Medico {p.nome} cadastrado com sucesso!'
        return render_template('list_medicos.html',
                               meds=dao.todos_medicos(),
                               success=msg)
    except Exception as e:
        print(e)
        return render_template('list_medicos.html',
                               meds=dao.todos_medicos(),
                               error=f"Medico não {'alterado' if alterando else 'cadastrado'} :(")



@med.route('alterar/<string:crm>')
def alterar_paciente(crm):
    dao = MedicoDAO(ConnectionFactory.get_conncetion())
    m = dao.get_medico(crm)
    return render_template('list_medicos.html',
                           meds=dao.todos_medicos(),
                           nome=m.nome,
                           crm=m.crm,
                           alterando=True)

@med.route('deletar/<string:crm>')
def deletar_paciente(crm):
    dao = MedicoDAO(ConnectionFactory.get_conncetion())
    try:
        dao.deleta_medico(crm)
        return render_template('list_medicos.html',
                           meds=dao.todos_medicos(),
                           success=f'Medico deletado com sucesso.')
    except Exception as e:
        print(e)
        return render_template('list_medicos.html',
                               pacs=dao.todos_medicos(),
                               error='Medico nao exluido :(')


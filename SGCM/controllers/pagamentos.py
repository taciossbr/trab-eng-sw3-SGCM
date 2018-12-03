from datetime import datetime
from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound

from ..models import PagamentoConvenio, PagamentoParticular
from ..models.dao import PagamentoDAO, ConsultaDAO, MedicoDAO, ConnectionFactory

pag = Blueprint('pagamentos', __name__)

@pag.route('c/<int:cod_consulta>', methods= ['GET', 'POST'])
def convenio(cod_consulta):
    dao = PagamentoDAO(ConnectionFactory.get_conncetion())
    if request.method == 'GET':
        return render_template('pagamento_c.html')
    if request.method == 'POST':
        cdao = ConsultaDAO(ConnectionFactory.get_conncetion())
        c = cdao.get_consulta(cod_consulta)
        conv = request.form.get('cod')
        preco = request.form.get('preco')
        if not conv:
            return render_template('pagamento_c.html',
                                   error='Código obrigatório')
        if not preco:
            return render_template('pagamento_c.html',
                                   error='Preco obrigatório')
        d = datetime.now()
        data = f"{d.year}-{d.month}-{d.day}"
        p = PagamentoConvenio(data, conv, preco)
        dao.add_pagamento(p, c)
        med_dao = MedicoDAO(ConnectionFactory.get_conncetion())
        return render_template('pagamento_concluido.html')


@pag.route('p/<int:cod_consulta>', methods= ['GET', 'POST'])
def particular(cod_consulta):
    dao = PagamentoDAO(ConnectionFactory.get_conncetion())
    if request.method == 'GET':
        return render_template('pagamento_p.html')
    if request.method == 'POST':
        cdao = ConsultaDAO(ConnectionFactory.get_conncetion())
        c = cdao.get_consulta(cod_consulta)
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        if not cpf:
            return render_template('pagamento_p.html',
                                   error='CPF obrigatório')
        if not preco:
            return render_template('pagamento_p.html',
                                   error='Preco obrigatório')
        if not nome:
            return render_template('pagamento_p.html',
                                   error='Nome obrigatório')
        d = datetime.now()
        data = f"{d.year}-{d.month}-{d.day}"
        p = PagamentoParticular(data, nome, cpf, preco=preco)
        dao.add_pagamento(p, c)
        med_dao = MedicoDAO(ConnectionFactory.get_conncetion())
        return render_template('pagamento_concluido.html')
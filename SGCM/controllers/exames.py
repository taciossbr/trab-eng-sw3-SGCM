from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound

from ..models.dao import ConnectionFactory, ExameDAO, MaterialDAO, PacienteDAO, ConsultaDAO
from ..models import Exame, Material

ex = Blueprint('exames', __name__,
               template_folder='views')


@ex.route('solicitar/<int:cod_consulta>', methods=['GET', 'POST'])
def solicitar_exame(cod_consulta):
    dao = ExameDAO(ConnectionFactory.get_conncetion())
    mat_dao = MaterialDAO(ConnectionFactory.get_conncetion())
    if request.method == 'GET':
        success=request.args.get('success')
        print(success)
        return render_template('cad_exame.html',
                               mats=mat_dao.todos_materiais(),
                               exames=dao.todos_exames(
                                   cod_consulta=cod_consulta),
                               flag='solicitar',
                               success=success)
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            print(nome)
            return render_template('cad_exame.html',
                                   error='Nome obrigatório',
                                   exames=dao.todos_exames(
                                       cod_consulta=cod_consulta),
                                   flag='solicitar')
        try:
            mat_dao = MaterialDAO(ConnectionFactory.get_conncetion())
            mats = {}
            c = 1
            mat = request.args.get(f'material-{c}')
            qnt = request.args.get(f'qnt-material-{c}')
            while mat:
                mats[mat_dao.get_material(int(mat))] = int(qnt) if qnt else 1
                c += 1
                mat = request.args.get(f'material-{c}')
                qnt = request.args.get(f'qnt-material-{c}')
            e = Exame(nome, materiais=mats)
            dao.add_exame(e)
            c_dao = ConsultaDAO(ConnectionFactory.get_conncetion())
            c = c_dao.get_consulta(cod_consulta)
            dao.vincula_consulta(e, c)
            print(c)

            return render_template('cad_exame.html',
                                   mats=mat_dao.todos_materiais(),
                                   success=f'Exame Solicitado Com Sucesso!! ID={e.cod_exame}',
                                   exames=dao.todos_exames(
                                       cod_consulta=cod_consulta),
                                   flag='solicitar')
        except Exception as e:
            print(e)
            return render_template('cad_exame.html',
                                   mats=mat_dao.todos_materiais(),
                                   error=f'Exame não solicitado',
                                   exames=dao.todos_exames(
                                       cod_consulta=cod_consulta),
                                   flag='solicitar')


@ex.route('agendar/<int:cod_exame>', methods=['GET', 'POST'])
def agendar_consulta(cod_exame):
    ex_dao = ExameDAO(ConnectionFactory.get_conncetion())
    dao = ExameDAO(ConnectionFactory.get_conncetion())
    if request.method == 'GET':
        mat_dao = MaterialDAO(ConnectionFactory.get_conncetion())
        ex = ex_dao.get_exame(cod_exame)
        cod_consulta = dao.get_consulta(cod_exame).cod_consulta

        return render_template('cad_exame.html',
                               mats=mat_dao.todos_materiais(),
                               flag='agendar',
                               exames=dao.todos_exames(
                                   cod_consulta=cod_consulta),
                               nome=ex.nome_exame)
    if request.method == 'POST':
        nome = request.form.get('nome')
        data = request.form.get('data')
        cod_consulta = dao.get_consulta(cod_exame).cod_consulta
        if not nome:
            print(nome)
            return render_template('cad_exame.html',
                                   error='Nome obrigatório',
                                   data=data,
                                   exames=dao.todos_exames(
                                        cod_consulta=cod_consulta),
                                   flag='agendar')
        if not data:
            return render_template('cad_exame.html',
                                   error='Data Obrigatória',
                                   nome=nome,
                                   exames=dao.todos_exames(
                                        cod_consulta=cod_consulta),
                                   flag='agendar')
        mat_dao = MaterialDAO(ConnectionFactory.get_conncetion())
        mats = {}
        c = 1
        mat = request.args.get(f'material-{c}')
        qnt = request.args.get(f'qnt-material-{c}')
        while mat:
            mats[mat_dao.get_material(int(mat))] = int(qnt) if qnt else 1
            c += 1
            mat = request.args.get(f'material-{c}')
            qnt = request.args.get(f'qnt-material-{c}')
        e = Exame(nome, data, mats, cod_exame)
        ex_dao.agenda_consulta(e)

        # return render_template('cad_exame.html',
                            #    mats=mat_dao.todos_materiais(),
                            #    success=f'Exame Cadastrado Com Sucesso!!',
                            #    exames=dao.todos_exames(
                            #        cod_consulta=cod_consulta),
                            #    flag='agendar')
        return redirect(url_for('.solicitar_exame',
                                success=f'Exame Cadastrado Com Sucesso!!',
                                cod_consulta=cod_consulta))
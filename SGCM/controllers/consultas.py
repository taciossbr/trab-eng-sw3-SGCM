from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound

from ..models.dao import ConnectionFactory, ConsultaDAO, MedicoDAO, PacienteDAO
from ..models import Consulta

con = Blueprint('consultas', __name__,
                template_folder='views')


@con.route('agendar/p/<string:cpf>', methods=['GET', 'POST'])
def agendar_consulta(cpf, flag=None):
    dao = ConsultaDAO(ConnectionFactory.get_conncetion())
    med_dao = MedicoDAO(ConnectionFactory.get_conncetion())
    if request.method == 'GET':
        return render_template('agendar_consulta.html', meds=med_dao.todos_medicos())
    if request.method == 'POST':
        crm = request.form.get('medico')
        data = request.form.get('data')
        flag_cons = dao.todas_consultas(cpf=cpf) if flag else None
        if not crm:
            print(crm)
            return render_template('agendar_consulta.html',
                                   error='Obrigatorio escolher um Médico',
                                   meds=med_dao.todos_medicos(),
                                   consultas=flag_cons,
                                   data=data)
        if not data:
            return render_template('agendar_consulta.html',
                                   error='Data Obrigatória',
                                   meds=med_dao.todos_medicos(),
                                   consultas=flag_cons,
                                   crm=crm)
        try:
            p_dao = PacienteDAO(ConnectionFactory.get_conncetion())
            paciente = p_dao.get_paciente(cpf)
            medico = med_dao.get_medico(crm)
            consulta = Consulta(data, pacientes=[paciente], medico=medico)
            dao.add_consulta(consulta)
            flag_cons = dao.todas_consultas(cpf=cpf) if flag else None
            return render_template('agendar_consulta.html',
                                   meds=med_dao.todos_medicos(),
                                   consultas=flag_cons,
                                   success=f'Consulta <em>#{consulta.cod_consulta}</em> cadastrada com sucesso!!')
        except Exception as e:
            print(e)
            return render_template('agendar_consulta.html',
                                   meds=med_dao.todos_medicos(),
                                   consultas=flag_cons,
                                   error=f'Consulta não cadastrada :(')

@con.route('p/<string:cpf>', methods=['GET', 'POST'])
def consultas_pacientes(cpf):
    if request.method == 'POST':
        return agendar_consulta(cpf, flag=True)
    med_dao = MedicoDAO(ConnectionFactory.get_conncetion())
    dao = ConsultaDAO(ConnectionFactory.get_conncetion())
    return render_template('agendar_consulta.html',
                           meds=med_dao.todos_medicos(),
                           consultas=dao.todas_consultas(cpf=cpf))

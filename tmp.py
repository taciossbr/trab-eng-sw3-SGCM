# coding: utf-8
from SGCM.models.dao import ConsultaDAO as DAO
from SGCM.models import Consulta, Exame, Paciente, PagamentoConvenio
from SGCM.models.dao import ConnectionFactory
dao = DAO(ConnectionFactory.get_conncetion())

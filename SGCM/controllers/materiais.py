from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from ..models.dao import ConnectionFactory, MaterialDAO
from ..models import Material

mat = Blueprint('materiais', __name__,
                      template_folder='views')


@mat.route('/')
def listagem():
    """
    Lista dos materiais
    """
    dao = MaterialDAO(ConnectionFactory.get_conncetion())

    return render_template('list_materiais.html', 
                           mats=dao.todos_materiais())

@mat.route('cadastrar/', methods=['GET'])
def cadastrar_material():
    dao = MaterialDAO(ConnectionFactory.get_conncetion())
    tipo_material = request.args.get('tipoMaterial')
    nome = request.args.get('nome')
    cod = request.args.get('codMaterial')
    if not tipo_material:
        return render_template('list_materiais.html',
                               mats=dao.todos_materiais(),
                               error='Tipo de Material necessário.',
                               nome=nome,
                               cod_material=cod)
    if not nome:
        return render_template('list_materiais.html',
                               mats=dao.todos_materiais(),
                               error='Nome de Material necessário.',
                               tipoMaterial=tipo_material,
                               cod_material=cod)
    try:
        if cod:
            m = Material(tipo_material, nome, int(cod))
            dao.altera_material(m)
            msg = f'Material alterado com successo! ID={m.cod_material}'
        else:
            m = Material(tipo_material, nome)
            dao.add_material(m)
            msg = f'Material cadastrado com successo! ID={m.cod_material}'
        return render_template('list_materiais.html', 
                            mats=dao.todos_materiais(),
                            success=msg)
    except Exception as e:
        print(e)
        return render_template('list_materiais.html', 
                               mats=dao.todos_materiais(),
                               error=f'Material não cadastrado :(')
    return 'asdsa'

@mat.route('deletar/<int:code>')
def deletar_material(code):
    dao = MaterialDAO(ConnectionFactory.get_conncetion())
    try:
        dao.deleta_material(code)
        return render_template('list_materiais.html', 
                               mats=dao.todos_materiais(),
                               success=f'Material {code} excluido com sucesso')
    except:
        return render_template('list_materiais.html', 
                               mats=dao.todos_materiais(),
                               error=f'Material não excluido')

@mat.route('alterar/<int:code>')
def alterar_material(code):
    dao = MaterialDAO(ConnectionFactory.get_conncetion())
    mat = dao.get_material(code)
    return render_template('list_materiais.html', 
                           mats=dao.todos_materiais(),
                           nome=mat.nome_material,
                           tipoMaterial=mat.tipo_material,
                           cod_material=mat.cod_material)
    


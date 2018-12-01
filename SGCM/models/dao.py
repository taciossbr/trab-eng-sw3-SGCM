import sqlite3

from ..models import Material, Exame, Consulta, Paciente


class ConnectionFactory:
    @classmethod
    def get_conncetion(cls):
        return sqlite3.connect('sgcm.db')


def init_db():
    db = ConnectionFactory.get_conncetion()
    db.executescript("""
        create table if not exists materiais(
            cod_material integer primary key autoincrement,
            tipo_material text not null,
            nome_material text not null
        );

        create table if not exists exames(
            cod_exame integer primary key autoincrement,
			nome_exame text not null,
            data_exame text not null
        );

        create table if not exists materiais_exame(
            cod_exame integer not null,
            cod_material integer not null,
            quantidade integer,
            foreign key (cod_exame) references exames(cod_exame),
            foreign key (cod_material) references materiais(cod_material),
            primary key(cod_exame, cod_material)
        );

        create table if not exists consultas(
            cod_consulta integer primary key autoincrement,
            data_consulta text not null
        );

        create table if not exists exames_consulta(
            cod_exame integer not null,
            cod_consulta integer not null,
            foreign key (cod_exame) references exames(cod_exame),
            foreign key (cod_consulta) references consulta(cod_consulta),
            primary key(cod_exame, cod_consulta)
        );

        create table if not exists pagamentos(
            cod_pagamento integer primary key autoincrement,
            data_pagamento text not null
        );

        create table if not exists pagamentos_particulares(
            cod_pagamento integer primary key,
            nome_pagador text not null,
            cpf_pagador text not null
        );

        create table if not exists pagamentos_convenio(
            cod_pagamento integer primary key,
            cod_convenio text not null
        );
        
        create table if not exists pacientes(
            nome text not null,
            cpf text primary key
        );
        
        create table if not exists pacientes_consulta(
            cod_consulta integer not null,
            cpf text not null,
            foreign key (cod_consulta) references consultas(cod_consulta),
            foreign key (cpf) references pacientes(cpf),
            primary key (cod_consulta, cpf)
        );""")
    print('Banco de Dados Iniciado')


class DAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn


class MaterialDAO(DAO):
    def add_material(self, material: Material):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO materiais
            (tipo_material, nome_material)
            VALUES (?, ?)""", (material.tipo_material, material.nome_material))
        self.conn.commit()
        material.cod_material = cursor.lastrowid

    def get_material(self, cod_material):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM materiais
            WHERE cod_material = ?;""", (cod_material, ))
        mat_tup = cursor.fetchone()
        if mat_tup:
            return Material(mat_tup[1], mat_tup[2], mat_tup[0])
        return None

    def altera_material(self, material: Material):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE materiais
            set tipo_material= ?, nome_material=?
            WHERE cod_material = ?""", (material.tipo_material, material.nome_material, material.cod_material))
        self.conn.commit()

    def todos_materiais(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM materiais;""")
        mats = []
        for mat_tup in cursor.fetchall():
            mats.append(Material(mat_tup[1], mat_tup[2], mat_tup[0]))

        return mats


class ExameDAO(DAO):
    def add_exame(self, exame: Exame):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO exames
            (data_exame, nome_exame)
            values(?, ?)""", (exame.data_exame, exame.nome_exame))
        exame.cod_exame = cursor.lastrowid
        dao = MaterialDAO(self.conn)
        for material in exame.materiais:
            if material.cod_material:
                dao.altera_material(material)
            else:
                dao.add_material(material)
                m = exame.materiais[material]
                cursor.execute("""
                    INSERT INTO materiais_exame
                    values (?, ?, ?);
                """, (exame.cod_exame, material.cod_material, m))
        self.conn.commit()

    def get_exame(self, cod_exame):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT nome_exame, data_exame, cod_exame FROM exames;""")
        tup = cursor.fetchone()
        cursor.execute("""
            SELECT * FROM materiais_exame
            JOIN materiais ON materiais_exame.cod_material = materiais.cod_material
            WHERE materiais_exame.cod_exame = ?;""", (tup[2],))
        mats = []
        for mat_tup in cursor.fetchall():
            mats.append(Material(mat_tup[1], mat_tup[2], mat_tup[0]))
        exame = Exame(tup[0], tup[1], mats, tup[2])

        return exame

    def todos_exames(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT nome_exame, data_exame, cod_exame FROM exames;""")
        exames = []
        for tup in cursor.fetchall():
            mats = []
            cursor1 = self.conn.cursor()
            cursor1.execute("""
            SELECT * FROM materiais_exame
            JOIN materiais ON materiais_exame.cod_material = materiais.cod_material
            WHERE materiais_exame.cod_exame = ?;""", (tup[2],))
            mats = []
            for mat_tup in cursor1.fetchall():
                mats.append(Material(mat_tup[1], mat_tup[2], mat_tup[0]))
            exame = Exame(tup[0], tup[1], mats, tup[2])
            exames.append(exame)

        return exames


class ConsultaDAO(DAO):
    def add_consulta(self, consulta: Consulta):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO consultas
            (data_consulta)
            values(?)""", (consulta.data_consulta, ))
        consulta.cod_consulta = cursor.lastrowid
        dao = ExameDAO(self.conn)
        for exame in consulta.exames:
            if exame.cod_exame is None:
                dao.add_exame(exame)
                cursor.execute("""
                    INSERT INTO exames_consulta
                    values (?, ?);
                """, (exame.cod_exame, consulta.cod_consulta))
        dao = PacienteDAO(self.conn)
        for pac in consulta.pacientes:
            print(pac)
            if dao.get_paciente(pac.cpf) is None:
                print('new)')
                dao.add_paciente(pac)
                cursor.execute("""
                    INSERT INTO pacientes_consulta
                    values(?, ?);
                """, (consulta.cod_consulta, pac.cpf))
        self.conn.commit()

    def todas_consultas(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM consultas;""")
        edao = ExameDAO(self.conn)
        pdao = PacienteDAO(self.conn)
        consultas = []
        for tup in cursor.fetchall():
            cursor1 = self.conn.cursor()
            exames = []
            cursor1.execute("""
            SELECT cod_exame FROM exames_consulta
            WHERE cod_consulta = ?;""", (tup[0],))
            print('tup', tup[0])
            for row in cursor1.fetchall():
                exames.append(edao.get_exame(row[0]))
            pacientes = []
            cursor1.execute("""
            SELECT cpf FROM pacientes_consulta
            WHERE cod_consulta = ?;""", (tup[0],))
            for row in cursor1.fetchall():
                pacientes.append(pdao.get_paciente(row[0]))
            consulta = Consulta(tup[1], exames, pacientes, tup[0])
            consultas.append(consulta)
        return consultas


class PacienteDAO(DAO):
    def add_paciente(self, paciente: Paciente):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes
            values(?, ?)""", (paciente.nome, paciente.cpf))
        self.conn.commit()

    def get_paciente(self, cpf):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM pacientes
            WHERE cpf = ?""", (cpf,))
        row = cursor.fetchone()
        if not row is None:
            return Paciente(*row)
        else:
            return None

    def todos_pacientes(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM pacientes""")
        return [Paciente(*row) for row in cursor.fetchall()]

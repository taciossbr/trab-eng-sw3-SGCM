
class Material:
    def __init__(self, tipo_material, nome_material, cod_material=None):
        self.cod_material = cod_material
        self.tipo_material = tipo_material
        self.nome_material = nome_material

    def __hash__(self):
        return hash(self.nome_material)

    def __eq__(self, other):
        if isinstance(other, Material):
            return self.nome_material == other.nome_material
        else:
            return False

    def __repr__(self):
        return f"Material('tipo_material={self.tipo_material}',nome_material'{self.nome_material}',cod_material={self.cod_material})"


class Exame:
    def __init__(self, nome_exame, data_exame, materiais=None, cod_exame=None):
        self.cod_exame = cod_exame
        self.nome_exame = nome_exame
        self.data_exame = data_exame
        self.materiais = materiais or {}

    def add_material(self, material, quantidade=1):
        if material in self.materiais:
            self.materiais[material] += quantidade
        else:
            self.materiais[material] = quantidade

    def __repr__(self):
        return f"Exame(cod_exame={self.cod_exame},nome_exame='{self.nome_exame}',data_exame='{self.data_exame}',materiais={[x for x in self.materiais]})"


class Consulta:
    def __init__(self, data_consulta, exames=None, pacientes=None, cod_consulta=None):
        self.cod_consulta = cod_consulta
        self.data_consulta = data_consulta
        self.exames = exames or []
        self.pacientes = pacientes or []

    def add_exame(self, exame):
        self.exames.append(exame)

    def add_paciente(self, paciente):
        self.pacientes.append(paciente)

    def __repr__(self):
        return f"Consulta(cod_consulta={self.cod_consulta},data_consulta='{self.data_consulta}',exames={self.exames},pacientes={self.pacientes})"


class Paciente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def __repr__(self):
        return f"Paciente(nome='{self.nome}'',cpf='{self.cpf}')"


class Pagamento:
    def __init__(self, data_pagamento, cod_pagamento=None):
        self.cod_pagamento = cod_pagamento
        self.data_pagamento = data_pagamento


class PagamentoParticular(Pagamento):
    def __init__(self, data_pagamento, nome_pagador, cpf_pagador, cod_pagamento=None):
        super().__init__(self, data_pagamento, cod_pagamento)
        self.nome_pagador = nome_pagador
        self.cpf_pagador = cpf_pagador


class PagamentoConvenio(Pagamento):
    def __init__(self, data_pagamento, codigo_convenio, cod_pagamento=None):
        super().__init__(self, data_pagamento, cod_pagamento)
        self.codigo_convenio = codigo_convenio

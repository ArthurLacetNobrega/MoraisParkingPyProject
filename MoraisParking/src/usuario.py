class Usuario:
    """ Representa o usuario que vai ter acesso ao sistema"""

    def __init__(self, nome, cpf, funcao, setor, usuario, senha):
        self.nome = nome
        self.cpf = cpf
        self.funcao = funcao
        self.setor = setor
        self.usuario = usuario
        self.senha = senha

    # Getters e Setters
    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_cpf(self):
        return self.cpf

    def set_cpf(self, cpf):
        self.cpf = cpf

    def get_funcao(self):
        return self.funcao

    def set_funcao(self, funcao):
        self.funcao = funcao

    def get_setor(self):
        return self.setor

    def set_setor(self, setor):
        self.setor = setor

    def get_usuario(self):
        return self.usuario

    def set_usuario(self, usuario):
        self.usuario = usuario

    def get_senha(self):
        return self.senha

    def set_senha(self, senha):
        self.senha = senha

    def __eq__(self, outro):
        return isinstance(outro, Usuario) and outro.usuario == self.usuario

    # toString
    def __str__(self):
        return "Nome: %s\nCPF: %s\nFuncao: %s\nSetor: %s\nUsuario: %s\n Senha: %s\n" %(self.nome, self.cpf, self.funcao, self.setor, self.usuario, self.senha)
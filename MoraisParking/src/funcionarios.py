class Funcionarios:


    def __init__(self, nome, matricula, setor, funcao):
        self.nome = nome
        self.matricula = matricula
        self.setor = setor
        self.funcao = funcao

    #Getters & Setters
    def get_nome(self):
        return self.nome

    def set_nome (self, nome):
        self.nome = nome

    def get_matricula(self):
        return self.matricula

    def set_matricula (self, matricula):
        self.matricula = matricula

    def get_setor(self):
        return self.setor

    def set_setor (self, setor):
        self.setor = setor

    def get_funcao(self):
        return self.funcao

    def set_funcao (self, funcao):
        self.funcao = funcao

    # toString
    def __str__(self):
        return "Nome: %s\nMatricula: %s\nSetor: %s\nFunção: %s" %(self.nome, self.matricula, self.setor, self.funcao)
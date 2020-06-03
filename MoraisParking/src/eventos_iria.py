class Eventos():
    """Representa os eventos que podem acontecer, que reduzem a capacidade e modificam o acesso de veiculos"""

    def __init__(self, nome, data_inicio, duracao, vagas):
        self.nome = nome
        self.data_inicio = data_inicio
        self.duracao = duracao
        self.vagas = vagas
        self.evento_areas = {}

    #Getters & Setters
    def get_nome(self):
        return self.nome

    def set_nome (self, nome):
        self._nome = nome

    def get_data_inicio(self):
        return self.data_inicio

    def set_data_inicio(self, data_inicio):
        return self.data_inicio

    def get_duracao(self):
        return self.duracao

    def set_duracao(self, duracao):
        self.duracao = duracao

    def get_vagas(self):
        return self.vagas

    def set_vagas(self, vagas):
        self.vagas = vagas

    def get_evento_areas(self):
        return self.evento_areas


        #To String
    def __str__(self):
        return "Nome: %s\nData de Realização: %s\nDuração: %d\nVagas: %s" % (self.nome, self.data_inicio, self.duracao, self.vagas)


import sqlite3

class Veiculo:
    """representa os veículos que terão acesso ao estacionamento"""

    def __init__(self, placa, proprietario, modelo, categoria):
        self.placa = placa
        self.proprietario = proprietario
        self.modelo = modelo
        self.categoria = categoria

    # Getters e Setters 
    def get_proprietario(self):
        return self.proprietario

    def set_proprietario(self, proprietario):
        self.proprietario = proprietario

    def get_placa(self):
        return self.placa

    def set_placa(self, placa):
        self.placa = placa

    def get_modelo(self):
        return self.modelo

    def set_modelo(self, modelo):
        self.modelo = modelo

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, categoria):
        self.categoria = categoria

    #toString
    def __str__(self):
        return "Placa: %s\nProprietário: %s\nModelo: %s\nCategoria: %s" %(self.placa, self.proprietario, self.modelo, self.categoria)



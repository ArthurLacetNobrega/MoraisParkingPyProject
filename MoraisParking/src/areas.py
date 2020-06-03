class Areas():
    """Representa as áreas do estacionamento, por categoria"""
    def __init__(self, nome, capacidade, categoria):
        self.nome = nome
        self.capacidade = capacidade
        self.categoria = categoria
        self.veiculos_area = list()

    #Getter & Setter
    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_capacidade(self):
        return self.capacidade

    def set_capacidade(self, capacidade):
        self.capacidade = capacidade

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, categoria):
        self.categoria = categoria

    def get_veiculos_area(self):
        return self.veiculos_area

    #Metodos
    def entrada_veiculo(self, veiculo):
        self.veiculos_area.append(veiculo)

    def saida_veiculo(self, veiculo):
        self.veiculos_area.remove(veiculo)

    #To String
    def __str__(self):
        return "Nome: %s\nCapacidade: %d\nCategoria: %s" %(self.nome, self.capacidade, self.categoria)

    def check(self):
        for veic in self.get_veiculos_area():
            print(veic)







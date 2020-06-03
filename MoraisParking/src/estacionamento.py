from areas import Areas
from eventos import *
from proprietario import Proprietario
from usuario import Usuario
from veiculo import Veiculo
from ocorrencias import Ocorrencia
from relatorios import Relatorios
from funcionarios import Funcionarios
from datetime import datetime, timedelta
import sqlite3


class Singleton:
    '''para garantir que apenas um objeto de um certo tipo seja criado'''
    __instance = None

    def __new__(cls, *args, **kwargs):
        if Singleton.__instance is None:
            Singleton.__instance = super().__new__(cls)
        return Singleton.__instance


class Estacionamento(Singleton):
    """Representa o estacionamento e cotrola a integração dos métodos das classes"""

    def __init__(self):
        self.cadastro_areas = list()
        self.cadastro_veiculos = list()
        self.cadastro_ocorrencias = list()
        self.cadastro_proprietarios = {}
        self.categorias = ['PREFERENCIAL', 'FUNCIONARIOS', 'CARRO', 'MOTOCICLETA', 'VAN', 'ÔNIBUS', 'VISITANTES']
        self.tipo_ocorrencias = ['FURTO', 'SINISTRO', 'ESTACIONAMENTO INDEVIDO', 'AVARIA', 'INUNDAÇÃO', 'OUTROS']
        self.cadastro_usuario = list()
        self.lista_ocupacao = list()
        self.cadastro_funcionarios = list()

    # getters
    def get_cadastro_areas(self):
        return self.cadastro_areas

    def get_cadastro_veiculos(self):
        return self.cadastro_veiculos

    def get_cadastro_ocorrencias(self):
        return self.cadastro_ocorrencias

    def get_cadastro_proprietarios(self):
        return self.cadastro_proprietarios

    def get_categorias(self):
        return self.categorias

    def get_tipo_ocorrencias(self):
        return self.tipo_ocorrencias

    def get_cadastro_usuario(self):
        return self.cadastro_usuario
    
    def get_lista_ocupacao(self):
        return self.lista_ocupacao

    # METODOS RELACIONADOS A CATEGORIAS
    def adicionar_categoria(self, categoria):
        '''Caso o gestor precise incluir uma nova categoria no estacionamento'''
        try:
            self.categorias.append(categoria.upper())
            print("Categoria adicionada com sucesso!")
        except:
            print("Cadastro não realizado!")

    def validar_cetegoria(self, categoria):
        '''funcao de validação de categoria'''
        if categoria.upper() not in self.categorias:
            print("Categoria inválida! A categoria deve ser uma dessas opções:  ", self.categorias)
            categoria = input("Insira a categoria: ").upper()
            return categoria

    # METODOS RELACIONADOS A VEICULOS e PROPRIETARIOS
    def cadastrar_veiculo(self, nome, matricula, curso, placa, modelo, categoria):
        '''Este método irá instanciar o objeto proprietário e o objeto veículo a partir de uma única solicitacao ao usuario.'''

        # primeiro valida se o veículo já existe no cadastro.
        if self.validar_veiculo(placa.upper()) == None:
            # cadastra o proprietário no dicionario e no BD
            prop = Proprietario(nome.upper(), matricula.upper(), curso.upper())
            self.cadastro_proprietarios[placa.upper()] = prop
            c.execute(
                'CREATE TABLE IF NOT EXISTS proprietarios(placa TEXT PRIMARY KEY, nome TEXT, matricula TEXT, curso TEXT)')
            c.execute('INSERT INTO proprietarios VALUES (?, ?, ?,?)',
                      (placa.upper(), prop.get_nome(), prop.get_matricula(), prop.get_curso()))
            con.commit()

            # Cadastra o veiculo no array e no BD
            veic = Veiculo(placa.upper(), prop.get_nome(), modelo.upper(), categoria.upper())

            try:
                c.execute(
                    'CREATE TABLE IF NOT EXISTS veiculos(placa TEXT PRIMARY KEY, proprietario TEXT, modelo TEXT, categoria TEXT)')
                c.execute('INSERT INTO veiculos VALUES (?, ?, ?,?)',
                          (veic.get_placa(), prop.get_nome(), veic.get_modelo(), veic.get_categoria()))
                con.commit()
                self.cadastro_veiculos.append(veic)
                print("Veículo cadastrado com sucesso")
            except:
                print("Erro ao cadastrar veículo!")

        else:
            print('Veículo já está cadastrado!')
            resposta = input('Deseja cadastrá-lo novamente? (S/N) ')
            if resposta.upper() == 'S':
                self.remover_veiculo(placa.upper())
                self.cadastrar_veiculo(input('Nome: '), input('Matícula: '), input('Curso: '), input('Placa: '),
                                       input('Modelo: '), input('Categoria: '))

    def consultar_proprietario(self, placa):
        '''Consulta quem é o proprietário do veículo atraves da placa informada'''
        placa_consulta = placa.upper()
        if placa_consulta in self.cadastro_proprietarios.keys():
            print(self.cadastro_proprietarios[placa_consulta])
        else:
            print("ATENÇÃO!!! Veículo não cadastrado!")

    def consultar_veiculo(self, placa):
        '''retorna o veículo (str) através da placa informada'''
        veiculo = self.validar_veiculo(placa.upper())
        if veiculo in self.get_cadastro_veiculos():
            print(veiculo)
        else:
            print("Veículo não cadastrado!")

    def validar_veiculo(self, placa):
        '''método chave, que permite validar a existência do veículo na lista'''
        for veiculo in self.cadastro_veiculos:
            if placa.upper() == veiculo.get_placa():
                return veiculo
        return None

    def remover_veiculo(self, placa):
        '''Método para excluir o veículo e o proprietário vinculado a ele'''
        # remove do BD
        try:
            c.execute("DELETE FROM veiculos WHERE placa = ?", (placa.upper(),))
            con.commit()
            c.execute("DELETE FROM proprietarios WHERE placa = ?", (placa.upper(),))
            con.commit()
            print('Veículo removido com sucesso!')
        except:
            print("Veículo não cadastrado!")

        # remove o proprietario do dicionario
        del self.cadastro_proprietarios[placa]

        # remove o veículo da lista
        veiculo = self.validar_veiculo(placa.upper())
        self.cadastro_veiculos.remove(veiculo)

    def validar_entrada(self, placa):
        '''método que valida a entrada do veículo no estacionamento, checando seu cadastramento e a área que pode estacionar
        e registra a data e hora da entrada e o veiculo, para fins de controle de rotatividade'''
        if self.validar_veiculo(placa.upper()) != None:
            veic = self.validar_veiculo(placa.upper())
            for area in self.get_cadastro_areas():
                if area.get_categoria().upper() == veic.get_categoria().upper():
                    area.entrada_veiculo(veic)
            c.execute(
                'CREATE TABLE IF NOT EXISTS entradas(data TEXT, hora TEXT,placa TEXT,categoria TEXT)')
            c.execute('INSERT INTO entradas VALUES (?,?,?,?)',
                      (data_em_texto, hora_em_texto, veic.get_placa().upper(), veic.get_categoria()))
            con.commit()

            self.lista_ocupacao.append(veic.get_placa())
            print('Entrada Registrada!')
        else:
            print('ATENÇÃO! Veículo não cadastrado!')
            # aqui, caso o veículo não esteja cadastrado e o usuário queira permitir a entrada pra uma area apropriada.
            resposta = input('Deseja permitir entrada como Visitante? (S/N) ')
            if resposta.upper() == "S":
                self.cadastrar_veiculo('Visitante', 'n/a', 'n/a', placa.upper(),
                                       'n/a', 'VISITANTES')
                self.validar_entrada(placa)
            else:
                return

    def validar_saida(self, placa):
        '''valida a saída de um veículo que tenha tido sua entrada registrada'''
        if placa.upper() in self.lista_ocupacao:
            veic = self.validar_veiculo(placa.upper())
            c.execute(
                'CREATE TABLE IF NOT EXISTS saidas(data TEXT, hora TEXT,placa TEXT,categoria TEXT)')
            c.execute('INSERT INTO saidas VALUES (?,?,?,?)',
                      (data_em_texto, hora_em_texto, veic.get_placa().upper(), veic.get_categoria()))
            con.commit()

            for area in self.get_cadastro_areas():
                if area.get_categoria().upper() == veic.get_categoria().upper():
                    area.saida_veiculo(veic)
            self.lista_ocupacao.remove(placa.upper())
            # como o veículo entrou temporariamente no cadastro de veículos como visitante, assim que ele sai do estacionamento,
            # ele é removido dessa base.
            if veic.get_categoria() == 'VISITANTES':
                self.remover_veiculo(placa.upper())
            print('Saída Registrada!')
        else:
            print("Entrada não registrada!")

    # METODOS RELACIONADOS A ÁREAS
    def cadastrar_area(self, nome, capacidade, categoria):
        '''O usuário(gestor) cadastra novas áreas'''
        area = Areas(nome.upper(), capacidade, categoria.upper())
        self.cadastro_areas.append(area)
        self.categorias.append(area.get_categoria())

        # inserção no banco
        try:
            c.execute(
                'CREATE TABLE IF NOT EXISTS areas(nome TEXT, capacidade INT, categoria TEXT)')
            c.execute('INSERT INTO areas VALUES (?, ?, ?)',
                      (area.get_nome(), area.get_capacidade(), area.get_categoria()))
            con.commit()
            print("Área cadastrada com sucesso!")
        except:
            print("Erro ao efetuar cadastro!")

    def consultar_area(self, categoria):
        '''consulta a área pela sua categoria, retornando a capacidade da área'''
        categ_areas = {}
        for area in self.cadastro_areas:
            if categoria.upper() == area.get_categoria():
                categ_areas[area.get_categoria()] = area.get_capacidade()
                return print('A área e sua capacidade: ', categ_areas)

        return print("A área ainda não foi criada!")

    def alterar_capacidade(self, categoria, vagas):
        '''Método para o gestor, caso ele queira alterar (reduzir ou aumentar) a capacidade de alguma área, para o surgimento de novas'''
        # alteração da capacidade no objeto Area
        for area in self.cadastro_areas:
            if categoria.upper() == area.get_categoria():
                nova_capacidade = area.get_capacidade() - vagas
                area.set_capacidade(nova_capacidade)

                # alteração da capacidade no Banco
                c.execute('UPDATE areas SET capacidade = ? WHERE categoria = ?', (nova_capacidade, categoria.upper()))
                con.commit()
            else:
                print('Área não cadastrada!')

    def excluir_area(self, categoria):
        '''Método utilizado pelo gestor, caso ele queira remover alguma área'''
        for area in self.cadastro_areas:
            if categoria.upper() == area.get_categoria():
                self.cadastro_areas.remove(categoria.upper())
                try:
                    # exclusão do Banco
                    c.execute('DELETE FROM areas WHERE categoria = ?', (categoria.upper()), )
                    con.commit()
                except:
                    print("Área removida com sucesso!")
            else:
                print('Área não cadastrada!')

    def ocupacao_areas(self, categoria):
        '''Mostra o percentual de ocupação da área, mesmo em dias de eventos'''
        percent = 0
        for area in self.cadastro_areas:
            if categoria.upper() == area.get_categoria():
                # quando o sistema identifica que é dia de evento, ele fará alteração no cálculo da ocupacao.
                # para que essa alteração não seja 'setada' diretamente na área já cadastrada.
                if self.dias_eventos():
                    reducao_vaga = 0
                    # consulta no banco se é dia de evento e a capacidade destinada àquela área
                    c.execute('SELECT vagas FROM areas_eventos WHERE data = ? AND area = ? ',
                              (data_em_texto, categoria.upper()))
                    for linha in c.fetchall():
                        reducao_vaga = linha[0]
                    quantidade = len(area.get_veiculos_area())
                    percent = (quantidade * 100 / (area.get_capacidade() - reducao_vaga))
                else:
                    # se não for dia de evento, o cálculo é padrão
                    quantidade = len(area.get_veiculos_area())
                    percent = (quantidade * 100 / area.get_capacidade())
        return percent

    def status_areas(self, categoria):
        '''Mostra os veículos que estão em cada área, no instante da consulta'''
        for area in self.cadastro_areas:
            if categoria.upper() == area.get_categoria():
                for veiculo in area.get_veiculos_area():
                    print(veiculo)

    # METODOS RELACIONADOS A USUARIOS
    def cadastrar_usuario(self, nome, cpf, funcao, setor, usuario, senha):
        '''método de cadastro do usuário'''
        user = Usuario(nome.upper(), cpf.upper(), funcao.upper(), setor.upper(), usuario, senha)
        try:
            c.execute(
                'CREATE TABLE IF NOT EXISTS usuarios (nome TEXT, cpf TEXT, funcao TEXT, setor TEXT, usuario TEXT, senha TEXT)')
            c.execute('INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?)',
                      (user.get_nome(), user.get_cpf(), user.get_funcao(), user.get_setor(), user.get_usuario(),
                       user.get_senha()))
            con.commit()
            self.cadastro_usuario.append(user)
            print("Usuário cadastrado com sucesso!")
        except:
            print("Erro ao cadastrar usuário!")

    def validar_usuario(self, user):
        '''método que verifica se o usuário está cadastrado'''
        for usuario in self.cadastro_usuario:
            if user == usuario.get_usuario():
                return usuario
        return None

    def login(self, usuario, senha):
        '''metodo que valida o login do usuário, contanto que já esteja cadastrado'''
        user = self.validar_usuario(usuario)
        if user != None:
            if user.get_usuario() == usuario and user.get_senha() == senha:
                return True
            else:
                return False
        else:
            return False

    # METODOS RELACIONADOS A OCORRÊNCIAS
    def validar_tipo_ocorrencia(self, tipo):
        if tipo in self.tipo_ocorrencias:
            return tipo
        else:
            return "Tipo inválido!"

    def cadastrar_ocorrencia(self, tipo, quantidade_veiculos, data, hora, fatos):
        '''método para cadastrar ocorrências. gera um ID automático(sequencia) que permite facilidade ao usuário do estacionamento
         consultar o andamento posteriormente'''
        id = len(self.cadastro_ocorrencias) + 1
        ocorrencia = Ocorrencia(id, tipo.upper(), quantidade_veiculos, data, hora, fatos)
        try:
            c.execute(
                'CREATE TABLE IF NOT EXISTS ocorrencias (id INTEGER, tipo TEXT, quantidade_veiculos INTEGER, data TEXT, hora TEXT, fatos TEXT)')
            c.execute('INSERT INTO ocorrencias VALUES (?, ?, ?, ?, ?, ?)',
                      (id, ocorrencia.get_tipo(), ocorrencia.get_quantidade_veiculos(), ocorrencia.get_data(),
                       ocorrencia.get_hora(),
                       ocorrencia.get_fatos()))
            con.commit()
            self.cadastro_ocorrencias.append(ocorrencia)
            print("Ocorrência cadastrada com sucesso!")
        except:
            print("Erro ao cadastrar ocorrência")

        # inclui os veículos envolvidos na ocorrencia, validando se os mesmos possuem cadastro.
        # caso contrário deverá ser cadastrado.
        for i in range(quantidade_veiculos):
            placa = input("Insira a placa do veículo %sº envolvido: " % (i + 1))
            veiculo = self.validar_veiculo(placa.upper())
            if veiculo != None:
                c.execute(
                    'CREATE TABLE IF NOT EXISTS veiculos_ocorrencias (id INTEGER, placa TEXT)')
                c.execute('INSERT INTO veiculos_ocorrencias VALUES (?,?)', (ocorrencia.get_id(), veiculo.get_placa()))
                con.commit()
                ocorrencia.adicionar_veiculo(veiculo)
            else:
                print("Veículo não cadastrado!")
        print('Para acompanhamento, o ID desta ocorrência é: ', id)

    def consultar_ocorrencia_id(self, id):
        '''método para consultar a ocorrência a partir do ID fornecido previamente.'''
        for ocorrencia in self.get_cadastro_ocorrencias():
            if id == ocorrencia.get_id():
                return print(ocorrencia)

        return print('Ocorrência não localizada!')

    def consultar_ocorrencia_placa(self, placa):
        '''método para consultar ocorrência a partir da placa do veículo.
        retorna todas as ocorrências que ele tenha se envolvido'''
        c.execute("SELECT * FROM veiculos_ocorrencias WHERE placa = ?", (placa.upper(),))
        for linha in c.fetchall():
            id = linha[0]
            c.execute("SELECT * FROM ocorrencias WHERE id = ?", (id,))
            for linha in c.fetchall():
                return print(linha)
        return print('Veículo não possui ocorrências registradas!')

        # METODOS RELACIONADOS A EVENTOS
    def reservar_areas_eventos(self,nome_evento):
        evento = Eventos.buscar_evento(nome_evento.upper())
        if evento != None:
            data = evento[1]
            data = datetime.strptime(data, '%d/%m/%Y').date()
            for evento in Eventos.all():
                for i in range(evento[2]):
                    data_nova = data + timedelta(days=i)  # adiciona a quantidade de dias de evento à data inicial
                    data_format = data_nova.strftime('%d/%m/%Y')
                    print("Informe quantas vagas serão reservadas por área no dia %d" % (
                            i + 1))  # caso o evento tenha ocupações distintas por dia de evento.
                    self.cadastrar_areas_evento(evento, data_format)
        else:
            print('Evento não cadastrado!')


    def cadastrar_areas_evento(self, evento, data):
        '''Método para criar uma tabela com a área e a capacidade que será destinada no dia do evento.
         Importante para que o método da capacidade saiba quanto será reduzido por área no dia específico'''

        print('Áreas: ', self.get_categorias())
        categoria = input('Insira a Área que será reduzida: ')
        vagas = int(input('Insira a quantidade de vagas a reduzir: '))
        resposta = input('Deseja alterar a capacidade de nova área? (S/N) ')
        c.execute('CREATE TABLE IF NOT EXISTS areas_eventos (data TEXT, area TEXT, vagas INTEGER)')
        c.execute('INSERT INTO areas_eventos VALUES (?,?,?)',
                  (data, categoria.upper(), vagas))
        con.commit()
        if resposta.upper() == 'S':
            self.cadastrar_areas_evento(evento, data)

    def dias_eventos(self):
        '''informa ao método de ocupação de áreas quais são os dias que há eventos.'''
        c.execute('SELECT data FROM areas_eventos ')
        for linha in c.fetchall():
            if linha[0] == data_em_texto:
                return True

        #MÉTODO FUNCIONÁRIO
    def cadastrar_funcionario(self, nome, matricula, setor, funcao, placa, categoria):

        funcionario = Funcionarios(nome.upper(), matricula.upper(), setor.upper(), funcao.upper())
        if self.validar_veiculo(placa.upper()) != None:
            veiculo = self.validar_veiculo(placa.upper())
            try:
                c.execute('CREATE TABLE IF NOT EXISTS funcionarios (nome TEXT, matricula TEXT, setor TEXT, funcao TEXT')
                c.execute('INSERT INTO ocorrencias VALUES (?, ?, ?, ?, ?, ?)',
                          (funcionario.get_nome(), funcionario.get_matricula(),funcionario.get_setor(), funcionario.get_funcao(), placa.upper(), categoria.upper()))
                con.commit()
                self.cadastro_funcionarios.append(funcionario)
                veiculo.set_categoria(categoria.upper())
                print("Funcionário Cadastrado!")
            except:
                print("Erro no cadastro!")

        else:
            print("Veículo não cadastrado!")



    '''MÉTODOS ARMAZENAMENTO - QUE REINSEREM NAS LISTAS, DICIONÁRIOS, OS VALORES JÁ REGISTRADOS'''

    def armazenar_veiculos(self):
        c.execute("SELECT * FROM veiculos ")
        for linha in c.fetchall():
            placa = linha[0]
            proprietario = linha[1]
            modelo = linha[2]
            categoria = linha[3]
            veiculo = Veiculo(placa, proprietario, modelo, categoria)
            self.cadastro_veiculos.append(veiculo)

    def armazenar_proprietarios(self):
        c.execute("SELECT * FROM proprietarios ")
        for linha in c.fetchall():
            placa = linha[0]
            nome = linha[1]
            matricula = linha[2]
            curso = linha[3]
            prop = Proprietario(nome, matricula, curso)
            self.cadastro_proprietarios[placa] = prop

    def armazenar_areas(self):
        c.execute("SELECT * FROM areas ")
        for linha in c.fetchall():
            nome = linha[0]
            capacidade = linha[1]
            categoria = linha[2]
            area = Areas(nome, capacidade, categoria)
            self.cadastro_areas.append(area)

    def armazenar_usuarios(self):
        c.execute("SELECT * FROM usuarios ")
        for linha in c.fetchall():
            nome = linha[0]
            cpf = linha[1]
            funcao = linha[2]
            setor = linha[3]
            usuario = linha[4]
            senha = linha[5]
            user = Usuario(nome, cpf, funcao, setor, usuario, senha)
            self.cadastro_usuario.append(user)

    def armazenar_ocorrencias(self):
        c.execute("SELECT * FROM ocorrencias ")
        for linha in c.fetchall():
            id = linha[0]
            tipo = linha[1]
            quantidade_veiculos = linha[2]
            data = linha[3]
            hora = linha[4]
            fatos = linha[5]
            ocorrencia = Ocorrencia(id, tipo, quantidade_veiculos, data, hora, fatos)
            self.cadastro_ocorrencias.append(ocorrencia)
            c.execute("SELECT * FROM veiculos_ocorrencias ")
            for linha in c.fetchall():
                id = linha[0]
                placa = linha[1]
                veiculo = self.validar_veiculo(placa.upper())
                ocorrencia.adicionar_veiculo(veiculo)


    '''MÉTODOS QUE GERAM OS RELATÓRIOS'''

    def relatorio_ocorrencias(self):
        """executa o acesso ao BD e chama a função exportar."""

        def gerar_dicionario(cursor, row):
            dic = {}
            for idx, col in enumerate(cursor.description):
                dic[col[0]] = row[idx]
            return dic

        con.row_factory = gerar_dicionario
        c = con.cursor()

        c.execute("SELECT id, tipo, quantidade_veiculos, data, hora, fatos FROM ocorrencias")
        dados = c.fetchall()

        titulo = "RELAÇÃO DE OCORRÊNCIAS"

        cabecalho = (
            ("id", "ID"),
            ("tipo", "TIPO"),
            ("quantidade_veiculos", "QTD VEICULOS"),
            ("data", "DATA"),
            ("hora", "HORA"),
            ("fatos", "FATOS"),
        )

        nome_arquivo = "relatorio_ocorrencia.pdf"

        relatorio = Relatorios(titulo, cabecalho, dados, nome_arquivo).exportar()
        print(relatorio)

    def relatorio_ocorrencias_data(self, data):
        """executa o acesso ao BD e chama a função exportar."""

        def gerar_dicionario(cursor, row):
            dic = {}
            for idx, col in enumerate(cursor.description):
                dic[col[0]] = row[idx]
            return dic

        con.row_factory = gerar_dicionario
        c = con.cursor()
        c.execute("SELECT id, tipo, quantidade_veiculos, data, hora, fatos FROM ocorrencias WHERE data = ?", (data,))
        dados = c.fetchall()

        titulo = "RELAÇÃO DE OCORRÊNCIAS"

        cabecalho = (
            ("id", "ID"),
            ("tipo", "TIPO"),
            ("quantidade_veiculos", "QTD VEICULOS"),
            ("data", "DATA"),
            ("hora", "HORA"),
            ("fatos", "FATOS"),
        )

        nome_arquivo = "relatorio_ocorrencia_data.pdf"

        relatorio = Relatorios(titulo, cabecalho, dados, nome_arquivo).exportar()
        print(relatorio)

    def relatorio_rotatividade(self, data):
        """executa o acesso ao BD e chama a função exportar."""

        def gerar_dicionario(cursor, row):
            dic = {}
            for idx, col in enumerate(cursor.description):
                dic[col[0]] = row[idx]
            return dic

        con.row_factory = gerar_dicionario
        c = con.cursor()
        c.execute("SELECT data, hora, placa, categoria FROM entradas WHERE data = ?", (data,))
        dados = c.fetchall()

        titulo = "RELAÇÃO DE VEÍCULOS"

        cabecalho = (
            ("data", "DATA"),
            ("hora", "HORA"),
            ("placa", "PLACA"),
            ("categoria", "CATEGORIA"),
        )

        nome_arquivo = "relatorio_rotatividade_data.pdf"

        relatorio = Relatorios(titulo, cabecalho, dados, nome_arquivo).exportar()
        print(relatorio)


# conexão com o banco de dados
con = sqlite3.connect('database.db')
c = con.cursor()

# variaveis constantes
data_atual = datetime.today()
data_em_texto = data_atual.strftime('%d/%m/%Y')
hora_em_texto = data_atual.strftime('%H:%M')

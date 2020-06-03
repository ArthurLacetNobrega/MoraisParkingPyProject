import sqlite3

con = sqlite3.connect('database.db')
c = con.cursor()

class Eventos():
    """Representa os eventos que podem acontecer, que reduzem a capacidade e modificam o acesso de veiculos"""

    #criar tabela
    #método estático para criação do método
    @staticmethod
    def criar_tabela():
        try:
            c.execute(
                'CREATE TABLE IF NOT EXISTS eventos (nome TEXT, data_inicio TEXT, duracao INTEGER, vaga TEXT)')
        except:
            print('Erro ao criar a tabela')

    '''Metodo usada para buscar todos os itens da tabela eventos'''
    @staticmethod
    def all():
        try:
            r = c.execute('SELECT * FROM eventos')
        except:
            print('Erro ao fazer consulta')
        else:
            return r.fetchall()

    @staticmethod
    def salvar_evento(nome, data_inicio, duracao, vagas):
        '''cadastrando evento, a função sera chamada em estacionamento.py '''
        print("CADASTRO DE EVENTOS")
        try:
            c.execute("INSERT INTO eventos VALUES (?, ?, ?, ?)",
                      (nome.upper(), data_inicio, duracao, vagas))
            con.commit()
        except:
            print("HOUVE UM ERRO!")
        else:
            print("ADICIONADO!")

    @staticmethod
    def buscar_por_nome():
        return Eventos.buscar_evento(input("Digite o nome do Evento: "))

    @staticmethod
    def buscar_evento(nome):
        try:
            r = c.execute('SELECT * FROM eventos WHERE nome = ?', (nome.upper(),))
            evento = r.fetchone()
        except:
            print('Erro ao fazer consulta')
            evento = None
        finally:
            return evento

    @staticmethod
    def excluir_evento(nome):
        if Eventos.buscar_evento(nome.upper()):
            try:
                c.execute('DELETE FROM eventos WHERE nome = ?', (nome.upper(),))
                con.commit()
                print(f"O evento {nome.upper()} foi excluido com sucesso")
            except:
                print('Erro ao fazer EXCLUSÃO')
        else:
            print("Evento não encontrado")

    @staticmethod
    def ler_campo(valor_atual, campo):
        valor_lido = input(f'{campo}')
        return valor_atual if valor_lido == '' else valor_lido

    @staticmethod
    def atualizar_evento_por_nome(nome):
        evento = Eventos.buscar_evento(nome.upper())
        if evento:
            nome_atual, data_inicio_atual, duracao_atual, vagas_atual = evento
            nome = Eventos.ler_campo(nome_atual, "Novo Nome: ")
            data_inicio = Eventos.ler_campo(data_inicio_atual, "Nova data: ")
            duracao = Eventos.ler_campo(duracao_atual, "Nova Duração: ")
            vagas = Eventos.ler_campo(vagas_atual, "Novo número de vagas: ")
            try:
                c.execute("""UPDATE eventos SET 
                        nome = ?, data_inicio = ?, duracao = ?, vaga = ? WHERE nome = ?""",
                          (nome.upper(), data_inicio, duracao, vagas, nome_atual.upper()))
                con.commit()
                print(f"O evento {nome.upper()} foi atualizado com sucesso")
            except:
                print('Erro ao fazer ATUALIZAÇÃO')
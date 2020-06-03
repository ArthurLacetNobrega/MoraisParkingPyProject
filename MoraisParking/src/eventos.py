from eventos_db import *

def cadastrar_evento():
    print('************ CADASTRAR EVENTO *************')
    Eventos.salvar_evento(input("Nome: "), input("Data de Inicio: "), input("Duracao: "), input("Vagas: "))

def consultar_evento_por_nome():
    print('************ CONSULTAR EVENTO POR NOME *************')
    evento = Eventos.buscar_por_nome()
    if evento:
        print(f'Evento: {evento}')
    else:
        print("Evento não encontrado")

def consultar_eventos():
    print('************ LISTA DE TODOS OS EVENTOS *************')
    for evento in Eventos.all():
        print(f'Evento: {evento}')

def remover_evento():
    print('************ EXCLUSÃO DE EVENTO *************')
    Eventos.excluir_evento(input("Nome do evento:"))

def atualizar_evento():
    print('************ ATUALIZAÇÃO DE EVENTO *************')
    Eventos.atualizar_evento_por_nome(input("Nome do evento:"))
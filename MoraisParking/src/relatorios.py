from sqlite3 import connect

from arrow import utcnow, get
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas

class Relatorios():
    '''Exporta os dados em uma tabela em um pdf'''
    def __init__(self, titulo, cabecalho, dados, nome_arquivo):
        self.titulo = titulo
        self.cabecalho = cabecalho
        self.dados = dados
        self.nome_arquivo = nome_arquivo
        self.estilos = getSampleStyleSheet()


    def converter_dados(self):
        '''Converter os dados em uma lista para criar a tabela em pdf'''
        estilo_cabecalho = ParagraphStyle(name="estilo_cabecalho", alignment=TA_LEFT, fontSize=10, textColor=white,
                                          fontName="Helvetica-Bold", parent=self.estilos["Normal"])

        estilo_normal = self.estilos["Normal"]
        estilo_normal.alignment = TA_LEFT

        chaves, nomes = zip(*[[k, n] for k, n in self.cabecalho])

        cabecalho = [Paragraph(nome, estilo_cabecalho) for nome in nomes]
        novos_dados = [tuple(cabecalho)]

        for dado in self.dados:
            novos_dados.append([Paragraph(str(dado[chave]), estilo_normal) for chave in chaves])

        return novos_dados

    def exportar(self):
        '''Exportar os dados para um pdf'''

        alinhamento_titulo = ParagraphStyle(name="titulo", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=black,
                                          parent=self.estilos["Heading1"])

        self.ancho, self.alto = letter

        converter_dados = self.converter_dados()

        tabela = Table(converter_dados, colWidths=(self.ancho - 100) / len(self.cabecalho), hAlign="CENTER")

        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), black),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Texto centralizado e alinhado à esquerda
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),  # linhas internas
            ("BOX", (0, 0), (-1, -1), 0.25, black),  # Linha) externa
        ]))

        lista = []
        lista.append(Paragraph(self.titulo, alinhamento_titulo))
        lista.append(Spacer(1, 0.16 * inch))
        lista.append(tabela)

        arquivo_pdf = SimpleDocTemplate(self.nome_arquivo, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Relatório", author="Morais' Parking System")

        try:
            arquivo_pdf.build(lista)
            return "Relatório gerado com sucesso!"

        except PermissionError:
            return "Erro inesperado! Permissão negada!"





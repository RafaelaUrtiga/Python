from flask import Flask, flash, request, redirect, url_for, render_template
import xml.etree.ElementTree as ET
import json, csv
from io import TextIOWrapper

app = Flask(__name__)

@app.route("/")
def inicial():
    return render_template ('inicio.html')

        #CRIAÇÃO DA CLASSE
class leitorArquivo:
    
        
        #TRATA O ARQUIVO COM BASE NA EXTENSAO
    def ler_arquivo(self, arquivo):
        extensao = arquivo.filename.split('.')[-1]
        if extensao == 'txt':
            return self.ler_txt(arquivo)
        elif extensao == 'json':
            return self.ler_json(arquivo)
        elif extensao == 'csv':
            return self.ler_csv(arquivo)
        elif extensao == 'xml':
            return self.ler_xml(arquivo)
        else:
            return render_template ('extensao.html')
        
    ###############################################
    ### EXIBE OS CONTEUDOS COM BASE NA EXTENSAO ###
    ###############################################
    def ler_txt(self, arquivo):
        conteudo = arquivo.read()
        return conteudo
        
    ###########################

    def ler_json(self, arquivo):
        conteudo = arquivo.read()

        dados = json.loads(conteudo)
        retorno = ''

        for chave in dados:
            retorno += chave + ': ' + dados[chave] + '\n'

        return retorno

    ###########################


    def ler_csv(self, arquivo):
        
        # Lê os dados do CSV usando o módulo csv
        leitor = csv.reader(TextIOWrapper(arquivo, encoding='utf-8'))

        retorno = '-----------------------------\n'
        for linha in leitor:
            retorno += '|'

            for valor in linha:
                retorno += valor + '|'
            
            retorno += '\n'

        retorno += '-----------------------------'

        return retorno
        
    ###########################

    def ler_xml(self, arquivo):
        try:
            # Parse do XML usando ElementTree
            xml = ET.fromstring(arquivo.read())

            retorno = ''
            # Itera sobre os elementos do XML e exibe seus valores
            for elemento in xml.iter():
                retorno += f"{elemento.tag}: {elemento.text}\n"
        
            return retorno
        except Exception as e:
            return render_template ('xml.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        #### VALIDAÇÕES #####
        #CHECA SE O ARQUIVO FOI ENVIADO PARA UPLOAD 
        if 'arquivo' not in request.files:
            return render_template ('envio.html')
        
        arquivo = request.files['arquivo']
                
        #USUARIO MANDOU VARIAVEL VAZIA
        if arquivo.filename == '':
            return render_template ('vazio.html')
        
        leitor = leitorArquivo()
        resultado = leitor.ler_arquivo(arquivo)
        return resultado

    ### CONTEUDO EXIBIDO APENAS NO METODO  GET PARA TESTES ###
    return render_template ('index.html')
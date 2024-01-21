from flask import Flask, flash, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def inicial():
    return "<h1>Projeto Funcionando.</h1> <p>Envie um arquivo para a rota '/upload'</p>"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        #### VALIDAÇÕES #####
        #CHECA SE O ARQUIVO FOI ENVIADO PARA UPLOAD 
        if 'arquivo' not in request.files:
            return "Não foi enviado arquivo para upload. Envie um arquivo"
        
        arquivo = request.files['arquivo']
                
        #USUARIO MANDOU VARIAVEL VAZIA
        if arquivo.filename == '':
            return "Por favor, selecione um arquivo"

        #TRATA O ARQUIVO COM BASE NA EXTENSAO
        extensao = arquivo.filename.split('.')[-1]
        if (extensao == 'txt'):
            return lerTXT(arquivo)

        elif (extensao == 'json'):
            return lerJSON(arquivo)

        elif (extensao == 'csv'):
            return lerCSV(arquivo)

        elif (extensao == 'xml'):
            return lerXML(arquivo)

        else:
            return 'Arquivo inválido'
        
    ### CONTEUDO EXIBIDO APENAS NO METODO  GET PARA TESTES ###
    return '''
    <!doctype html>
    <title>Faça o upload do arquivo</title>
    <h1>Enviar um arquivo</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=arquivo>
      <input type=submit value=Enviar>
    </form>
    '''

###############################################
### EXIBE OS CONTEUDOS COM BASE NA EXTENSAO ###
###############################################
def lerTXT(arquivo):
    conteudo = arquivo.read()
    return conteudo
    
###########################
import json
def lerJSON(arquivo):
    conteudo = arquivo.read()

    dados = json.loads(conteudo)
    retorno = ''

    for chave in dados:
        retorno += chave + ': ' + dados[chave] + '\n'

    return retorno

###########################
import csv
from io import TextIOWrapper
def lerCSV(arquivo):
    
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
import xml.etree.ElementTree as ET
def lerXML(arquivo):
    try:
        # Parse do XML usando ElementTree
        xml = ET.fromstring(arquivo.read())

        retorno = ''
        # Itera sobre os elementos do XML e exibe seus valores
        for elemento in xml.iter():
            retorno += f"{elemento.tag}: {elemento.text}\n"
    
        return retorno
    except Exception as e:
        return 'Não foi possível ler o arquivo XML'
from pymongo import MongoClient
from environment_variables import getKey
from openai import OpenAI
import random 
import re
from collections import OrderedDict

def tableInterpretationTextGenerator(pergunta, optAndPercentage):

    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    text = f'{pergunta_formatada} \n'
    for options in optAndPercentage.items():
        pct = str(options[1]).replace(".", ",")
        text = f'{text} - {pct}% responderam {options[0]}\n'  
    
    return text

key = getKey()
clientAI = OpenAI(api_key=key)

# print(completion.choices[0].message)

client = MongoClient('localhost',username='root',password='MongoDB2019!')

db = client.cpa
collection = db['curso']


"""
Código para criação de título utilizando a openAI, deixar reservado para utilizar mais tarde.
"""
titulos = []
for document in collection.find().limit(5):
    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',document["pergunta"])
    completion = clientAI.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Escritor de relatório"},
            {"role": "user", "content": f"Transforme a pergunta {pergunta_formatada} na forma de um título sucinto e que não seja indagação"}
        ]
    )
    titulos.append(completion.choices[0].message.content)

respostas = []
for document in collection.find().limit(5):
    inicio_textual = random.choice(["Considerando a Tabela , ","De acordo com a Tabela, ","Pela Tabela ", "Constatou-se pela Tabela que ", "Percebe-se pela Tabela que "])
    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',document["pergunta"])
    temp_dict = document["opcao_e_porcentagem"]
    sorted_dict = dict(sorted(document["opcao_e_porcentagem"].items(), key=lambda x: x[1], reverse=True))
    temp_message = tableInterpretationTextGenerator(pergunta_formatada, sorted_dict)
    print(temp_message)
    completion = clientAI.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é especialista em gramática e possui muito conhecimento na área de redação e escrita"},
            {"role": "user", "content": f"Reescreva na forma de um parágrafo sucinto iniciando com a frase {inicio_textual} o seguinte texto: \n {temp_message} "}
        ]
    )
    respostas.append(completion.choices[0].message.content)

perguntaResposta = {}
for i in range(len(respostas)):
    perguntaResposta.update({f'{titulos[i]}': respostas[i]})

for value in perguntaResposta.items():
    print(f'{value[0]}\n')
    print(f'{value[1]}\n')


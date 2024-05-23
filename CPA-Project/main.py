from pymongo import errors
from database.connectionDB import mongoDBDataBase
from database.python_mongoDB_dbconfig import read_db_config
from src.csvManipulationFunctions.CSVManager import *
from src.generationFunctions.mainGenerator import *
from database.databaseQuerys import df_centro_por_curso,df_centro_por_ano

#Inicializando conexão com o banco de dados
db_config = read_db_config()
client = mongoDBDataBase.connection(db_config)
print("Connection Established with MongoDB")
database = client.cpa

#Criando as collections que serão usadas
curso = database.curso
cursoAtualizado = database['cursoAtualizado2024']
centro_e_curso = database['centro_e_curso']
diretor_e_centro = database['diretor_e_centro']

'''
OBS: DEPOIS CRIAR UM CONTROLLER DE ESCOPO MAIOR PARA CONSEGUIR COBRIR MELHOR AS FUNCOES PARA QUE NAO FIQUE ISSO TUDO,
MAS ESPERAR ACABAR TODA A GERAÇÃO DE RELATÓRIO
'''

# CSVManagment.insertMainCSVtoDatabase(database, cursoAtualizado)
# CSVManagment.insertCursoeCentroCSVtoDatabase(database, centro_e_curso) 
# CSVManagment.insertCentroDiretorCSVDatabase(database, diretor_e_centro)  
# gerarGrafTabRelatorioGPT(curso)
# df_centro_por_curso(database)
df_centro_por_ano(database, 2021)
# gerarRelatoriosPorCentro(curso)
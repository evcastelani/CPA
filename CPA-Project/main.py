from pymongo import errors
from database.connectionDB import mongoDBDataBase
from database.python_mongoDB_dbconfig import read_db_config
from src.csvManipulationFunctions.CSVManager import *
from src.generationFunctions.mainGenerator import *

#Inicializando conexão com o banco de dados
db_config = read_db_config()
client = mongoDBDataBase.connection(db_config)
print("Connection Established with MongoDB")
database = client.cpa

curso = database.curso
centro_e_curso = database['centro_e_curso']
diretor_e_centro = database['diretor_e_centro']

# CSVManagment.insertMainCSVtoDatabase(database, curso)
# CSVManagment.insertCursoeCentroCSVtoDatabase(database, centro_e_curso) 
# CSVManagment.insertCentroDiretorCSVDatabase(database, diretor_e_centro)  
gerarGrafTabRelatorioGPT(curso)
# gerarRelatoriosPorCentro(curso)
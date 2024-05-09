from pymongo import errors
from database.connectionDB import mongoDBDataBase
from database.python_mongoDB_dbconfig import read_db_config
from src.csvManipulationFunctions.CSVManager import *
from src.generationFunctions.mainGenerator import gerarGrafTabRelatorioGPT

#Inicializando conexão com o banco de dados
db_config = read_db_config()
client = mongoDBDataBase.connection(db_config)
print("Connection Established with MongoDB")
database = client.cpa
curso = database.curso

CSVManagment.InsertCSVtoDatabase(database, curso)   
gerarGrafTabRelatorioGPT(curso)
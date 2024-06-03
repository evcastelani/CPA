from pymongo import errors
from database.connectionDB import mongoDBDataBase
from database.connectionDB import connectToDatabase 
from src.csvManipulationFunctions.CSVManager import *
from src.generationFunctions.mainGenerator import *
from src.generationFunctions.relatório.gerarRelatorio import gerarRelatorioPorCurso
from database.databaseQuerys import df_centro_por_curso,df_centro_por_ano

#Inicializando conexão com o banco de dados
database = connectToDatabase()

#Criando as collections que serão usadas (OBS: REALIZAR MUDANÇA BASEADA NO ANO, EX: centro_e_curso_{ano})
curso = database.curso
cursoAtualizado = database['cursoAtualizado2024']
centro_e_curso = database['centro_e_curso']
diretor_e_centro = database['diretor_e_centro']
cursos_por_centro = database['centro_por_curso']
centro_por_ano = database['centro_por_ano_2021'] 

def firstStepApplication():

    #Inserir CSVs no banco de dados
    CSVManagment.insertMainCSVtoDatabase(database, cursoAtualizado)
    CSVManagment.insertCursoeCentroCSVtoDatabase(database, centro_e_curso) 
    CSVManagment.insertCentroDiretorCSVDatabase(database, diretor_e_centro)  

    #Gerar Gráfico, Tabela e Relatório
    gerarGrafTabRelatorioGPT(curso)

def preprocessing():

    #Preprocessamento
    #TALVEZ PREPROCESSAR O CENTRO POR CURSO DE TODOS OS CENTROS, PARA ASSIM JÁ FICAR TUDO PRONTO PARA PRÓXIMA ETAPA
    df_centro_por_curso(database, 2021, 'CCE')


    df_centro_por_ano(database, 2021)


def geraçãoDeRelatorio():
    #Geração dos relatórios
    gerarUmRelatorioTeste('Direito',curso, centro_por_ano, cursos_por_centro, "introducao.md","conclusao.md", 2022, 'CCE')

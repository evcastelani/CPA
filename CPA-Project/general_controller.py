from pymongo import errors
import pymongo.collection
import pymongo.collection
import pymongo.collection
import pymongo.collection
import pymongo.database
from database.connectionDB import connectToDatabase 
from src.csvManipulationFunctions.CSVManager import *
from src.generationFunctions.mainGenerator import *
from src.generationFunctions.relatório.gerarRelatorio import gerarRelatorioPorCurso
from database.databaseQuerys import df_cursos_por_centro,df_centro_por_ano

#Inicializando conexão com o banco de dados
database = connectToDatabase()

#Criando as collections que serão usadas (OBS: REALIZAR MUDANÇA BASEADA NO ANO, EX: centro_e_curso_{ano})
curso = database.curso

cursoAtualizado = database['cursoTeste']
centro_e_curso = database['centro_e_curso']
diretor_e_centro = database['diretor_e_centro']
cursos_por_centro = database['cursos_por_centro']
centro_por_ano = database['centro_por_ano_2021'] 

def firstStepApplication() -> None:
    """
    Função que junta os primeiros passos da execução do programa que seria as inserções e os realiza de uma vez.
    """

    #Inserir CSVs no banco de dados
    
    CSVManagment.insertMainCSVtoDatabase(database, cursoAtualizado)
    # CSVManagment.insertCursoeCentroCSVtoDatabase(database, centro_e_curso) 
    # CSVManagment.insertCentroDiretorCSVDatabase(database, diretor_e_centro)  

    #Gerar Gráfico, Tabela e Relatório
    # gerarGrafTabRelatorioGPT(curso)

def preprocessing(database: pymongo.database, ano: int, collectionCurso: pymongo.collection) -> None:
    """
    Realiza a criação dos dataframes intermediários que são utilizados para a criação de da introdução e 
    conclusão. E os insere em uma collection no banco de dados.

    :param database: Conexão com o banco de dados.
    :type database: Database
    :param ano: Contém o ano que é uma condition para escolhida que tem relação com o ano do arquivo csv
    será feito a leitra.
    :type ano: Integer
    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)    
    """

    #Preprocessamento
    centros = collectionCurso.distinct('centro_de_ensino')
    print(centros)

    document_to_insert = []

    for centro in centros:
        print(centro)
        document_to_insert.extend(df_cursos_por_centro(database, ano, centro))

    database['cursos_por_centro'].insert_many(document_to_insert)

    df_centro_por_ano(database, ano)


def geraçãoDeRelatorio(collectionCurso: pymongo.collection, collectionCentroPorAno: pymongo.collection, collectionCursosPorCentro: pymongo.collection, ano: int) -> None:
    """
    Realiza a criação de relatórios, podendo ser possível escolher se será gerado um único relatório,
    por centro ou todos os relatórios.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param ano: Contém o ano que é uma condition para escolhida que tem relação com o ano do arquivo csv será feito a leitra.
    :type ano: Integer
    """
    opcoes = [1,2,3]

    escolha = int(input('Escolha quantos relatorios você quer gerar com base nas opções: \n 1- Gerar relatórios por centro \n 2- Gerar relatório único \n 3- Gerar todos relatórios\n Escolha: '))
    if escolha not in opcoes:
        print('Digite uma opção válida!')

    if escolha == 1:
        centro = str(input('Digite o nome do centro que gostaria de criar os relatórios: '))    
        gerarRelatoriosPorCentro(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano, centro)
    if escolha == 2:
        curso == str(input('Digite o nome do curso que gostaria de gerar relatório: '))
        gerarUmRelatorio(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano, curso)
    if escolha == 3:
        gerarTodosRelatorios(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano)

def runAplication() -> None:
    """
    Junta todos os passos das funções acima e os realiza em ordem.
    """
    # firstStepApplication()
    ano = int(input('Digite o ano escolhido que será gerado os relatórios: '))
    # preprocessing(database, ano, curso)
    geraçãoDeRelatorio(curso, centro_por_ano, cursos_por_centro, ano)
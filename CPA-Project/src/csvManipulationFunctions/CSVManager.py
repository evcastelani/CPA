from pathlib import Path
import pandas as pd 
import pymongo
from src.supportFunctions.percentageUpdateBD import *

class CSVManagment:

    def maincsv_verifier(verifier, collectionName):
        """
        Função que verifica se os dados do CSV já foram inseridos no banco de dados

        :param verifier: Um valor a ser verificado no banco para ver se os dados já foram inseridos
        :type verifier: String or Int
        :param collectionName: Collection que estamos utilizando
        :type collectionName: Collection
        :return: Boolean que mostra se os dados estão no banco ou não
        :rtype: Boolean
        """
        for document in collectionName.find().limit(1):
            if document["codigo_curso"] == verifier:
                return True
            return False

    def CSVReader():
        """
        Função que retorna o nome do arquivo CSV que será usado.

        :return: Nome do arquivo CSV que será usado
        :rtype: String
        """
        nameArchCSV = input("Digite o nome do arquivo CSV: ")
        return nameArchCSV
    
    def findPath():
        """
        Função que retorna o caminho do diretório que está o arquivo csv

        :return: Path para o arquivo onde está o arquivo CSV
        :rtype: Path
        """
        path = Path(__file__).parent.resolve()
        return path

    def insertMainCSVtoDatabase(database,collectionName):
        """
        Realiza a leitura do arquivo csv transformando ele em um dataframe temporário (OBS: Futuramente talvez seja interessante dropar esse dataframe)
        
        :param database: O banco de dados que será feito as inserções
        :type database: Database
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        """
        csvArchive = CSVManagment.CSVReader()
        dirArquivo = CSVManagment.findPath()
        df = pd.read_csv(f'{dirArquivo}/{csvArchive}', sep=',', header = 0)
        print(df)

        #O cabeçalho terá um formato padrão para evitar erros e problemas futuros, apenas sendo necessário manter a ordem de cada coluna
        cabecalho = (
            'cd_curso', 
            'nm_curso', 
            'centro_de_ensino', 
            'cd_grupo',
            'nm_grupo',
            'cd_subgrupo',
            'nm_subgrupo',
            'cd_disciplina',
            'nm_disciplina',
            'cd_pergunta',
            'nm_pergunta',
            'ordem_opcoes',
            'opcao',
            'respostas',
            'total_do_curso',
            'porcentagem')
        
        if CSVManagment.maincsv_verifier(df.iloc[0,0], collectionName) == True:
            return print("Os dados já foram inseridos no banco!")

        # Neste for estamos iterando o dataframe e coletando as informações para serem inseridas no banco de dados
        for i in range(len(df)):
            print(f"Inserindo infos no banco: %{round(100*i/len(df), 0)}")
            if i < len(df)-1:
                pergunta_anterior = df.iloc[i-1,10]
                pergunta_atual = df.iloc[i,10]
                proxima_pergunta = df.iloc[i+1,10]
                
                if pergunta_atual != pergunta_anterior:
                    temp_pctdict = {}
                    #Inserindo informações iniciais em cada BSON.
                    collectionName.insert_one(
                            {
                            cabecalho[0]: int(df.iloc[i,0]),    #codigo_curso
                            cabecalho[1]:f'{df.iloc[i,1]}',     #nome_do_curso
                            cabecalho[2]: f'{df.iloc[i,2]}',    #centro_de_ensino
                            cabecalho[3]: int(df.iloc[i,3]),    #codigo_grupo
                            cabecalho[4]: str(df.iloc[i,4]),    #nome_grupo
                            cabecalho[5]: int(df.iloc[i,5]),    #codigo_subgrupo
                            cabecalho[6]: f'{df.iloc[i,6]}',    #nome_subgrupo
                            cabecalho[7]: int(df.iloc[i,7]),    #codigo_disciplina
                            cabecalho[8]: str(df.iloc[i,8]),    #nome_disciplina
                            cabecalho[9]: int(df.iloc[i,9]),    #codigo_pergunta 
                            cabecalho[10]: f"{df.iloc[i,10]}",  #nome_pergunta
                            cabecalho[11]: int(df.iloc[i,7]),   #ordem_opcao
                            cabecalho[14]: int(df.iloc[i,14])   #total_do_curso
                            } 
                        )
                    temp_pctdict.update({str(df.iloc[i,12]): int(df.iloc[i,13])})

                elif pergunta_atual != proxima_pergunta:
                    temp_pctdict.update({str(df.iloc[i,12]): int(df.iloc[i,13])})
                    opcao_e_pct = percentageCalculator(temp_pctdict, int(df.iloc[i,14]))
                    insertPercentageDictIntoDB(collectionName,'pct_por_opcao',opcao_e_pct, 'cd_curso', int(df.iloc[i,0]), 'cd_pergunta', int(df.iloc[i,9]))

                temp_pctdict.update({str(df.iloc[i,12]): int(df.iloc[i,13])})

        return print("Inserção dos dados no banco de dados finalizada corretamente ✅")


    def insertCursoeCentroCSVtoDatabase(database, collectionName):
        '''
        Realiza a leitura do csv cursos e centros e faz a inserção dos dados no banco de dados
        
        :param database: O banco de dados que será feito as inserções
        :type database: Database
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        '''
        # csvArchive = CSVManagment.CSVReader()
        csvArchive = 'cursos_e_centros.csv'
        dirArquivo = CSVManagment.findPath()
        df = pd.read_csv(f'{dirArquivo}/{csvArchive}', sep=',', header = 0)

        print(df)

        cabecalho = list(map(lambda x: x.lower(), list(df.columns)))

        print(cabecalho[0])

        for i in range(len(df)):
            print(f"Inserindo infos no banco: %{round(100*i/len(df), 0)}")
            collectionName.insert_one(
                {
                    cabecalho[0]: int(df.iloc[i,0]),
                    cabecalho[1]: float(df.iloc[i,1]),
                    cabecalho[2]: str(df.iloc[i,2]),
                    cabecalho[3]: str(df.iloc[i,3]),
                    cabecalho[4]: int(df.iloc[i,4]),
                    cabecalho[5]: int(df.iloc[i,5])
                }
            )
        return print("Inserção dos dados no banco de dados finalizada corretamente ✅")



    def insertCentroDiretorCSVDatabase(database, collectionName):
        '''
        Realiza a leitura do csv centro e diretor e faz a inserção dos dados no banco de dados
        
        :param database: O banco de dados que será feito as inserções
        :type database: Database
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        '''
        # csvArchive = CSVManagment.CSVReader()
        csvArchive = 'centros_e_diretores.csv'
        dirArquivo = CSVManagment.findPath()
        df = pd.read_csv(f'{dirArquivo}/{csvArchive}', sep=',', header = 0)

        cabecalho = list(map(lambda x: x.lower(), list(df.columns)))
        
        for i in range(len(df)):
            collectionName.insert_one(
                {
                    cabecalho[0]: str(df.iloc[i,0]),
                    cabecalho[1]: str(df.iloc[i,1]),
                    cabecalho[2]: str(df.iloc[i,2]),
                    cabecalho[3]: str(df.iloc[i,3]),
                    cabecalho[4]: str(df.iloc[i,4]),
                }
            )
        return print("Inserção dos dados no banco de dados finalizada corretamente ✅")

    
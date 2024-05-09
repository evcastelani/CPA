from pathlib import Path
import pandas as pd 
import pymongo
from src.supportFunctions.percentageUpdateBD import *

class CSVManagment:

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

    def InsertCSVtoDatabase(database,collectionName):
        """
        Realiza a leitura do arquivo csv transformando ele em um dataframe temporário (OBS: Futuramente talvez seja interessante dropar esse dataframe)
        
        :param database: O banco de dados que será feito as inserções
        :type database: Database
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        """
        csvArchive = CSVManagment.CSVReader()
        dirArquivo = CSVManagment.findPath()
        df = pd.read_csv(f'{dirArquivo}/{csvArchive}', sep=';', header = 0)

        cabecalho = list(map(lambda x: x.lower(), list(df.columns)))
        print(cabecalho)
        #Filtragem do dataframe
        print(df)

        # Neste for estamos iterando o dataframe e coletando as informações para serem inseridas no banco de dados
        for i in range(len(df)):
            print(f"Inserindo infos no banco: %{round(100*i/len(df), 0)}")
            if i < len(df)-1:
                pergunta_anterior = df.iloc[i-1,6]
                pergunta_atual = df.iloc[i,6]
                proxima_pergunta = df.iloc[i+1,6]
                
                if pergunta_atual != pergunta_anterior:
                    temp_pctdict = {}
                    #Inserindo informações iniciais em cada BSON.
                    collectionName.insert_one(
                            {
                            cabecalho[0]: int(df.iloc[i,0]),
                            cabecalho[1]:f'{df.iloc[i,1]}',
                            cabecalho[2]: f'{df.iloc[i,2]}',
                            cabecalho[3]: int(df.iloc[i,3]),
                            cabecalho[4]: f'{df.iloc[i,4]}',
                            cabecalho[5]: int(df.iloc[i,5]),
                            cabecalho[6]: f"{df.iloc[i,6]}", 
                            cabecalho[7]: int(df.iloc[i,7]),
                            cabecalho[11]: int(df.iloc[i,11])
                            } 
                        )
                    temp_pctdict.update({str(df.iloc[i,8]): int(df.iloc[i,10])})

                elif pergunta_atual != proxima_pergunta:
                    temp_pctdict.update({str(df.iloc[i,8]): int(df.iloc[i,10])})
                    opcao_e_pct = percentageCalculator(temp_pctdict, int(df.iloc[i,11]))
                    insertPercentageDictIntoDB(collectionName,'pct_por_opcao',opcao_e_pct, 'codigo_curso', int(df.iloc[i,0]), 'nu_pergunta', int(df.iloc[i,5]))

                temp_pctdict.update({str(df.iloc[i,8]): int(df.iloc[i,10])})

        print("Inserção dos dados no banco de dados finalizada corretamente ✅")
            
            
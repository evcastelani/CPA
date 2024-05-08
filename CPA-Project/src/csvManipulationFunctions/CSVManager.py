from pathlib import Path
import pandas as pd 
import pymongo

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

        #Filtragem do dataframe
        print(df)

        #Neste for estamos iterando o dataframe e coletando as informações para serem inseridas no banco de dados
        for i in range(len(df)):
            print(f"Inserindo infos no banco: %{round(100*i/len(df), 0)}")
            temp_dict = {str(df.iloc[i,8]): int(df.iloc[i,10])}
            if i < len(df)-1:
                pergunta_anterior = df.iloc[i-1,6]
                pergunta_atual = df.iloc[i,6]
                
                if pergunta_atual != pergunta_anterior:
                    #Inserindo informações iniciais em cada BSON.
                    collectionName.insert_one(
                            {
                            'Codigo_Curso': int(df.iloc[i,0]),
                            'Nome_do_Curso':f'{df.iloc[i,1]}',
                            'Centro_de_ensino': f'{df.iloc[i,2]}',
                            'cd_subgrupo': int(df.iloc[i,3]),
                            'nm_subgrupo': f'{df.iloc[i,4]}',
                            'nu_pergunta': int(df.iloc[i,5]),
                            'pergunta': f"{df.iloc[i,6]}", 
                            'Ordem_opcoes': int(df.iloc[i,7]),
                            'opcao_e_qtdResposta': temp_dict,
                            'TotalResp_do_Curso': int(df.iloc[i,11])
                            } 
                        )
                else:
                    #Incrementando os arrays de opcao e porcentagem utilizando o update.
                    database.curso.update_one(
                        {
                            'Codigo_Curso': int(df.iloc[i,0]),    
                            'nu_pergunta': int(df.iloc[i,5])
                        },
                        {
                            '$set': {f'opcao_e_qtdResposta.{str(df.iloc[i,8])}': int(df.iloc[i,10])}
                        }
                    )
            elif i == len(df)-1:
                database.curso.update_one(
                    {
                        'Codigo_Curso': int(df.iloc[i,0]),
                        'nu_pergunta': int(df.iloc[i,5])
                    },
                    {
                        '$set': {f'opcao_e_qtdResposta.{str(df.iloc[i,8])}': int(df.iloc[i,10])}
                 
                    }
                )
        print("Inserção dos dados no banco de dados finalizada corretamente ✅")
            
            
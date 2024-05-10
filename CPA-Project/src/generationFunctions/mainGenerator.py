from src.supportFunctions.dictToTwoLists import dictToList
from src.generationFunctions.graph.graphGenerator import controllerGraphGenerator
from src.generationFunctions.text.textFunctions import composeTable
from src.openAI.openAIFunctions import *

def gerarGrafTabRelatorioGPT(collectionName):
    """
    Função controller que chama as outras funções para gerar o gráfico, a tabela e as legendas e reports para o relatório

    :param CollectionName: Paramêtro que chama a collection na qual estamos trabalhando
    :type CollectionName: Collection
    """
    index = 1
    for document in collectionName.find().limit(4):
        pergunta_formatada = pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',document["pergunta"])
        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
        opcoes, pct = dictToList(sorted_pctOptDict)
        path = controllerGraphGenerator(collectionName, opcoes, pct, document["codigo_curso"], document["cd_subgrupo"], document["nu_pergunta"], pergunta_formatada)
        table = composeTable(pergunta_formatada, sorted_pctOptDict)
        reportGraph = createReport(pergunta_formatada, sorted_pctOptDict, index)
        captionGraph = createCaption(pergunta_formatada)

        collectionName.update_one(
            {
                "codigo_curso": document["codigo_curso"],
                "nu_pergunta": document["nu_pergunta"]
            },
            {
                '$set': {
                    'path': path,
                    'tabela': table,
                    'relatorioGraficoGPT': reportGraph,
                    'legendaGraficoGPT': captionGraph  
                }
            }
        )
        index += 1



def gerarTodosRelatorios():
    ...

def gerarRelatorioCurso():
    ...

def gerarRelatorioPorCentro():
    ...
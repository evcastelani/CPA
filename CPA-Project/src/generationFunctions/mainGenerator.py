from src.supportFunctions.dictToTwoLists import dictToList
from src.generationFunctions.graph.graphGenerator import controllerGraphGenerator
from src.generationFunctions.text.textFunctions import composeTable
from src.openAI.openAIFunctions import *
from src.generationFunctions.relatório.compor_partes_relatorio import *
from src.generationFunctions.relatório.gerarRelatorio import gerarRelatorioPorCurso
import sys
sys.stdout.reconfigure(encoding="utf-8")

def gerarGrafTabRelatorioGPT(collectionName):
    """ 
    Função controller que chama as outras funções para gerar o gráfico, a tabela e as legendas e reports para o relatório

    :param CollectionName: Paramêtro que chama a collection na qual estamos trabalhando
    :type CollectionName: Collection
    """
    for document in collectionName.find({'relatorioGraficoGPT': {'$exists': False}}):
        pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',document["pergunta"])
        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
        opcoes, pct = dictToList(sorted_pctOptDict)
        path = controllerGraphGenerator(collectionName, opcoes, pct, document["codigo_curso"], document["cd_subgrupo"], document["nu_pergunta"], pergunta_formatada)
        # table = composeTable(pergunta_formatada, sorted_pctOptDict)
        reportGraph = createReport(pergunta_formatada, sorted_pctOptDict)
        # captionGraph = createCaption(pergunta_formatada)

        collectionName.update_one(
            {
                "codigo_curso": document["codigo_curso"],
                "nu_pergunta": document["nu_pergunta"]
            },
            {
                '$set': {
                    'path': path
                    # 'tabela': table,
                    # 'relatorioGraficoGPT': reportGraph,
                    # 'legendaGraficoGPT': captionGraph  
                }
            }
        )

def teste(collectionName):
    for document in collectionName.find():
        pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',document["pergunta"])
        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
        opcoes, pct = dictToList(sorted_pctOptDict)
        reportGraph = createReport(pergunta_formatada, sorted_pctOptDict)

        
def gerarTodosRelatorios(collectionName):
    cursos = collectionName.distinct("nome_do_curso")
    for nome_curso in cursos:
        #Aqui entra a função de gerarRelatorioCurso
        print(nome_curso)



def gerarRelatoriosPorCentro(collectionName):
    centro_de_ensino = str(input("Digite o centro de ensino que deseja escolher para gerar os relatórios: "))
    result = collectionName.distinct('nome_do_curso', {'centro_de_ensino': centro_de_ensino})
    for nome_cursos in result:
        ...
        #Aqui entra função gerarRelatorioCurso



def gerarUmRelatorioTeste(cursoEscolhido,collectionCurso ,collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, arquivo_conclusao, ano, centro_de_ensino):
    compor_introducao(collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, ano, centro_de_ensino)
    compor_conclusão(collectionCursosPorCentro, arquivo_conclusao, ano)
    gerarRelatorioPorCurso(cursoEscolhido, collectionCurso, collectionCursosPorCentro)
    
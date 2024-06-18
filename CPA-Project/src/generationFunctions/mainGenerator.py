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
        pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["pergunta"])
        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
        opcoes, pct = dictToList(sorted_pctOptDict)
        path = controllerGraphGenerator(collectionName, opcoes, pct, document["codigo_curso"], document["cd_subgrupo"], document["nu_pergunta"], pergunta_formatada)
        table = composeTable(pergunta_formatada, sorted_pctOptDict)
        # reportGraph = createReport(pergunta_formatada, sorted_pctOptDict) Funçao obsoleta, trocar dps
        # captionGraph = createCaption(pergunta_formatada) Função obsoleta, trocar dps

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

        
def gerarTodosRelatorios(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, arquivo_conclusao, ano):
    """
    Gera relatório de todos os cursos.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer

    """
    centros = collectionCurso.distinct('centro_de_ensino')
    for centro in centros:
        gerarRelatoriosPorCentro(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, arquivo_conclusao, ano, centro)

        


def gerarRelatoriosPorCentro(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, arquivo_conclusao, ano, centro_de_ensino):
    """
    Gera relatórios dos cursos pertencentes a um centro.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param centro_de_ensino: Centro de ensino escolhido para gerar os relatórios dos cursos pertencentes ao mesmo
    :type centro_de_ensino: String
    """
    compor_introducao(collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, ano, centro_de_ensino)
    compor_conclusão(collectionCursosPorCentro, arquivo_conclusao, ano)

    cursos = collectionCurso.distinct('nome_do_curso', {'centro_de_ensino': centro_de_ensino})
    print(cursos)
    for curso in cursos:
        gerarRelatorioPorCurso(curso, collectionCurso, collectionCursosPorCentro)
        cursoArquivo = f'{curso}.md'
        substituir_identificadores(cursoArquivo)



def gerarUmRelatorio(collectionCurso: pymongo.collection, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, arquivo_conclusao, ano, curso): # type: ignore

    document = collectionCurso.find_one({'nome_do_curso': curso}, {'centro_de_ensino': 1, 'id': 0})
    print(document['centro_de_ensino'])
    # compor_introducao(collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, ano, centro)
    # compor_conclusão(collectionCursosPorCentro, arquivo_conclusao, ano)
    
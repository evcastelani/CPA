from src.supportFunctions.dictToTwoLists import dictToList
from src.generationFunctions.graph.graphGenerator import controllerGraphGenerator
from src.generationFunctions.text.textFunctions import composeTable
from src.openAI.openAIFunctions import *
import os

def gerarGrafTabRelatorioGPT(collectionName):
    """
    Função controller que chama as outras funções para gerar o gráfico, a tabela e as legendas e reports para o relatório

    :param CollectionName: Paramêtro que chama a collection na qual estamos trabalhando
    :type CollectionName: Collection
    """
    for document in collectionName.find({'relatorioGraficoGPT': {'$exists': False}}):
        pergunta_formatada = pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',document["pergunta"])
        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
        opcoes, pct = dictToList(sorted_pctOptDict)
        path = controllerGraphGenerator(collectionName, opcoes, pct, document["codigo_curso"], document["cd_subgrupo"], document["nu_pergunta"], pergunta_formatada)
        table = composeTable(pergunta_formatada, sorted_pctOptDict)
        reportGraph = createReport(pergunta_formatada, sorted_pctOptDict)
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


def gerarRelatorioCurso(curso_escolhido, collectionName):
    arquivo = open(f'{curso_escolhido}.md', 'w')
    print('---', file=arquivo)
    print(f'title: \'Relatório do Curso de {curso_escolhido}\'', file=arquivo)
    print('titlepage: \"true\"', file=arquivo)
    print('titlepage-background: \"capa\"', file=arquivo)
    print('titlepage-rule-color: \"B3B3B3\"', file=arquivo)
    print('page-background: \"interna02\"', file=arquivo)
    print('page-background-opacity: \"1.0\"', file=arquivo)
    print('author: [CPA-Comissão Própria de Avaliação]', file=arquivo)
    print('lang: \"pt-BR\" ', file=arquivo)
    print('...', file=arquivo)
    print('', file=arquivo)

    #Precisa criar a função que compõe a introdução

    for document in collectionName.find({'nome_do_curso': curso_escolhido}):
        arquivo.write(f"![{document['legendaGraficoGPT']}](Imagens/{document['path']}) \n")
        print(' ', file=arquivo)
        print(f"Tabela index_- {document['legendaGraficoGPT']} \n", file=arquivo)
        arquivo.write(document['tabela'])
        arquivo.write('\n')
        print(' ', file=arquivo)
        print(document['relatorioGraficoGPT'])
        print(f"Edição da pergunta {document['nu_pergunta']} do subgrupo {document['cd_subgrupo']} do curso {document['nome_do_curso']} concluida com sucesso!")
    
    #Apenas falta a parte da conclusão
        
        
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
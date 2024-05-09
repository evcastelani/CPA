import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from src.supportFunctions.dictToTwoLists import dictToList
import os
from PIL import Image


def percentage_plot(pct, allvalues):
    """
    Função para plotar a porcentagem no gráfico de forma visual

    :param pct: Valor usado para realizar o calculo absoluto da porcentagem
    :type pct: Int
    :param allvalues: List contendo as porcentagens
    :type allvalues: List
    :return: retorna as porcentagnes para serem plotadas no gráfico
    :rtype: Int
    """
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.2f}%".format(pct, absolute) if pct > 0 else ''

def graphPlot(dirSaidaFig,cod_curso, cod_subgrupo, options,percentage, num_pergunta, pergunta):
    """
    Função que cria a figura do gráfico

    :param dirSaidaFig: Contém o path para o diretório onde será salvado as figuras.
    :type dirSaidaFig: Path
    :param cod_curso: Contém o codigo do curso que será utilizado para formar o nome da figura
    :type cod_curso: String
    :param cod_subgrupo: Contém o código do sub grupo que será utilizado para formar o nome da figura
    :type cod_subgrupo: String
    :param options: List que contém as opções de respostas que poderiam ser escolhidas
    :type options: List
    :param percentage: List que contém as porcentagens de cada opção que foi escolhida
    :type percentage: List
    :param num_pergunta: Contém o número da pergunta que será utilizado para formar o nome da figura
    :type num_pergnta: String
    :param pergunta: É a pergunta que dará título para a figura que contém o gráfico
    :type pergunta: String
    """

    figGraph_name = f'fig_{cod_curso}_{cod_subgrupo}_{num_pergunta}'
    print(figGraph_name)

    labelLegend = [f'{l}, {s}%' for l, s in zip(options, percentage)]

    wp = {'linewidth': 1, 'edgecolor': "black"}

    fig, ax = plt.subplots(figsize=(13, 7))

    wedges, texts, autotexts = ax.pie(percentage,
                                    autopct=lambda pct: percentage_plot(pct, percentage),
                                    labels=options,
                                    shadow=True,
                                    startangle=90,
                                    wedgeprops=wp,
                                    textprops=dict(color="white"))

    ax.legend(
            title="Opções",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            labels = labelLegend
            )

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(f"{pergunta}") 
    fig.savefig(os.path.join(dirSaidaFig, figGraph_name))
    plt.close(fig)

    path = f'{dirSaidaFig}/{figGraph_name}'
    return path


def controllerGraphGenerator(collectionName, opcoes, porcentagem, cod_curso, cd_subgrupo, nu_pergunta, pergunta):
    """
    Função que realiza a chamada da função que gera os gráficos para cada documento que estiver no banco de dados.

    :param collectionName: Coleção que contém os documentos que iremos realizar a inserção
    :type collectionName: Collection 
    """

    #Realizando a busca pelo caminho para o diretório em que serão salvos as figuras
    diretorio_trabalho = os.getcwd()
    subdiretorio_trabalho = 'Figuras_Graficos'

    diretorio_saida_figura = os.path.join(diretorio_trabalho, subdiretorio_trabalho)

    if not os.path.exists(diretorio_saida_figura):
        os.makedirs(diretorio_saida_figura)

    finalPath = graphPlot(diretorio_saida_figura, cod_curso, cd_subgrupo, opcoes, porcentagem, nu_pergunta, pergunta)
    
    return finalPath

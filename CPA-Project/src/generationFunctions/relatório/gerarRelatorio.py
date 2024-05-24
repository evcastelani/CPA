def gerarRelatorioPorCurso(curso_escolhido, collectionName):
    #Talvez separar parte inicial para virar uma função compor capa
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

    #-------------------------------- VIRA UMA FUNÇÃO ----------------------------
    for document in collectionName.find({'nome_do_curso': curso_escolhido}):
        # if document['codigo_disciplina'] == '-':

        arquivo.write(f"![{document['legendaGraficoGPT']}](Imagens/{document['path']}) \n")
        print(' ', file=arquivo)
        print(f"Tabela index_- {document['legendaGraficoGPT']} \n", file=arquivo)
        arquivo.write(document['tabela'])
        arquivo.write('\n')
        print(' ', file=arquivo)
        print(document['relatorioGraficoGPT'])
        print(f"Edição da pergunta {document['nu_pergunta']} do subgrupo {document['cd_subgrupo']} do curso {document['nome_do_curso']} concluida com sucesso!")
    
    for document in collectionName.find({'nome_do_curso': curso_escolhido}):
        # if document['codigo_disciplina'] != '-':
        ...
    #------------------------------------VIRA UMA FUNÇÃO ----------------------------

    #Apenas falta a parte da conclusão
import pystache

def compor_introducdao(collectionCursoPorAno,collectionCentroPorCurso, arquivo_intro, ano):
    ...
    template = pystache.parse_file(arquivo_intro)
    tabela_centros = "| Sigla | Centro   | Resp. | Matr.   |  %   |\n |------|:----:|:-----:|:---:|:---:| \n"
    for document in collectionCursoPorAno.find():
        respondentes_total += document['respondentes']
        matriculas_totais += document['matriculas']
        tabela_centros += f'| {document['centro_de_ensino']}'
        tabela_centros += f'| {document['centro_descricao']}'    
        tabela_centros += f'| {document['respondentes']}'    
        tabela_centros += f'| {document['matriculados']}'
        tabela_centros += f'| {document['porcentgem']}'    
        tabela_centros += '| \n'    
        
    participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
    
    tabela_cursos = df_2_tabela_cursos = "| Curso |  Resp. |Matr.|   %   | \n |------|:-----:|:-----:|:---:| \n "
    for document in collectionCentroPorCurso.find():
        tabela_cursos += f'| {document['nome_do_curso']}'
        tabela_cursos += f'| {document['respondentes']}'
        tabela_cursos += f'| {document['matriculados']}'
        tabela_cursos += f'| {document['porcentagem']}'
        tabela_cursos += '| \n'

    participacao_uem_virgula = participacao_uem.replace('.', ',')
    intro = pystache.render(template, {'tabela_centros': tabela_centros, 'tabela_cursos_por_centro': tabela_cursos, 'ano': ano, 'curso': '{{curso}}', 'participacao_uem': participacao_uem_virgula, 'participacao_curso': '{{participacao_curso}}'})
    with open("info_introducao.md", "w") as arquivo:
        arquivo.write(f'{intro} \n')
    

def compor_conclusão(collectionName, arquivo_conclusao, ano):
    template = pystache.parse_file(arquivo_conclusao)
    for document in collectionName.find():
        respondentes_total = document['respondentes']
        matriculas_totais = document['matriculas']
    
    participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
    participacao_uem_virgula = participacao_uem.replace('.', ',')
    conclusao = pystache.render(template, {'ano': ano, 'curso': '{{curso}}', 'participacao_uem': participacao_uem_virgula})
    
def compor_conteudoRelatório(colletionName, arquivo_intro):
    ...
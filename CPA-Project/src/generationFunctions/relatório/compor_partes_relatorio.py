import pystache
from src.supportFunctions.ponto_2_virgula import ponto_2_virgula 
import sys
sys.stdout.reconfigure(encoding="utf-8")


def compor_introducao(collectionCursoPorAno,collectionCursosPorCentro, arquivo_intro, ano, centro_de_ensino):
    with open(f'CPA-Project/components/{arquivo_intro}','r',encoding='utf-8') as f:
        template = f.read()
    renderer = pystache.Renderer()
    respondentes_total = 0
    matriculas_totais = 0
    
    tabela_centros = "| Sigla | Centro   | Resp. | Matr.   |  %   |\n |------|:----:|:-----:|:---:|:---:| \n"
    for document in collectionCursoPorAno.find():
        respondentes_total += document['respondentes']
        matriculas_totais += document['matriculados']
        tabela_centros += f'| {document['centro_de_ensino']}'
        tabela_centros += f'| {document['centro_descricao']}'    
        tabela_centros += f'| {document['respondentes']}'    
        tabela_centros += f'| {document['matriculados']}'
        tabela_centros += f'| {document['porcentagem']}'    
        tabela_centros += '| \n'    
        
    participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
    
    tabela_cursos = df_2_tabela_cursos = "| Curso |  Resp. |Matr.|   %   | \n |------|:-----:|:-----:|:---:| \n "
    for document in collectionCursosPorCentro.find({'centro_de_ensino': centro_de_ensino}):
        tabela_cursos += f'| {document['nome_do_curso']}'
        tabela_cursos += f'| {document['respondentes']}'
        tabela_cursos += f'| {document['matriculados']}'
        tabela_cursos += f'| {document['porcentagem']}'
        tabela_cursos += '| \n'

    intro = renderer.render(template, {'tabela_centros': tabela_centros, 'tabela_cursos_por_centro': tabela_cursos, 'ano': ano, 'curso': '{{curso}}', 'participacao_uem': ponto_2_virgula(participacao_uem), 'participacao_curso': '{{participacao_curso}}'})
    print(intro)
    with open("info_introducao.md", "w", encoding='utf-8') as arquivo:
        arquivo.write(f'{intro} \n')
    

def compor_conclusão(collectionNameCursosPorCentro, arquivo_conclusao, ano):
    with open(f'CPA-Project/components/{arquivo_conclusao}', 'r', encoding='utf-8') as f:
        template = f.read()
    renderer = pystache.Renderer()
    for document in collectionNameCursosPorCentro.find():
        respondentes_total = document['respondentes']
        matriculas_totais = document['matriculados']
    
    participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
    conclusao = renderer.render(template, {'ano': ano, 'curso': '{{curso}}', 'participacao_uem': ponto_2_virgula(participacao_uem)})
    with open("info_conclusao.md","w", encoding='utf-8') as arquivo:
        arquivo.write(f'{conclusao} \n')
    

def compor_conteudoRelatório(colletionName, arquivo_intro):
    ...


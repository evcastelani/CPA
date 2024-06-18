import pystache
import re
from src.supportFunctions.ponto_2_virgula import ponto_2_virgula 
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")


def compor_introducao(collectionCentroPorAno,collectionCursosPorCentro, arquivo_intro, ano, centro_de_ensino):
    """
    Gera um arquivo markdown contendo as informações da introdução do relatório.

    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param centro_de_ensino: Nome do centro de ensino escolhido para a geração da tabela contendo os seus cursos
    :type centro_de_ensino: String
    """
    with open(f'CPA-Project/relatorio-components/{arquivo_intro}','r',encoding='utf-8') as f:
        template = f.read()
    renderer = pystache.Renderer()
    respondentes_total = 0
    matriculas_totais = 0
    
    tabela_centros = "| Sigla | Centro   | Resp. | Matr.   |  %   |\n |------|:----:|:-----:|:---:|:---:| \n"
    for document in collectionCentroPorAno.find():
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
    """
    Compõe a conclusão criando um arquivo markdown com base no template já existente, substituindo
    valores e criando as tabelas usadas no mesmo.

    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer

    """
    with open(f'CPA-Project/relatorio-components/{arquivo_conclusao}', 'r', encoding='utf-8') as f:
        template = f.read()
    renderer = pystache.Renderer()
    for document in collectionNameCursosPorCentro.find():
        respondentes_total = document['respondentes']
        matriculas_totais = document['matriculados']
    
    participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
    conclusao = renderer.render(template, {'ano': ano, 'curso': '{{curso}}', 'participacao_uem': ponto_2_virgula(participacao_uem)})
    with open("info_conclusao.md","w", encoding='utf-8') as arquivo:
        arquivo.write(f'{conclusao} \n')
    

def substituir_identificadores(filename):
    # Lê o conteúdo do arquivo
    directory = Path('relatorio')
    file = f'{directory}/{filename}'

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Encontra todos os identificadores e substitui por números sequenciais
    index = 1
    def replace_index(match):
        nonlocal index
        replacement = f'tabela {index}'
        index += 1
        return replacement
    
    # Substitui todas as ocorrências de 'tabela _index'
    new_content = re.sub(r'tabela _index', replace_index, content)

    # Salva o novo conteúdo no mesmo arquivo ou em um novo arquivo
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(new_content)




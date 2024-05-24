from mustache import Mustache

def compor_introducdao(collectionCursoPorAno,collectionCentroPorCurso, arquivo_intro):
    ...
    template = Mustache(open(arquivo_intro).read())
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
        
    participacao_uem = round(100 * (respondentes_total/matriculas_totais), 1)
        



def compor_conclusão(collectionName, arquivo_intro):
    ...

def compor_conteudoRelatório(colletionName, arquivo_intro):
    ...
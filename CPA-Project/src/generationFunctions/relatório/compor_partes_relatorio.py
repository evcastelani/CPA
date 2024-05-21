import chevron

def compor_introducdao(collectionName, arquivo_intro):
    ...
    with open('introducao.md', 'r') as intro: 
        chevron.render(intro, {'mustache': 'intro'})
        df_2_tabela_centros = "| Sigla | Centro   | Resp. | Matr.   |  %   |\n |------|:----:|:-----:|:---:|:---:| \n"

def compor_conclusão(collectionName, arquivo_intro):
    ...

def compor_conteudoRelatório(colletionName, arquivo_intro):
    ...
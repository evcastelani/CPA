import re

def tableInterpretationTextGenerator(pergunta, optAndPercentage):
    """
    Função que cria um texto contendo uma pergunta, as opções e as porentagens

    :param pergunta: Será utilizado como título para o texto formado
    :type pergunta: String
    :param optAndPercentage: Contém as opções e suas respectivas porcentagens em um dicionário
    :type optAndPercentage: Dict
    :return: Texto que contendo tudo de maneira formatada para que uma IA possa interpretar de maneira correta
    :rtype: String
    """

    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    text = f'{pergunta_formatada} \n'
    for options in optAndPercentage.items():
        pct = str(options[1]).replace(".", ",")
        text = f'{text} - {pct}% responderam {options[0]}\n'  
    
    return text


def composeTable(pergunta, optAndPercentage):
    """
    Função que realiza a composição de uma tabela contendo as opções e porcentagens

    :param pergunta: Utilizado para identificação da tabela que foi criada
    :type pergunta: String
    :param optAndPercentage: Contém as opções e suas respectivas porcentagens em um dicionário
    :type optAndPercentage: Dict
    :return: Uma tabela formada em markdown
    :rtype: String
    """
    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    s = "| indicador |"
    for tuple in optAndPercentage.items():
        s = f'{s} {tuple[0]} |'

    s = f'{s} \n|---|'
    for tuple in optAndPercentage.items():
        s =  f'{s}---|'

    s = f'{s} \n| {pergunta_formatada} |'
    for tuple in optAndPercentage.items():
        pct = str(tuple[1]).replace('.', ',')
        s = f'{s} {pct}% | '         

    return s

opcao_e_porcentagem = {
        'Ótimo': 70.83,
        'Bom': 20.83,
        'Regular': 4.17,
        'Ruim': 4.17,
        'Péssimo': 0
    }

temp = tableInterpretationTextGenerator('1.2- Sua frequência nas disciplinas remotas', opcao_e_porcentagem)
print(temp)
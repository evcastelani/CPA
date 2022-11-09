# CPA

Este repositório foi criado para desenvolvimento de um pacote computacional para geração de relatórios automatizados para uso da CPA-UEM. 

# Uso básico
Este pacote está em fase inicial. Dessa forma, poucas funções foram implementadas. Como o pacote é escrito em linguagem Julia, a primeira coisa que deve ser feita é instalar a citada linguagem. Para isso, basta acessar [este link](https://julialang.org/) e seguir as instruções. Uma vez instalada a linguagem, para instalar o pacote CPA e suas dependências, basta acessar o Julia REPL e apertar a tecla ']' para acessar o gerenciador de pacotes. Em seguida, dentro do REPL, digite o comando abaixo:

```julia
Pkg> add https://github.com/evcastelani/CPA
```

Se tudo ocorreu corretamente, o módulo e suas dependências foram instalados corretamente. Agora, para carregar o pacote suas funções, novamente dentro do REPL, digitar o seguinte comando:

```julia
julia> using CPA
```

# Créditos

- Dioclecio Camelo
- Emerson Vitor Castelani

# TODO

1. [ ] Escrever doc string em cada função criada;
1. [ ] Inserir um template mais completo;
1. [ ] Criar uma função que permita, de alguma forma, inserir repetições no template;
1. [ ] Criar uma função que exporte para LaTeX ou Markdown.


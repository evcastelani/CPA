using Mustache, CSV, DataFrames, ReplGPT, SQLdf
using PyPlot,Unicode


##############################################################################
# Esta parte do código corresponde ao "módulo CPA"                           #
##############################################################################
function agrupamento(filename)
    Df = DataFrame[]
    if isa(filename,String)
        Df = CSV.read(filename,DataFrame)
    else 
        Df = filename 
    end
    N = groupby(Df,"nome_do_curso")
    tam_N = N.groups[end]
    V = []
    for i = 1:tam_N 
        S = groupby(N[i],"cd_subgrupo")
        tam_S = S.groups[end]
        for j=1:tam_S
            P = groupby(S[j],"nu_pergunta")
            tam_P = P.groups[end]
            for k=1:tam_P
                push!(V,P[k])
            end
        end
    end
    return Info_de_Curso.(V)

end

"""
    Info_de_Curso

Esse objeto encarrega-se de armazenar as informações de um dado curso que serão passadas para a função interpola. 

# Exemplo
```
julia-repl
julia> C = Info_de_Curso("MATEMATICA",10,23)

retorna um objeto C que será usado posteriormente pela função interpola
```
"""
struct Info_de_Curso
    bloco :: DataFrames.DataFrame
    #     #
    nome_do_curso :: String
    codigo_subgrupo:: Int64
    nome_subgrupo:: String
    numero_pergunta :: Int64 
    pergunta :: String
    ordem_opcoes :: Vector{Int64}
    opcoes :: Vector{String}
    porcentagem:: Vector{Float64}
    respostas:: Vector{Int64}
    total_do_curso :: Int64
    texto :: String 
    grafico :: String 
    tabela :: String
    function Info_de_Curso(_bloco)
        _nome_do_curso = String.(rstrip(_bloco[:,"nome_do_curso"][1,1]))
        _codigo_subgrupo = _bloco[:,"cd_subgrupo"][1,1]
        _nome_subgrupo = _bloco[:,"nm_subgrupo"][1,1]
        _numero_pergunta = _bloco[:,"nu_pergunta"][1,1]
        _pergunta = String(rstrip(replace(_bloco[:,"pergunta"][1,1],r"^\d+\.\d+\-\s*"=>"")))
        _ordem_opcoes = _bloco[:,"ordem_opções"]
        _opcoes = String.(_bloco[:,"opção"])
        #_porcentagem = corrigir_porcentagem(parse.(Float64,replace.(_bloco[:,"porcentagem"],","=>".")))
        _porcentagem = corrigir_porcentagem(_bloco[:,"porcentagem"])
        _respostas = _bloco[:,"respostas"]
        _total_do_curso = _bloco[:,"total_do_curso"][1,1]
        _texto = compor_sentenca(_pergunta,_opcoes,_porcentagem)
        _grafico = compor_grafico(_nome_do_curso,_codigo_subgrupo,_numero_pergunta,_pergunta,_opcoes,_porcentagem)
        _tabela = compor_tabela(_pergunta,_opcoes,_porcentagem)
        new(_bloco,_nome_do_curso,_codigo_subgrupo,_nome_subgrupo,_numero_pergunta,_pergunta,_ordem_opcoes,_opcoes,_porcentagem,_respostas,_total_do_curso,_texto,_grafico,_tabela)
    end
end

function corrigir_porcentagem(_porcentagem::Vector{Float64})
    if sum(_porcentagem)>=100.05
        (val,ind) = findmax(_porcentagem)
        _porcentagem[ind]=_porcentagem[ind]-0.1
    elseif sum(_porcentagem)<99.95
        (val,ind) = findmin(_porcentagem)
        _porcentagem[ind]=_porcentagem[ind]+0.1
    end
    _porcentagem = round.(_porcentagem,digits=2)
    return _porcentagem
end

function ponto_2_virgula(valor::Float64)
    return replace(string(valor),"."=>",")
end

function compor_sentenca(_pergunta::String,_opcoes::Vector{String},_porcentagem::Vector{Float64})
    s = string(_pergunta,"\n")
    for i=1:length(_opcoes)
        p = replace(string(_porcentagem[i]),"."=>",")
        s = string(s,"- $(p)% responderam $(_opcoes[i])\n")
    end
    return s 
end

function compor_grafico(_nome_do_curso,_codigo_subgrupo,_numero_pergunta,_pergunta::String,_opcoes::Vector{String},_porcentagem::Vector{Float64})
    aux = String.(replace(_nome_do_curso,r"\s+"=>""))
    s = "fig_$(aux)_$(_codigo_subgrupo)_$(_numero_pergunta).png"
    PyPlot.pie(_porcentagem,labels=_opcoes,autopct="%1.1f%%")
    #f = x->string(x,"%")
    #stringper = f.(string.(_porcentagem))
    #Plots.annotate!(plt,[-0.25, 0.25], [-0.25, 0.25], stringper)
    PyPlot.savefig("Imagens/$(s)")
    PyPlot.close()
    return s 
end

function compor_tabela(_pergunta::String,_opcoes::Vector{String},_porcentagem::Vector{Float64})
    s = "| Indicador | "
    for op in _opcoes
        s = string(s," $(op) | ")
    end
    s = string(s,"\n")
    s = string(s,"|---|")
    for op in _opcoes
        s = string(s,"---|")
    end
    s = string(s,"\n")
    s = string(s,"| $(_pergunta) |")
    for p in _porcentagem
        p2 = replace(string(p),"."=>",")
        s = string(s,"$(p2)% | ")
    end
    return s 
end





##################################################################################
#   Esta parte do arquivo refere-se aos elementos do compositor                  #
#   As funções aqui descritas irão gerar gráficos, dados e arquivos .md que      #
#   correspondem ao relatório de cada curso.                                     #
#                                                                                #
##################################################################################



function construir_dados_principais(avaliacao::DataFrame,cursos_e_centros::DataFrame,centro="CCE",ano=2020)
    df = sqldf("""
               SELECT 
               cc.nome_do_curso,
               ad.cd_subgrupo,
               ad.nm_subgrupo,
               ad.nu_pergunta,
               ad.pergunta,
               ad.ordem_opções,
               ad.opção,
               ad.porcentagem,
               ad.respostas,
               ad.total_do_curso
               FROM 
               avaliacao ad join cursos_e_centros cc 
               WHERE
               ad.codigo_curso=cc.Codigo_Curso
               AND
               cc.ano_referencia=$(ano)
               AND 
               cc.centro_de_ensino= "$(centro)"
               """)
    return df
end

function construir_tabela_cursos_por_centro(avaliacao::DataFrame,cursos_e_centros::DataFrame,centro::String,ano=2020)
    df = sqldf("""
               SELECT
               cc.nome_do_curso,
               cc.centro_de_ensino,
               ad.total_do_curso as Respondentes,
               cc.matriculados,
               (CAST(ad.total_do_curso AS FLOAT) / CAST(cc.matriculados AS FLOAT) * 100) as Porcentagem
               FROM
               avaliacao ad join cursos_e_centros cc
               WHERE	
               ad.codigo_curso=cc.codigo_curso 
               AND
               /* Define o período para obter os matriculados */
               cc.ano_referencia=2020
               AND
               /* Informa o centro de Ensino */
               cc.Centro_de_Ensino="$(centro)"
               GROUP BY 
               ad.codigo_curso
               ORDER BY
               cc.nome_do_curso
               """)
end

function construir_tabela_centro_por_ano(avaliacao::DataFrame,cursos_e_centros::DataFrame,centros_e_diretores::DataFrame,ano=2020)

    df = sqldf("""
               SELECT 
               geral.centro_de_ensino,
               cd.centro_descricao,
               sum(geral.Respondentes) Respondentes,
               sum(geral.Matriculados) Matriculados, 
               CAST(Respondentes AS FLOAT) / CAST(Matriculados AS FLOAT) * 100 as Porcentagem
               FROM	
               (SELECT
               cc.Centro_de_Ensino,
               ad.Nome_do_Curso,
               max(ad.total_do_curso) as Respondentes,
               cc.Matriculados

               FROM 
               avaliacao ad
               JOIN
               cursos_e_centros cc
               WHERE

               /* Aqui entra a definição do ano para puxar os matriculados */
               cc.ano_referencia = $(ano)
               AND	
               ad.codigo_curso = cc.codigo_curso
               GROUP BY 
               ad.nome_do_curso) geral 
               JOIN
               centros_e_diretores cd
               WHERE
               geral.centro_de_ensino = cd.centro_de_ensino
               GROUP BY 
               geral.centro_de_ensino
               ORDER BY
               geral.centro_de_ensino
               """)
    return df
end

"""
    preprocessar

Essa função tem por objetivo realizar o agrupamento dos objetos necessários. Dessa forma, essa deve ser a primeira função a ser executada.  

# Exemplo
```
julia-repl
julia> (T,c) = preprocessar("avaliacao_discente.csv","cursos_e_centros.csv","centros_e_diretores.csv","CCE",2020)
retornará em T um Dataframe e em c os cursos e um arquivo info_introducao.md será criado. 
```
"""
function preprocessar(_avaliacao::String,_cursos_e_centros::String,_centros_e_diretores::String,centro::String,ano::Int)
    global avaliacao = CSV.read(_avaliacao,DataFrame;normalizenames=true)
    global cursos_e_centros = CSV.read(_cursos_e_centros,DataFrame;normalizenames=true)
    global centros_e_diretores = CSV.read(_centros_e_diretores,DataFrame;normalizenames=true)
    dfprin = construir_dados_principais(avaliacao,cursos_e_centros,centro,ano)
    dfcen = construir_tabela_centro_por_ano(avaliacao,cursos_e_centros,centros_e_diretores,ano)
    dfcur = construir_tabela_cursos_por_centro(avaliacao,cursos_e_centros,centro,ano)
    compor_introducao(dfcen,dfcur,"introducao.md",ano)
    compor_conclusao(dfcen,dfcur,"conclusao.md",ano)
    T = agrupamento(dfprin)
    cursos = unique([T[i].nome_do_curso for i=1:length(T)])
    return T,cursos,dfcur
end


ReplGPT.initialize_conversation()

function compor_introducao(dfcentros::DataFrame,dfcursos::DataFrame,arquivo_intro::String="introducao.md",ano = 2020)
    template = Mustache.load(arquivo_intro)
    participacao_uem = round(100*(sum(dfcentros[:,3])/sum(dfcentros[:,4])),digits=1)
    df_2_tabela_centros = "| Sigla | Centro   | Resp. | Matr.   |  %   |\n |------|:----:|:-----:|:---:|:---:| \n"
    dfcentros[:,end] = round.(dfcentros[:,end],digits=1)
    for i=1:length(dfcentros[:,1])
        for j=1:length(dfcentros[1,:])
            if isa(dfcentros[i,j],Float64)    
                df_2_tabela_centros = df_2_tabela_centros * "| $(ponto_2_virgula(dfcentros[i,j])) "
            else
                df_2_tabela_centros = df_2_tabela_centros * "| $(dfcentros[i,j]) "
            end 
        end 
        df_2_tabela_centros = df_2_tabela_centros * " | \n"
    end 

    df_2_tabela_cursos = "| Curso |  Resp. |Matr.|   %   | \n |------|:-----:|:-----:|:---:| \n "
    dfcursos[:,end] = round.(dfcursos[:,end],digits=1)
    for i=1:length(dfcursos[:,1])
        for j=1:length(dfcursos[1,:])
            if j!=2 
                if isa(dfcursos[i,j],Float64)
                    df_2_tabela_cursos = df_2_tabela_cursos * "| $(ponto_2_virgula(dfcursos[i,j])) "
                else 
                    df_2_tabela_cursos = df_2_tabela_cursos * "| $(dfcursos[i,j]) "
                end
            end
        end 
        df_2_tabela_cursos = df_2_tabela_cursos * " | \n"
    end
    arquivo = open("info_introducao.md","w")
    intro = Mustache.render(template,Dict("tabela_centros"=>df_2_tabela_centros,"tabela_cursos_por_centro"=>df_2_tabela_cursos,"ano"=>ano,"curso"=>"{{curso}}","participacao_uem"=>ponto_2_virgula(participacao_uem),"participacao_curso"=>"{{participacao_curso}}"))
    write(arquivo,"$(intro) \n")
    close(arquivo)
end


function compor_conclusao(dfcentros::DataFrame,dfcursos::DataFrame,arquivo_concl::String="conclusao.md",ano = 2020)
    template = Mustache.load(arquivo_concl)
    participacao_uem = round(100*(sum(dfcentros[:,3])/sum(dfcentros[:,4])),digits=1)
     

    arquivo = open("info_conclusao.md","w")
    concl = Mustache.render(template,Dict("ano"=>ano,"curso"=>"{{curso}}","participacao_uem"=>ponto_2_virgula(participacao_uem),"participacao_curso"=>"{{participacao_curso}}"))
    write(arquivo,"$(concl) \n")
    close(arquivo)
end

"""
    compor_relatorio

Uma vez executada a função `preprocessar`, a função compor_relatorio deve ser utilizada. Ela é capaz de montar toda a estruturação do relatório à partir de partes que foram obtidas direta ou indiretamente. Em geral, essa função será chamada pela função compor_relatorio_por_grupo.
# Exemplos
```
julia-repl
julia> compor_relatorio(T,c,"CCE")

```
"""
function compor_relatorio(df::Vector{Info_de_Curso},curso::String,dc::DataFrame,centro::String,k=1)
    arquivo = open("$(curso).md","w")
    println(arquivo, "---")
    println(arquivo,"title: \"Relatório do Curso de $(curso)\"")
    println(arquivo,"titlepage: \"true\"")
    println(arquivo,"titlepage-background: \"capa\"")
    println(arquivo,"titlepage-rule-color: \"B3B3B3\"")
    println(arquivo,"page-background: \"interna02\"")
    println(arquivo,"page-background-opacity: \"1.0\"")
    println(arquivo,"author: [CPA-Comissão Própria de Avaliação]")
    println(arquivo,"lang: \"pt-BR\" ")
    println(arquivo,"...")
    println(arquivo,"")
    legenda_gpt = ""
    template = Mustache.load("info_introducao.md")
    participacao_curso = 0.0
    for i=1:length(dc[:,1])
        if curso == dc[i,1]
            participacao_curso = dc[i,end]
        end
    end
    intro = Mustache.render(template,Dict("curso"=>curso,"participacao_curso"=>ponto_2_virgula(participacao_curso)))
    write(arquivo,"$(intro) \n")
    flag = true
    println("🎈 Iniciando edição do curso $(curso) ... ")
    for i=1:length(df)

        if T[i].nome_do_curso == curso
            ReplGPT.initialize_conversation()
            legenda_gpt,flag = trychat("Transforme a pergunta $(T[i].pergunta) na forma de um título sucinto e que não seja indagação")
            if flag == false 
                close(arquivo)
                println("🚑 ChatGPT não se comunicou, arquivo fechado no $(curso) entrada $(i)!")
                return 
            end
            legenda_gpt = String(rstrip(replace(legenda_gpt,r"\""=>"")))
            #write(arquivo,"Gráfico $(k)- $(legenda_gpt) \n")
            write(arquivo,"![$(legenda_gpt)](Imagens/$(T[i].grafico)) \n")
            println(arquivo," ")
            println(arquivo,"Tabela $(k)- $(legenda_gpt) \n ")
            write(arquivo,T[i].tabela)
            write(arquivo,"\n")
            inicio_textual = rand(["Considerando a Tabela $(k), ","De acordo com a Tabela $(k), ","Pela Tabela $(k)", "Constatou-se pela Tabela $(k) que ", "Percebe-se pela Tabela $(k) que "])
            interpretacao_tabela_gpt,flag = trychat("Reescreva na forma de um parágrafo sucinto iniciando com a frase $(inicio_textual) o seguinte texto: \n $(T[i].texto) ")
            if flag == false 
                close(arquivo)
                println("🚑 ChatGPT não se comunicou, arquivo fechado no $(curso) entrada $(i)!")
                return 
            end
            println(arquivo," ")
            println(arquivo,interpretacao_tabela_gpt)
            k += 1
            println("👍 Edição da pergunta $(T[i].numero_pergunta) do subgrupo $(T[i].codigo_subgrupo) do curso $(curso) concluída com sucesso!")
        end
    end

    template = Mustache.load("info_conclusao.md")
    conclusao = Mustache.render(template,Dict("curso"=>curso,"participacao_curso"=>ponto_2_virgula(participacao_curso)))
    write(arquivo, "$(conclusao) \n")
    close(arquivo)
    println("🥳 Edição do curso $(curso) concluída com sucesso!")
    return 
end


"""
    trychat

Função auxiliar que permite tentar a comunicação com ChatGPT até n vezes, evitando assim possiveis falhas de comunicação. 
"""
function trychat(message::String,n=10)
    k = 1
    m = " "
    flag = false
    println()
    while k<n 
        try 
            m = "$(ReplGPT.call_chatgpt(message))"
            flag = true
            k = n 
            println("    🍻 Sucesso na execução do ChatGPT")
        catch
            println("    😠 Fracasso na execução do ChatGPT tentativa $(k)")
            k += 1
        end
    end

    return m,flag 
end



"""
    compor_relatorio_por_grupo

# Exemplo
```julia-repl
julia> (T,c) = preprocessar("avaliacao_discente.csv","cursos_e_centros.csv","centros_e_diretores.csv","CCE",2020)
julia> compor_relatorio_por_grupo(T,c,"CCE")
```
"""
function compor_relatorio_por_grupo(df::Vector{Info_de_Curso},cursos::Vector{String},dc::DataFrame,centro::String)
    for curso in cursos 
        compor_relatorio(df,curso,dc,centro,3)
    end
end




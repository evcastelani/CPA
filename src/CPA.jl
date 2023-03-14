module CPA
using Mustache, CSV

export Info_de_Curso, Template, interpola,ler_template


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
    nome :: String
    respondentes :: Int64
    matriculados :: Int64
    participacao :: Float64
    indicadores :: Vector{String}
    valores :: Vector{Union{Int64,Float64}}
    texto_chave :: String
    texto :: String
    grafico :: String
    tabela :: String 
    function Info_de_Curso(_nome,_respondentes,_matriculados,_indicadores,_valores,_texto_chave)
        _participacao = (_respondentes/_matriculados)*100
        _texto = "NONE"
        _tabela = "NONE"
        _grafico = "NONE"
        if occursin(r"{{.*?lista=true.*?}}",_texto_chave)
            _texto = "Preciso gerar a lista ordenada"
        end
        new(_nome,_respondentes,_matriculados,round(_participacao,digits=1),_indicadores,_valores,_texto_chave,_texto,_grafico,_tabela)
    end
end


"""
    Template

Este objeto define o layout, isto é, a estrutura de texto que será utilizada. Basicamente, temos que passar os atributos de algum objeto, por exemplo, `Info_de_Curso` para um texto. Esse texto, deve ser um objeto do tipo `Template`.

# Exemplo
```
julia-repl
julia> T = Template("Mustache.load(exemplo.txt"))
retorna um template que será usado posteriormente pela função interpola. Note que os atributos do objeto e do template devem estar conectados. 
```
"""
struct Template
    conteudo:: Mustache.MustacheTokens
end

"""
    ler_template

Essa função retorna o template na forma que ele pode ser lido. Basicamente, ela é uma forma mais sucinta de criar um template sem carregar, em comandos, um MustacheTokens.

# Exemplo
```
julia-repl
julia> T = ler_template("exemplo.txt")
returna T como Template. Templates são usados na função `interpola`.
```
"""
function ler_template(filename::String)
    return Template(Mustache.load(filename))
end

function lista()

end
"""
    interpola


O papel dessa função é interpolar um `Template` e um objeto `Info_de_Curso` e retornar uma `String` que poderá, de fato, confeccionar um texto em `LaTeX` ou `Markdown`.

# Exemplo
```
julia-repl
julia> T = ler_template("exemplo.txt")
julia> C = Info_de_Curso("Matemática",10,20)
julia> s = interpola(T,C)
julia> print(s)
```
"""
function interpola(T::Template,C::Info_de_Curso)
    return render(T.conteudo,C)
end
    


end # module

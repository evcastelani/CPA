module CPA
using Mustache, CSV

export Info_de_Curso, Template

struct Info_de_Curso
    nome :: String
    respondentes :: Int64
    matriculados :: Int64
end

struct Template
    conteudo:: MustacheTokens
end

function ler_template(filename::String)
    return Template(Mustache.load(filename))
end

function interpola(T::Template,C::Info_de_Curso)
    return render(T.conteudo,C)
end
    


end # module

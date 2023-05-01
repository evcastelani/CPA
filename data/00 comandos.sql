# Em revisão. 
---

## Comando para obter a lista de Respondentes por Curso
SELECT nome_do_curso, MAX(total_do_curso) AS Respondentes FROM avaliacao_discente_ere_2020 GROUP BY nome_do_curso;

# Obter a lista de centro, cursos e matriculados de 2020
SELECT * FROM centros_e_cursos WHERE ano_referencia=2020 ORDER by centro_de_ensino, nome_do_curso;

# Concatenar as duas buscas
# Não Funciona
SELECT *, 
    (SELECT nome_do_curso, MAX(total_do_curso) AS Respondentes 
        FROM avaliacao_discente_ere_2020 GROUP BY nome_do_curso) 
FROM centros_e_cursos 
WHERE ano_referencia=2020 
ORDER by centro_de_ensino, nome_do_curso;

# Não funciona
SELECT 
    av.nome_do_curso, 
    MAX(av.total_do_curso) AS Respondentes 
FROM avaliacao_discente_ere_2020 av 
GROUP BY av.nome_do_curso 

# Não funciona

UNION 
    SELECT 
        cc.nome_do_curso, 
        cc.matriculados 
    FROM centros_e_cursos cc 
    WHERE cc.ano_referencia=2020 AND av.nome_do_curso == cc.nome_do_curso;

# Não funciona

SELECT
    centros_e_curso.centro_de_ensino,
    av.nome_do_curso,
    MAX(av.total_do_curso) AS Respondentes,
    centros_e_curso.matriculados
FROM avaliacao_discente_ere_2020 av
GROUP BY av.nome_do_curso
INNER JOIN centros_e_cursos ON av.nome_do_curso=centros_e_curso.nome_do_curso;
# Em revisão. 
---

## Comando para obter a lista de Respondentes por Curso
SELECT nome_do_curso, MAX(total_do_curso) AS Respondentes FROM avaliacao_discente_ere_2020 GROUP BY nome_do_curso;

# Obter a lista de centro, cursos e matriculados de 2020
SELECT * FROM centros_e_cursos WHERE ano_referencia=2020 ORDER by centro_de_ensino, nome_do_curso;

# Concatenar as duas buscas
# Não Funciona
SELECT *,
	(SELECT cc.nome_do_curso
     FROM cursos_e_centros cc 
     where cc.codigo_curso=ad.codigo_curso) as Curso_Descricao
    
FROM avaliacao_discente_ere_2020 ad;
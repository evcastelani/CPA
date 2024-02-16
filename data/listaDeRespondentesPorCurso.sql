SELECT 
    nome_do_curso, 
    MIN(total_do_curso) AS Respondentes 
FROM 
    avaliacao_discente_ere_2020 
GROUP BY 
    nome_do_curso;
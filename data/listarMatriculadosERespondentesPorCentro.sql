SELECT 
	centros.centro_de_ensino,
    cd.centro_descricao,
    sum(centros.Respondentes) Respondentes,
    sum(centros.Matriculados) Matriculados, 
    CAST(sum(centros.Respondentes) AS FLOAT) / CAST(sum(centros.Matriculados) AS FLOAT) * 100 as Porcentagem
FROM	
    (SELECT
        cc.Centro_de_Ensino as Centro_de_Ensino,
        ad.Nome_do_Curso as Nome_do_Curso,
        min(ad.total_do_curso) as Respondentes,
        cc.Matriculados as Matriculados
    FROM 
        avaliacao_discente_ere_2020 ad
        JOIN
        cursos_e_centros cc
    WHERE

        /* Aqui entra a definição do ano para puxar os matriculados */
        cc.ano_referencia = "2020"
        AND	
        ad.codigo_curso = cc.codigo_curso
    GROUP BY 
        ad.nome_do_curso) centros 
        JOIN
        centros_e_diretores cd
WHERE
	centros.centro_de_ensino = cd.centro_de_ensino
GROUP BY 
	centros.centro_de_ensino
ORDER BY
	centros.centro_de_ensino
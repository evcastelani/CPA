SELECT
    cc.nome_do_curso,
    cc.centro_de_ensino,
    ad.total_do_curso as Respondentes,
    cc.matriculados,
    CAST(ad.total_do_curso AS FLOAT) / CAST(cc.matriculados AS FLOAT) * 100 as Porcentagem
FROM
    /* Junta as duas tabelas */
	avaliacao_discente_ere_2020 ad join cursos_e_centros cc
WHERE	
	ad.codigo_curso=cc.codigo_curso 
    AND
    /* Define o período para obter os matriculados */
    cc.ano_referencia=2020
    AND
    /* Informa o centro de Ensino */
    cc.Centro_de_Ensino="CCE"
GROUP BY 
	ad.codigo_curso
ORDER BY
	cc.nome_do_curso
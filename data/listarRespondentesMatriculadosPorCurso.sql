SELECT 
	cc.nome_do_curso, 
    cc.centro_de_ensino, 
    min(ad.total_do_curso) as total_respondentes, 
    cc.matriculados as total_matriculados,
    CAST(Min(ad.total_do_curso) AS FLOAT) / CAST(cc.matriculados AS FLOAT) * 100 as Porcentagem
FROM 
	avaliacao_discente_ere_2020 ad, 
    cursos_e_centros cc 
WHERE
	ad.codigo_curso = cc.codigo_curso 
  and
  	cc.ano_referencia = "2020"
group by 
	ad.nome_do_curso
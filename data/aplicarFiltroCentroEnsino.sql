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
	avaliacao_discente_ere_2020 ad 
    JOIN
    cursos_e_centros cc 
WHERE
	ad.codigo_curso=cc.Codigo_Curso
    AND
    cc.ano_referencia=2020
    AND 
    cc.centro_de_ensino="CCE";
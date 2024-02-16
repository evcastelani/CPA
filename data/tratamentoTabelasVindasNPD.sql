SELECT 
    cc.codigo_curso,
    cc.NOME_do_CURSO,
	cc.Centro_de_Ensino,
    ad.codigo_subgrupo as cd_subgrupo,
	ad.NOME_SUBGRUPO as nm_subgrupo,
	ad.CODIGO_PERGUNTA as nu_pergunta,
	ad.pergunta as pergunta,
	ad.ORDEM_OPCOES,
	ad.OPCAO,
	((SUM(ad.RESPOSTAS) * 100.0) / (SUM(ad.TOTAL_DO_CURSO) * 1.0))  as Porcentagem,
	SUM(ad.RESPOSTAS) as Respostas,
	SUM(ad.TOTAL_DO_CURSO) as Total_do_Curso
FROM 
	"2021 Discentes" ad 
    JOIN
    centros_cursos cc 
WHERE
	ad.codico_curso=cc.Codigo_Curso
    AND
    cc.ano_referencia=2021
    
GROUP BY
    ad.codico_curso,
    ad.CODIGO_PERGUNTA,
    ad.Opcao
ORDER BY 
    cc.NOME_DO_CURSO,
    ad.nome_subgrupo,
    ad.CODIGO_PERGUNTA,
    ad.ORDEM_OPCOES
;
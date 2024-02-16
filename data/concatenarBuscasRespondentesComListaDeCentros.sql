SELECT ad.codigo_curso, 
		cc.centro_de_ensino,
        /* Aqui faço uma combinação meio maluca para
        listar os nomes dos cursos e os nomes dos centros de forma declarada. 
        É só um exercício que usei para tentar combinar as tabelas.
        */
        (SELECT cd.centro_descricao from centros_e_diretores cd WHERE cd.centro_de_ensino=cc.centro_de_ensino) as Centro_Descricao,
        cc.nome_do_curso, 

        cc.matriculados,
        ad.cd_subgrupo,
        ad.nm_subgrupo,
        ad.nu_pergunta,
        ad.pergunta,
        ad.ordem_opções,
        ad.opção,
        ad.porcentagem,
        ad.respostas,
        ad.total_do_curso
        
/* Aqui faço a combinação de duas tabelas como se fosse uma única tabela.
    Tabela AD - Avaliação Discente
    Tabela CC - Cursos e Centros
*/

FROM 
    avaliacao_discente_ere_2020 ad JOIN
    cursos_e_centros cc 

/* Listagem dos matriculados de 2021 */
where 
	cc.codigo_curso=ad.codigo_curso AND 
    cc.ano_referencia = 2021;
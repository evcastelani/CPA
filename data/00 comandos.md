# Alguns comandos para usar na seleção de dados
----
Faço um exercício com alguns comandos de SQL para facilitar o trabalho com os Datasets.

Para trabalhar melhor os dados, preferi manter a tabela original de dados vindo do NPD. Somente será necessário acrescentar o código do curso na primeira coluna, conforme indica a imagem abaixo.

![](img/2023-05-01_13-26.png)


Se quiser fazer testes de SQL, podemos usar o site:
https://sqliteonline.com/

Assim não é necessário instalar um servidor de banco de dados ou um app para trabalhar com SQLite. 


# Índice dos comandos
  
* [Obter a lista de Respondentes por Curso](#obter-a-lista-de-respondentes-por-curso)
* [Obter a lista de centro, cursos e matriculados de 2021](#obter-a-lista-de-centro--cursos-e-matriculados-de-2021)
- [Exercício para Concatenar as duas buscas](#exerc-cio-para-concatenar-as-duas-buscas)
  * [Filtro aplicado ao CCE](#filtro-aplicado-ao-cce)
  * [Tabela de Cursos por Centro de Ensino e Ano de Referência](#tabela-de-cursos-por-centro-de-ensino-e-ano-de-refer-ncia)
  * [Listagem de Matriculados e Respondentes por Centro em um ano específico](#listagem-de-matriculados-e-respondentes-por-centro-em-um-ano-espec-fico)







## Obter a lista de Respondentes por Curso
Um comando rápido para calcular o total de respondentes. 

```
SELECT nome_do_curso, MAX(total_do_curso) AS Respondentes FROM avaliacao_discente_ere_2020 GROUP BY nome_do_curso;
```

## Obter a lista de centro, cursos e matriculados de 2021

Esse comando permite com que sejam listados todos os alunos matriculados de um determinado ano.

```
SELECT * 
FROM 
    cursos_e_centros 
WHERE 
    ano_referencia=2021 
ORDER BY 
    centro_de_ensino, nome_do_curso;
```

# Exercício para Concatenar as duas buscas
Nessa parte eu tento combinar as duas buscas para facilitar o trabalho de consulta às tabelas. 

```
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

```

## Filtro aplicado ao CCE

Formatação do filtro por Centro e Por período de 2020.

```
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
    

```

## Tabela de Cursos por Centro de Ensino e Ano de Referência
Nessa tabela, listamos as seguintes variáveis. 
- Código do curso
- Nome do Curso
- Centro de Ensino
- Nome do Curso (Reescrito)
- Total de respondentes
- Número de matriculados
- Porcentagem entre os respondentes e matriculados


```
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


```

## Listagem de Matriculados e Respondentes por Centro em um ano específico

Esse aqui foi um pouco mais complicado, pois ele trabalha com uma tabela combinada, dentro de outra combinada. 

Com certeza existe uma forma mais elegante para resolver. 

Mas ele retorna as seguintes variáveis:
- Centro de Ensino
- Número de Respondentes
- Número de Matriculados

Lembrando que ele faz um filtro para um determinado ano.

```
SELECT 
	centro_de_ensino,
    sum(Respondentes) Respondentes,
    sum(Matriculados) Matriculados
FROM	
  (SELECT
      cc.Centro_de_Ensino,
      ad.Nome_do_Curso,
      max(ad.total_do_curso) as Respondentes,
      cc.Matriculados

  FROM 
      avaliacao_discente_ere_2020 ad
      JOIN
      cursos_e_centros cc
  WHERE
      cc.ano_referencia = 2020
      AND	
      ad.codigo_curso = cc.codigo_curso
  GROUP BY 
      ad.nome_do_curso)
GROUP BY 
	centro_de_ensino
ORDER BY
	centro_de_ensino

```

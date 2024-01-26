# Busca inicial e formatação

Formatação de saída solicitada pelo Prof. Emerson.

```
SELECT 
dis.CODICO_CURSO as Codigo_Curso,
dis.Nome_Curso as Nome_do_Curso,
dis.CODIGO_SUBGRupo as CD_Subgrupo,
dis.Nome_Subgrupo as NM_Subgrupo,
dis.codigo_Pergunta as NU_Pergunta,
dis.Pergunta,
dis.ordem_opcoes as Ordem_Opções,
dis.opcao as Opção,
dis.Porcentagem,
dis.Respostas,
Total_do_Curso

FROM

"2021 Discentes" dis;
```

Seleção somente dos códigos do curso e nomes a partir das tabelas de Centro e Discentes. 

```
select distinct codigo_curso, nome_do_Curso from cursos_e_centros;
select distinct codico_curso, nome_Curso from "2021 Discentes";
```

Seleção de Códigos por Centro de Ensino

```
SELECT distinct Codigo_Curso FROM centros_cursos WHERE Centro_de_Ensino="CSA";
```

Resultado:

```
1	CIÊNCIAS ECONÔMICAS
2	DIREITO
3	LETRAS
4	GEOGRAFIA
5	HISTORIA
6	QUIMICA
7	MATEMATICA
8	ADMINISTRACAO
9	ENGENHARIA CIVIL
10	ENGENHARIA QUIMICA
11	EDUCACAO FISICA
12	CIENCIAS CONTABEIS
13	PEDAGOGIA
14	CIENCIAS BIOLOGICAS
15	FISICA
16	FARMACIA
17	ZOOTECNIA
19	AGRONOMIA
21	PSICOLOGIA
22	PEDAGOGIA(CRC)
23	CIENCIAS CONTABEIS (CRC)
24	MEDICINA
25	ODONTOLOGIA
26	CIENCIA DA COMPUTACAO
27	ENGENHARIA TEXTIL
28	LICENCIATURA PLENA EM CIENCIAS
30	ENFERMAGEM
31	INFORMATICA
33	CIENCIAS SOCIAIS
34	FILOSOFIA
35	ENGENHARIA MECANICA
36	ENGENHARIA DE ALIMENTOS
37	ENGENHARIA DE PRODUCAO
38	ARQUITETURA E URBANISMO
39	ESTATISTICA
40	SECRETARIADO EXECUT. TRILINGUE
42	MUSICA
43	DESIGN
44	MODA
45	ENGENHARIA AGRICOLA(CAR)
46	AGRONOMIA (CAU)
47	MEDICINA VETERINARIA-CAU
48	TEC. EM CONSTRUCAO CIVIL-CAU
50	TECNOL. EM MEIO AMBIENTE-CAU
62	BIOMEDICINA
63	HISTORIA - CRV
64	EDUCACAO FISICA (CRV)
65	SERVICO SOCIAL (CRV)
66	COMUNICACAO E MULTIMEIOS
67	FISICA (CRG)
68	BIOQUIMICA
70	ENGENHARIA AMBIENTAL-CAU
71	ENGENHARIA DE ALIMENTOS-CAU
72	ARTES CENICAS
73	ARTES VISUAIS
74	ENGENHARIA CIVIL-CAU
75	ENGENHARIA ELETRICA
76	ENGENHARIA DE PRODUCAO (CRG)
79	PEDAGOGIA - PARFOR
93	BIOTECNOLOGIA
49	TECNOLOGIA EM ALIMENTOS (CAU)
69	TECNOLOGIA EM BIOTECNOLOGIA
92	LIC. EM CIENCIAS NATURAIS-CRG
```

# Seleção por Centro

Aqui tentamos explorar os resultados por Centro de Ensino.

```
SELECT 
dis.CODICO_CURSO as Codigo_Curso,
dis.Nome_Curso as Nome_do_Curso,
dis.CODIGO_SUBGRupo as CD_Subgrupo,
dis.Nome_Subgrupo as NM_Subgrupo,
dis.codigo_Pergunta as NU_Pergunta,
dis.Pergunta,
dis.ordem_opcoes as Ordem_Opções,
dis.opcao as Opção,
dis.Porcentagem,
dis.Respostas,
Total_do_Curso

FROM

"2021 Discentes" dis 

WHERE 
Codigo_Curso IN (SELECT distinct Codigo_Curso FROM centros_cursos WHERE Centro_de_Ensino="CSA")
;





```

# Ainda sem muita definição. 
Estou tentando montar algo que inclua o Centro na lista. O problema é que o resultado está saindo repetido.



```
SELECT 
dis.CODICO_CURSO as Codigo_Curso,
cec.Nome_Do_Curso as Nome_do_Curso,
cec.Centro_de_Ensino as Centro_de_Ensino,
dis.CODIGO_SUBGRupo as CD_Subgrupo,
dis.Nome_Subgrupo as NM_Subgrupo,
dis.codigo_Pergunta as NU_Pergunta,
dis.Pergunta,
dis.ordem_opcoes as Ordem_Opções,
dis.opcao as Opção,
dis.Porcentagem,
dis.Respostas,
Total_do_Curso

FROM

"2021 Discentes" dis, centros_cursos cec



WHERE 
dis.CODICO_CURSO = cec.Codigo_Curso and cec.Ano_Referencia = 2021

ORDER BY Codigo_Curso, nu_Pergunta, ORDEM_OPCOES
;
```

```
SELECT 
dis.CODICO_CURSO as Codigo_Curso,
cec.Nome_Do_Curso as Nome_do_Curso,
cec.Centro_de_Ensino as Centro_de_Ensino,
dis.CODIGO_SUBGRupo as CD_Subgrupo,
dis.Nome_Subgrupo as NM_Subgrupo,
dis.codigo_Pergunta as NU_Pergunta,
dis.Pergunta,
dis.ordem_opcoes as Ordem_Opções,
dis.opcao as Opção,
dis.Porcentagem,
dis.Respostas,
Total_do_Curso
FROM
"2021 Discentes" dis, centros_cursos cec
WHERE 
dis.CODICO_CURSO = cec.Codigo_Curso and cec.Ano_Referencia = 2021
ORDER BY Codigo_Curso, nu_Pergunta, ORDEM_OPCOES
;
```


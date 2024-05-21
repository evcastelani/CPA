def df_centro_por_curso(database):
    cursos_e_centros = database['centro_e_curso']
    curso = database['curso']

    # Realizar a agregação de dados
    results = cursos_e_centros.aggregate([
        {
            "$lookup": {
                "from": "curso",
                "localField": "codigo_curso",
                "foreignField": "codigo_curso",
                "as": "curso"
            }
        },
        {
            "$unwind": "$curso"
        },
        {
            "$match": {
                "ano_referencia": 2020,
                "centro_de_ensino": "CSA",
                "curso.codigo_curso": {"$exists": True}
            }
        },
        {
            "$group": {
                "_id": "$codigo_curso",
                "nome_do_curso": {"$first": "$nome_do_curso"},
                "centro_de_ensino": {"$first": "$centro_de_ensino"},
                "matriculados": {"$first": "$matriculados"},
                "total_do_curso": {"$first": "$curso.total_do_curso"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "nome_do_curso": 1,
                "centro_de_ensino": 1,
                "respondentes": "$total_do_curso",
                "matriculados": 1,
                "porcentagem": {
                    "$round": [
                        {
                            "$multiply": [
                                {"$divide": ["$total_do_curso", "$matriculados"]},
                                100
                            ]
                        },
                        2
                    ]
                }
            }
        },
        {
            "$sort": {"nome_do_curso": 1}
        },
        {
            "$out": "centro_por_curso"
        }
    ])

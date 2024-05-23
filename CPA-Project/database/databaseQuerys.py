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


def df_centro_por_ano(database, ano):
    curso = database['curso']
    cursos_e_centros = database['cursos_e_centros']
    centros_e_diretores = database['centros_e_diretores']

#     curso.aggregate([
#     {
#         "$lookup": {
#             "from": "cursos_e_centros",
#             "localField": "codigo_curso",
#             "foreignField": "codigo_curso",
#             "as": "cursos_e_centros"
#         }
#     },
#     {
#         "$unwind": "$cursos_e_centros"
#     },
#     {
#         "$match": {
#             "cursos_e_centros.ano_referencia": 2021 
#         }
#     },
#     {
#         "$group": {
#             "_id": "$nome_do_curso",
#             "centro_de_ensino": {"$first": "$cursos_e_centros.centro_de_ensino"},
#             "respondentes": {"$max": "$total_do_curso"},
#             "matriculados": {'$first': "$cursos_e_centros.matriculados"}
#         }
#     },
#     {
#         "$lookup": {
#             "from": "centros_e_diretores",
#             "localField": "centro_de_ensino",
#             "foreignField": "centro_de_ensino",
#             "as": "centros_e_diretores"
#         }
#     },
#     {
#         "$unwind": "$centros_e_diretores"
#     },
#     {
#         "$group": {
#             "_id": "$centro_de_ensino",
#             "centro_descricao": {"$first": "$centros_e_diretores.centro_descricao"},
#             "respondentes": {"$sum": "$respondentes"},
#             "matriculados": {"$sum": "$matriculados"},
#             "porcentagem": {
#                 "$avg": {
#                     "$multiply": [
#                         {"$divide": [{"$sum": "$respondentes"}, {"$sum": "$matriculados"}]},
#                         100
#                     ]
#                 }
#             }
#         }
#     },
#     {
#         '$project': {
#             '_id': 0,
#             'centro_de_ensino':'$_id',
#             'centro_descricao':1,
#             'respondentes': 1,
#             'matriculados':1,
#             'porcentagem': {'$round': ['$porcentagem', 2]}
#         }

#     },
#     {
#         "$sort": {"_id": 1}
#     },
#     {
#         '$out': 'centro_por_ano'
#     }
# ])

    curso.aggregate([
        {   
            "$lookup": {
            "from": "cursos_e_centros",
            "localField": "codigo_curso",
            "foreignField": "codigo_curso",
            "as": "cursos_e_centros"
            }
        },
        {
            "$unwind": "$cursos_e_centros"
        },
        {
            "$match": {
                "cursos_e_centros.ano_referencia": 2021 
            }
        },
        {
            "$group": {
                "_id": "$nome_do_curso",
                "centro_de_ensino": {"$first": "$cursos_e_centros.centro_de_ensino"},
                "respondentes": {"$max": "$total_do_curso"},
                "matriculados": {'$first': "$cursos_e_centros.matriculados"},
                "porcentagem": {
                    "$avg": {
                        "$multiply": [
                            {"$divide": [{"$sum": "$total_do_curso"}, {"$sum": "$cursos_e_centros.matriculados"}]},
                            100
                        ]
                    }
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'centro_de_ensino':1,
                'respondentes': {'$sum':'$respondentes'},
                'matriculados': {'$sum': '$matriculados'},
                'porcentagem': {'$round': ['$porcentagem',2]}
            }
        },
        {
            '$out':'centro_por_ano'
        }
    ])
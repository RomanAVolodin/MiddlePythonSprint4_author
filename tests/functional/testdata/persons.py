from http import HTTPStatus

find_persons_edge_cases = [
    (
        {'person_id': '7ddf1e3b-20b9-4898-97ac-559442a07467'},
        {
            'status': HTTPStatus.OK,
            'fields': {'uuid', 'full_name', 'films'},
            'film_fields': {'id', 'title', 'imdb_rating'},
        },
    ),
    ({'person_id': 'string'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'person_id': 100}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'person_id': ' '}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
]

find_persons_valid_data = [
    (
        {'person_id': '02e304e3-1984-4d52-9f4a-b9c5713f54b3'},
        {
            'status': HTTPStatus.OK,
            'fields': {'uuid', 'full_name', 'films'},
            'film_fields': {'id', 'title', 'imdb_rating'},
        },
    ),
    (
        {'person_id': '30500cd3-4d07-4ced-939b-f4d139f97bf5'},
        {
            'status': HTTPStatus.OK,
            'fields': {'uuid', 'full_name', 'films'},
            'film_fields': {'id', 'title', 'imdb_rating'},
        },
    ),
]

find_persons_invalid_data = [
    ({'person_id': 'fb0afa02-c3d9-40f6-afeb-312f71cfd9f2'}, {'status': HTTPStatus.NOT_FOUND}),
    ({'person_id': 'fdb8dbfb-e6c7-43a4-bb31-1f85627236eb'}, {'status': HTTPStatus.NOT_FOUND}),
]

find_persons_films = [
    (
        {'person_id': '7293cc37-a32a-4370-8f9a-b9189a6f43a1', 'films_amount': 10},
        {'status': HTTPStatus.OK, 'films_amount': 10, 'film_fields': {'id', 'title', 'imdb_rating'}},
    ),
    (
        {'person_id': '71c62f7b-af3e-41da-8441-000539af3afa', 'films_amount': 2},
        {'status': HTTPStatus.OK, 'films_amount': 2, 'film_fields': {'id', 'title', 'imdb_rating'}},
    ),
    (
        {'person_id': '4272b555-3a0d-4402-9244-24ea9d00c3b6', 'films_amount': 60},
        {'status': HTTPStatus.OK, 'films_amount': 10, 'film_fields': {'id', 'title', 'imdb_rating'}},
    ),
]

person_redis_data = [
    (
        {'person_id': 'bfc673dc-ec37-4876-8825-29440e2e22c1'},
        {'status': HTTPStatus.OK, 'fields': {'uuid', 'full_name', 'films'}},
    ),
]

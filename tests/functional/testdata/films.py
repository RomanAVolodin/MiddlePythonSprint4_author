from http import HTTPStatus

film_edge_cases_data = [
    (
        {
            'films_amount': 60,
            'page_size': 50,
            'page_number': 1,
        },
        {'status': HTTPStatus.OK, 'length': 50, 'fields': {'id', 'title', 'imdb_rating'}},
    ),
    (
        {
            'films_amount': 60,
            'page_size': 50,
            'page_number': 2,
        },
        {'status': HTTPStatus.OK, 'length': 10, 'fields': {'id', 'title', 'imdb_rating'}},
    ),
    (
        {
            'films_amount': 60,
            'page_size': 50,
            'page_number': 3,
        },
        {'status': HTTPStatus.NOT_FOUND, 'length': 1},
    ),
    (
        {
            'films_amount': 1,
            'page_size': -1,
            'page_number': 3,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
    (
        {
            'films_amount': 1,
            'page_size': 0,
            'page_number': 3,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
    (
        {
            'films_amount': 1,
            'page_size': 1,
            'page_number': -1,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
    (
        {
            'films_amount': 1,
            'page_size': 1,
            'page_number': 0,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
]

validation_genre_data = [
    ({'genre': '02e304e3-1984-4d52-9f4a-b9c5713f54b3'}, {'status': HTTPStatus.NOT_FOUND}),
    ({'genre': 'string'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'genre': 100}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
]

validation_query_data = [
    ({'query': '02e304e3-1984-4d52-9f4a-b9c5713f54b3'}, {'status': HTTPStatus.NOT_FOUND}),
    ({'query': 'string'}, {'status': HTTPStatus.NOT_FOUND}),
    ({'query': 100}, {'status': HTTPStatus.NOT_FOUND}),
]

validation_sort_data = [
    ({'sort': 'imdb_rating'}, {'status': HTTPStatus.OK, 'fields': {'id', 'title', 'imdb_rating'}}),
    ({'sort': '-imdb_rating'}, {'status': HTTPStatus.OK, 'fields': {'id', 'title', 'imdb_rating'}}),
    ({'sort': 'some_sorting'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
]

validation_pages_data = [
    ({'page_size': 10, 'page_number': 1}, {'status': HTTPStatus.OK, 'fields': {'id', 'title', 'imdb_rating'}}),
    ({'page_size': 10, 'page_number': '1'}, {'status': HTTPStatus.OK, 'fields': {'id', 'title', 'imdb_rating'}}),
    ({'page_size': 10, 'page_number': 'number'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'page_size': '10', 'page_number': 1}, {'status': HTTPStatus.OK, 'fields': {'id', 'title', 'imdb_rating'}}),
    ({'page_size': 'number', 'page_number': 1}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'page_size': '10', 'page_number': '1'}, {'status': HTTPStatus.OK, 'fields': {'id', 'title', 'imdb_rating'}}),
    ({'page_size': 'number', 'page_number': 'number'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
]

get_film_data = [
    (
        {'film_uuid': 'b62c9858-8230-463a-a8b0-30074d1b5171'},
        {
            'status': HTTPStatus.OK,
            'fields': {
                'id',
                'title',
                'description',
                'file',
                'imdb_rating',
                'genres',
                'actors',
                'directors',
                'writers',
                'actors_names',
                'directors_names',
                'writers_names',
                'last_change_date',
            },
        },
    ),
]

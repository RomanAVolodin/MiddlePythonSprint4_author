from http import HTTPStatus

person_edge_cases_data = [
    (
        {
            'persons_amount': 60,
            'page_size': 50,
            'page_number': 1,
        },
        {'status': HTTPStatus.OK, 'length': 50, 'fields': {'uuid', 'full_name', 'films'}},
    ),
    (
        {
            'persons_amount': 60,
            'page_size': 50,
            'page_number': 2,
        },
        {'status': HTTPStatus.OK, 'length': 10, 'fields': {'uuid', 'full_name', 'films'}},
    ),
    (
        {
            'persons_amount': 60,
            'page_size': 50,
            'page_number': 3,
        },
        {'status': HTTPStatus.NOT_FOUND, 'length': 1},
    ),
    (
        {
            'persons_amount': 1,
            'page_size': -1,
            'page_number': 3,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
    (
        {
            'persons_amount': 1,
            'page_size': 0,
            'page_number': 3,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
    (
        {
            'persons_amount': 1,
            'page_size': 1,
            'page_number': -1,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
    (
        {
            'persons_amount': 1,
            'page_size': 1,
            'page_number': 0,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1},
    ),
]


validation_query_data = [
    ({'query': '02e304e3-1984-4d52-9f4a-b9c5713f54b3'}, {'status': HTTPStatus.NOT_FOUND}),
    ({'query': 'string'}, {'status': HTTPStatus.NOT_FOUND}),
    ({'query': 100}, {'status': HTTPStatus.NOT_FOUND}),
]


validation_pages_data = [
    ({'page_size': 10, 'page_number': 1}, {'status': HTTPStatus.OK, 'fields': {'uuid', 'full_name', 'films'}}),
    ({'page_size': 10, 'page_number': '1'}, {'status': HTTPStatus.OK, 'fields': {'uuid', 'full_name', 'films'}}),
    ({'page_size': 10, 'page_number': 'number'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'page_size': '10', 'page_number': 1}, {'status': HTTPStatus.OK, 'fields': {'uuid', 'full_name', 'films'}}),
    ({'page_size': 'number', 'page_number': 1}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'page_size': '10', 'page_number': '1'}, {'status': HTTPStatus.OK, 'fields': {'uuid', 'full_name', 'films'}}),
    ({'page_size': 'number', 'page_number': 'number'}, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
]

get_person_data = [
    (
        {
            'person_uuid': 'b62c9858-8230-463a-a8b0-30074d1b5171',
            'persons_amount': 1,
            'page_size': 50,
            'page_number': 1,
            'query': '',
        },
        {'status': HTTPStatus.OK, 'fields': {'uuid', 'full_name', 'films'}},
    ),
]

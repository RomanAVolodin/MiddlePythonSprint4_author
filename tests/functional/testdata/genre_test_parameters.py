from http import HTTPStatus

genre_get_genres_data = [
    (
        {
            'genres_amount': 60,
        },
        {'status': HTTPStatus.OK, 'length': 60, 'fields': {'id', 'name'}},
    ),
    (
        {
            'genres_amount': 30,
        },
        {'status': HTTPStatus.OK, 'length': 30, 'fields': {'id', 'name'}},
    ),
]


genre_id_data = [
    (
        {
            'genreuuid': '23f58e26-1168-40b6-b4a6-ad2126d580f0',
            'genres_amount': 1,
        },
        {'status': HTTPStatus.OK, 'length': 2, 'fields': {'id', 'name'}},
    ),
    (
        {
            'genreuuid': '4d714dd1-d48e-45bc-a782-accfdd0d2753',
            'genres_amount': 1,
        },
        {'status': HTTPStatus.OK, 'length': 2, 'fields': {'id', 'name'}},
    ),
]

genre_not_found_id_data = [
    (
        {
            'genreuuid': '417da93a-bd80-45ba-bae5-38c5c5eabc40',
            'genres_amount': 1,
        },
        {'status': HTTPStatus.NOT_FOUND, 'message': {'detail': 'genre not found'}},
    ),
    (
        {
            'genreuuid': 'e969d9e9-1870-45cc-9e71-5f15a874b5b5',
            'genres_amount': 1,
        },
        {'status': HTTPStatus.NOT_FOUND, 'message': {'detail': 'genre not found'}},
    ),
]


genre_incorrect_id_data = [
    (
        {
            'genreuuid': 'df417da93a-bd80-45ba-bae5-38c5c5eabc40',
            'genres_amount': 1,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'message_part': 'Input should be a valid UUID'},
    ),
    (
        {
            'genreuuid': 'e969d-9e918-7045-cc9-e715f15a-874b5b5',
            'genres_amount': 1,
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'message_part': 'Input should be a valid UUID'},
    ),
]

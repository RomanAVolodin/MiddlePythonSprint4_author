from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from services.film import FilmService, get_film_service
from services.paginated_params import PaginatedParams
from .schemas import Film, FilmSummary

router = APIRouter()


@router.get(
    '/search',
    response_model=list[FilmSummary],
    dependencies=[Depends(PaginatedParams)],
)
@router.get(
    '',
    response_model=list[FilmSummary],
    dependencies=[Depends(PaginatedParams)],
)
async def get_films(
    film_service: FilmService = Depends(get_film_service),
    genre: UUID | None = Query(None, description='Filter films by genre UUID'),
    query: str | None = Query(None, description='Filter films by title'),
    sort: str
    | None = Query(
        None,
        description='Sort order for films, options: imdb_rating, ' 'use prefix ` - ` for descending order',
        pattern=r'^(-imdb_rating|imdb_rating|None)$',
    ),
    page_size: int = Query(
        PaginatedParams.default_page_size,
        description='Number of films per page',
        ge=PaginatedParams.page_size_ge,
    ),
    page_number: int = Query(
        PaginatedParams.default_page_number,
        description='Page number',
        ge=PaginatedParams.page_number_ge,
    ),
):
    """Получение списка фильмов"""

    films = await film_service.get_films(page_size, page_number, sort, genre, query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    return films


@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    """Получение фильма по его id"""

    film = await film_service.get_by_id(str(film_id))
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film

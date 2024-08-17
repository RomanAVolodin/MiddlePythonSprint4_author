from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from services.paginated_params import PaginatedParams
from services.persons import PersonService, get_persons_service

router = APIRouter()


@router.get('/search', dependencies=[Depends(PaginatedParams)])
async def search_persons(
    query: str | None = Query(None),
    page_number: int = Query(
        PaginatedParams.default_page_number,
        description='Page number',
        ge=PaginatedParams.page_number_ge,
    ),
    page_size: int = Query(
        PaginatedParams.default_page_size,
        description='Number of films per page',
        ge=PaginatedParams.page_size_ge,
    ),
    person_service: PersonService = Depends(get_persons_service),
):
    """Получение списка персон"""

    persons = await person_service.get_persons(page_size, page_number, query)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    return persons


@router.get('/{person_id}')
async def get_person(
    person_id: UUID,
    person_service: PersonService = Depends(get_persons_service),
):
    """Получение персоны по его id"""

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}/film')
async def get_person_and_films(
    person_id: UUID,
    person_service: PersonService = Depends(get_persons_service),
):
    """Получение фильмов персоны по его id"""

    person = await person_service.get_films_by_person_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person

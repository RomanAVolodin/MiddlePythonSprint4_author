from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('', response_model=list[Genre])
async def get_genres(
    genre_service: GenreService = Depends(get_genre_service),
):
    """Получение списка жанров"""

    genres = await genre_service.get_genres()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return genres


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
    genre_id: UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    """Получение жанра по его id"""

    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre

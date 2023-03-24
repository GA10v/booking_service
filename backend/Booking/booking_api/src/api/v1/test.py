from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.post(
    '/test_ok',
    summary='Test OK',
    description='Тест OK',
)
async def test_ok(request: Request) -> HTTPStatus:
    return HTTPStatus.OK


@router.post(
    '/test_bad',
    summary='Test UNAUTHORIZED',
    description='Тест UNAUTHORIZED',
)
async def test_bad(request: Request) -> HTTPStatus:
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='test')

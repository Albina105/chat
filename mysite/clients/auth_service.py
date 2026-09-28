import httpx
from fastapi import HTTPException
from mysite.config import AUTH_SERVICE_URL


async def verify_access_token(token: str):
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(
                url=f'{AUTH_SERVICE_URL}/auth/verify/',
                headers={'Authorization': f'Bearer {token}'}
            )
    except httpx.RequestError:
        raise HTTPException(detail='Auth Service иштеген жок', status_code=500)

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail='Access token неправильный или просрочен')

    if response.status_code != 200:
        raise HTTPException(status_code=503, detail='Ошибка')

    try:
        user_data = response.json()

        return {
            "id": int(user_data['id']),
            "username": user_data['username'],
            'is_official': user_data['is_official'],
        }
    except (KeyError, TypeError, ValueError):
        raise HTTPException(status_code=500, detail='Неправильные данные')
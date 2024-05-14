from httpx import AsyncClient
from service.services import generate_hash, validate_secret_key

secret_key = ''


async def test_generate_secret(client: AsyncClient):
    global secret_key

    response = await client.post("/generate", json={
        "codePhrase": "123",
        "secret": "string",
        "secretKey": "string",
        "isActive": True,
        "lifetimeDays": 7,
        "expireAt": "2024-05-17T08:44:23.911114"
    })

    assert response.status_code == 201
    assert response.json()['secret_key']

    secret_key = response.json()['secret_key']


async def test_get_secret(client: AsyncClient):
    response = await client.get(f"/secrets/{secret_key}?code_phrase=123")
    assert response.status_code == 200
    assert response.json()['secret']


async def test_get_expired_secret(client: AsyncClient):
    response = await client.get(f"/secrets/{secret_key}?code_phrase=123")
    assert response.status_code == 403
    assert response.json()['detail'] == 'Secret is not active'


async def test_get_secret_not_found(client: AsyncClient):
    response = await client.get(f"/secrets/123?code_phrase=123")

    assert response.status_code == 404
    assert response.json()['detail'] == 'Secret not found or code phrase not valid'


async def test_generate_hash():
    hash_string = await generate_hash('string')

    assert isinstance(hash_string, str)


async def test_validate_secret_key():
    assert await validate_secret_key(secret_key, '123') == True


async def test_invalid_secret_key():
    assert await validate_secret_key(secret_key, '1234') == False

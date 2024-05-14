from datetime import timedelta, datetime

from .schemas import SecretDTO
from database.db import Secret
from fastapi import APIRouter, status, HTTPException, Depends
from .services import generate_hash, validate_secret_key, generate_crypto_secret, decrypt_crypto_secret

router = APIRouter(
    tags=["Secret"],

)


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_secret(secret: SecretDTO) -> dict:
    try:
        secret.secret_key = await generate_hash(secret.secret + secret.code_phrase + str(datetime.utcnow()))
        secret.code_phrase = await generate_hash(secret.code_phrase)
        secret.expire_at = datetime.utcnow() + timedelta(days=secret.lifetime_days)
        secret.secret = await generate_crypto_secret(secret=secret.secret)

        await Secret.insert_one(
            secret.model_dump(by_alias=False, exclude={'id'})
        )

        return {'secret_key': secret.secret_key}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/secrets/{secret_key}', status_code=status.HTTP_200_OK)
async def get_secret(secret_key: str, code_phrase: str = ''):

    if await validate_secret_key(secret_key=secret_key, code_phrase=code_phrase):

        secret = await Secret.find_one({"$and": [{'secret_key': secret_key},
                                                 {'code_phrase': await generate_hash(code_phrase)}]})

        if not secret['is_active']:
            raise HTTPException(status_code=403, detail="Secret is not active")

        await Secret.update_one(
            {'secret_key': secret_key},
            {'$set': {'is_active': False}}
        )

        return {'secret': await decrypt_crypto_secret(secret['secret'])}

    else:
        raise HTTPException(status_code=404, detail="Secret not found or code phrase not valid or secret expired")

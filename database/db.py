import motor.motor_asyncio
import pymongo

from settings import settings

url_prod = f'mongodb://{settings.MONGO_INITDB_ROOT_USERNAME}:{settings.MONGO_INITDB_ROOT_PASSWORD}@mongo:27017'
url_localhost = f'mongodb://localhost:27017'


client = motor.motor_asyncio.AsyncIOMotorClient(
    url_prod,
    uuidRepresentation="standard",
)

db = client['secrets']
Secret = db['Secret']


async def create_indexes():
    await db['Secret'].create_index([('secret_key', pymongo.ASCENDING)])
    await db['Secret'].create_index([("expire_at", 1)], expireAfterSeconds=10)

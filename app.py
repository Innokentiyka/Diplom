from fastapi import FastAPI

from database.db import create_indexes
from service.router import router as service_router


app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_indexes()

app.include_router(service_router)

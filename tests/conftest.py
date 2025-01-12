import asyncio

import pytest
from httpx import AsyncClient
from app import app


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

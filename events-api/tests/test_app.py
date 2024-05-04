from fastapi import status

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_heartbeat(fastapi_client: AsyncClient) -> None:
    response = await fastapi_client.get("/heartbeat")
    response.json()
    # assert data["version"] == version
    assert response.status_code == status.HTTP_200_OK

    assert response.json()['version'] == '0.0.1'
    assert response.json()['description'] == 'Events API'

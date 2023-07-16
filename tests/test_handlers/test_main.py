from httpx import AsyncClient


async def test_main(ac: AsyncClient):
    response = await ac.get('/')

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from TracFolio!"
    }

from httpx import Response
from fastapi.testclient import TestClient

from main import app


client: TestClient = TestClient(app=app)

base_url = "http://127.0.0.1:8000/"
base_headers: dict[str, str] = {"Accept": "application/json; version=1"}


def make_request(url, method="GET", headers={}, data={}) -> Response:
    headers = dict(base_headers, **headers)
    if method == "POST":
        return client.post(url=url, headers=headers, json=data)
    return client.get(url=url, headers=headers)

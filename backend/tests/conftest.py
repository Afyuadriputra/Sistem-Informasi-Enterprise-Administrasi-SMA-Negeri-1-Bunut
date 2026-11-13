import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_headers():
    def _headers(token=None, request_id="req-test-12345"):
        h = {"HTTP_X_REQUEST_ID": request_id}
        if token:
            h["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        return h

    return _headers

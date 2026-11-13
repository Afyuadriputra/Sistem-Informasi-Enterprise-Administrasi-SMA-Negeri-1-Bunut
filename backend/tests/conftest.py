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


@pytest.fixture(autouse=True)
def test_private_media_root(tmp_path, settings):
    media_dir = tmp_path / "private_media"
    media_dir.mkdir(parents=True, exist_ok=True)
    settings.PRIVATE_MEDIA_ROOT = str(media_dir)

import json

import pytest

import aphids


def test_status(client):
    rv = client.get('/status')
    assert rv.status_code == 200
    assert json.loads(rv.data.decode()) == {'status': 'ok'}


def test_version(client):
    rv = client.get('/version')
    assert rv.status_code == 200
    assert json.loads(rv.data.decode()) == {'version': '0.1.0'}


@pytest.fixture
def client():
    return aphids.app.test_client()

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


def test_welcome(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<a href="/authenticate">authenticate</a>' in rv.data
    assert b'<a href="/register">create account</a>' in rv.data
    assert b'good' in rv.data; assert b'justice' in rv.data


def test_authenticate(client):
    rv = client.get('/authenticate')
    assert rv.status_code == 200


def test_register(client):
    rv = client.get('/register')
    assert rv.status_code == 200


@pytest.fixture
def client():
    return aphids.app.test_client()

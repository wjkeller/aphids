import json

from lxml import html
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


def test_success_page(client):
    rv = client.get('/success?user=test_success_page_user')
    assert rv.status_code == 200
    assert b'test_success_page_user' in rv.data


def test_authenticate_form(client):
    rv = client.get('/authenticate')
    assert rv.status_code == 200
    doc = html.fromstring(rv.data)
    form, = doc.forms
    assert form.action == None
    assert form.method == 'POST'
    assert set(form.inputs.keys()) == {'csrf_token', 'username', 'password'}
    username = form.inputs['username']
    assert username.type == 'text'
    password = form.inputs['password']
    assert password.type == 'password'


@pytest.mark.parametrize('url,fields', (
    ('/authenticate', ('username', 'password')),
    ('/register', ('username', 'password', 'confirm_password')),
))
def test_csrf(client, url, fields):
    rv = client.post(url, data={name: 'data' for name in fields})
    doc = html.fromstring(rv.data)
    form, = doc.forms
    error_elem, = form.cssselect('.error')
    assert error_elem.text == 'CSRF token missing'


@pytest.mark.parametrize('username,password,error', (
    ('', '', 'all fields required'),
    ('user', '', 'all fields required'),
    ('', 'pass', 'all fields required'),
    ('user', 'pass', 'invalid credentials'),
))
def test_authenticate_error(client, username, password, error):
    rv = client.post('/authenticate', data={
        'csrf_token': get_csrf_token(client, '/authenticate'),
        'username': username,
        'password': password,
    })
    assert rv.status_code == 200
    doc = html.fromstring(rv.data)
    form, = doc.forms
    error_elem, = form.cssselect('.error')
    assert error_elem.text == error


def test_authenticate_success(client):
    username = 'test_authenticate_succes_user'
    password = 'password'
    user = aphids.User(username, password)
    aphids.db.session.add(user)
    aphids.db.session.commit()
    rv = client.post('/authenticate', data={
        'csrf_token': get_csrf_token(client, '/authenticate'),
        'username': username,
        'password': password,
    })
    assert rv.status_code == 302
    assert rv.location == 'http://localhost/success?user=' + username


def test_register_form(client):
    rv = client.get('/register')
    assert rv.status_code == 200
    doc = html.fromstring(rv.data)
    form, = doc.forms
    assert form.action == None
    assert form.method == 'POST'
    assert set(form.inputs.keys()) == {'csrf_token', 'username',
                                       'password', 'confirm_password'}
    username = form.inputs['username']
    assert username.type == 'text'
    password = form.inputs['password']
    assert password.type == 'password'
    confirm_password = form.inputs['confirm_password']
    assert confirm_password.type == 'password'


@pytest.mark.parametrize('username,password,confirm,error', (
    ('', '', '', 'all fields required'),
    ('user', '', '', 'all fields required'),
    ('', 'pass', '', 'all fields required'),
    ('user', 'pass', '', 'all fields required'),
    ('user', '', 'pass', 'all fields required'),
    ('', 'pass', 'pass', 'all fields required'),
    ('user', 'pass', 'pas', 'password mismatch'),
))
def test_register_error(client, username, password, confirm, error):
    rv = client.post('/register', data={
        'csrf_token': get_csrf_token(client, '/register'),
        'username': username,
        'password': password,
        'confirm_password': confirm,
    })
    assert rv.status_code == 200
    doc = html.fromstring(rv.data)
    form, = doc.forms
    error_elem, = form.cssselect('.error')
    assert error_elem.text == error


def test_register_success(client):
    username = 'test_register_success_user'
    rv = client.post('/register', data={
        'csrf_token': get_csrf_token(client, '/register'),
        'username': username,
        'password': 'password',
        'confirm_password': 'password',
    })
    assert rv.status_code == 302
    assert rv.location == 'http://localhost/success?user=' + username


@pytest.fixture
def client():
    aphids.db.create_all()
    return aphids.app.test_client()


def get_csrf_token(client, url):
    rv = client.get(url)
    doc = html.fromstring(rv.data)
    form, = doc.forms
    return form.inputs['csrf_token'].value

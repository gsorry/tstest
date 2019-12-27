from flask import url_for


def test_register(client):
    response = client.get(url_for('auth.registerresource'))
    assert response.status_code == 200


def test_login(client):
    response = client.get(url_for('auth.loginresource'))
    assert response.status_code == 200


def test_request_password(client):
    response = client.get(url_for('auth.requestpasswordresource'))
    assert response.status_code == 200

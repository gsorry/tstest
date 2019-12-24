
def test_not_found(client):
    response = client.get('/dummy/')
    assert response.status_code == 404

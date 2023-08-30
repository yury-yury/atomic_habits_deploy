def test_root_not_found(client):
    response = client.get('/false/')

    assert response.status_code == 404

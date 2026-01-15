def test_users_fetch(client):
    res = client.get("/users")
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_organizations_fetch(client):
    res = client.get("/organizations")
    assert res.status_code == 200

def test_opportunities_fetch(client):
    res = client.get("/opportunities")
    assert res.status_code == 200

def test_applications_fetch(client):
    res = client.get("/applications")
    assert res.status_code == 200

def test_payments_fetch(client):
    res = client.get("/payments")
    assert res.status_code == 200


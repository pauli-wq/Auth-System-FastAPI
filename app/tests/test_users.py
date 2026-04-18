from fastapi import status


# test para crear usuarios
def test_create_user(client, test_user):
    resp = client.post(
        "/users",
        json={
            "username": "jorge_perez",
            "email": "example@test.com",
            "full_name": "Jorge Luis",
            "password": "user213",
        },
    )
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert data["username"] == "jorge_perez"
    assert data["email"] == "example@test.com"
    assert data["full_name"] == "Jorge Luis"


# test donde devolvemos una lista de usuario
def test_get_list_users(client, test_user):
    resp = client.get("/users")
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.json(), list)

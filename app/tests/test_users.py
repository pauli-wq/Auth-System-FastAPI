from fastapi import status

from app.tests.conftest import test_engine


# test para crear usuarios
def test_create_user(client):
    resp = client.post(
        "/users",
        json={
            "username": "test_user",
            "email": "example@test.com",
            "full_name": "Test User",
            "password": "user213",
        },
    )
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert data["username"] == "test_user"
    assert data["email"] == "example@test.com"
    assert data["full_name"] == "Test User"


# test donde devolvemos una lista de usuario
def test_get_list_users(client):
    resp = client.get("/users")
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.json(), list)


# obtener usuario por ID
def test_get_user_id(client, test_user):
    resp = client.get(f"/users/{test_user.id}")
    assert resp.status_code == status.HTTP_200_OK


# para ID inexistente
def test_get_id_not_found(client):
    resp = client.get("/users/333")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


# test actualizar usuario
def test_update_user(client, test_user):
    # hacemos login para obtener el token
    login_data = {"username": test_user.username, "password": "secret123"}
    resp = client.post("auth/login", data=login_data)
    assert resp.status_code == status.HTTP_200_OK

    # actualizamos usuario con datos nuevos
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"username": "New Test"}  # nuevos datos
    resp = client.put(f"users/{test_user.id}", json=update_data, headers=headers)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["username"] == "New Test"


# test usuario no autorizado
def test_update_user_unauthorized(client, test_user):
    # actualizamos sin enviar el token header
    resp = client.put(f"/users/{test_user.id}", json={"username": "Testing User"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

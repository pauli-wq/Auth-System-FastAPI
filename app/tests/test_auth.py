from fastapi import status


# test para el endpoint loging
def test_login_success(client, test_user):
    resp = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": "secret123"},
    )
    assert resp.status_code == status.HTTP_200_OK


def test_get_user_info_valid_token(client, test_user):
    # login para obtener el token
    login_resp = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": "secret123"},
    )
    assert login_resp.status_code == status.HTTP_200_OK
    token = login_resp.json()["access_token"]

    # obtener info del usuario con el token
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/users/profile", headers=headers)
    assert resp.status_code == status.HTTP_200_OK


# sin token el acceso es denegado
def test_get_user_info_unauthorized(client):
    resp = client.get("/users/profile")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# verifica que con clave incorrecta falle
def test_wrong_pass(client, test_user):
    resp = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": "NaN123"},
    )
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

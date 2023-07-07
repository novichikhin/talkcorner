import uuid

from httpx import AsyncClient

from talkcorner.common.database.holder import DatabaseHolder
from tests.fixtures.protocols.auth_token import CreateAuthAccessToken, CreateAuthRefreshToken
from tests.fixtures.protocols.user import CreateUser


async def test_login_user(client: AsyncClient, create_user: CreateUser):
    user = await create_user(password=(password:="qwerty12345"))

    response = await client.post(
        "/api/v1/user/login",
        data={
            "username": user.username,
            "password": password
        }
    )

    assert response.status_code == 200

    json = response.json()

    assert (access_token := json["access_token"])
    assert json["refresh_token"]
    assert json["token_type"]

    response = await client.get(
        "/api/v1/user/",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


async def test_refresh_token(
        client: AsyncClient,
        create_user: CreateUser,
        create_auth_refresh_token: CreateAuthRefreshToken
):
    user = await create_user()

    response = await client.post(
        "/api/v1/user/refresh",
        headers={"Authorization": f"Bearer {create_auth_refresh_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert (access_token := json["access_token"])
    assert json["token_type"]

    response = await client.get(
        "/api/v1/user/",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


async def test_email_verify(
        client: AsyncClient,
        create_user: CreateUser,
        create_auth_access_token: CreateAuthAccessToken,
        holder: DatabaseHolder
):
    user = await create_user(email_verified=False)

    response = await client.get(
        f"/api/v1/user/email/verify/{str(user.email_token)}",
        headers={"Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    verified_user = await holder.user.read_by_id(user_id=user.id)

    assert verified_user

    assert verified_user.email_verified == json["email_verified"]


async def test_get_users(
        client: AsyncClient,
        create_user: CreateUser,
        create_auth_access_token: CreateAuthAccessToken
):
    user = await create_user()

    response = await client.get(
        "/api/v1/user/",
        headers={"Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert len(json) == 1

    assert str(user.id) == json[0]["id"]
    assert user.username == json[0]["username"]


async def test_get_user(
        client: AsyncClient,
        create_user: CreateUser,
        create_auth_access_token: CreateAuthAccessToken
):
    user = await create_user()

    response = await client.get(
        f"/api/v1/user/{user.id}",
        headers={"Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert str(user.id) == json["id"]
    assert user.username == json["username"]


async def test_create_user(client: AsyncClient, holder: DatabaseHolder):
    response = await client.post(
        "/api/v1/user/",
        json={
            "username": "Test User",
            "password": "qwerty12345",
            "email": "test@ya.ru"
        }
    )

    assert response.status_code == 200

    json = response.json()

    assert "id" in json

    user = await holder.user.read_by_id(user_id=uuid.UUID(json["id"]))

    assert user

    assert user.username == json["username"]
    assert user.email == json["email"]
    assert user.email_verified == json["email_verified"]

from httpx import AsyncClient
from passlib.context import CryptContext

from talkcorner.common.database.holder import DatabaseHolder
from tests.fixtures.protocols.auth_token import CreateAuthToken
from tests.fixtures.protocols.user import CreateUser


async def test_get_forums(
        client: AsyncClient,
        crypt_context: CryptContext,
        holder: DatabaseHolder,
        create_user: CreateUser,
        create_auth_token: CreateAuthToken
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum",
        description=None,
        creator_id=user.id
    )

    assert forum

    response = await client.get(
        "/api/v1/forum/",
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert len(json) == 1

    assert forum.id == json[0]["id"]
    assert forum.title == json[0]["title"]
    assert forum.description == json[0]["description"]
    assert str(forum.creator_id) == json[0]["creator_id"]


async def test_get_forum(
        client: AsyncClient,
        crypt_context: CryptContext,
        holder: DatabaseHolder,
        create_user: CreateUser,
        create_auth_token: CreateAuthToken
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum",
        description=None,
        creator_id=user.id
    )

    assert forum

    response = await client.get(
        f"/api/v1/forum/{forum.id}",
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert forum.id == json["id"]
    assert forum.title == json["title"]
    assert forum.description == json["description"]
    assert str(forum.creator_id) == json["creator_id"]


async def test_create_forum(
        client: AsyncClient,
        crypt_context: CryptContext,
        holder: DatabaseHolder,
        create_user: CreateUser,
        create_auth_token: CreateAuthToken
):
    user = await create_user()

    response = await client.post(
        "/api/v1/forum/",
        json={
            "title": "Test Forum",
            "description": "Test Forum Description"
        },
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert "id" in json

    forum = await holder.forum.read_by_id(forum_id=json["id"])

    assert forum

    assert forum.title == json["title"]
    assert forum.description == json["description"]


async def test_update_forum(
        client: AsyncClient,
        crypt_context: CryptContext,
        holder: DatabaseHolder,
        create_user: CreateUser,
        create_auth_token: CreateAuthToken
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum",
        description=None,
        creator_id=user.id
    )

    assert forum

    new_description = "New Description"

    response = await client.put(
        f"/api/v1/forum/{forum.id}",
        json={
            "description": new_description
        },
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert forum.id == json["id"]

    forum = await holder.forum.read_by_id(forum_id=json["id"])

    assert forum

    assert forum.description == new_description


async def test_delete_forum(
        client: AsyncClient,
        crypt_context: CryptContext,
        holder: DatabaseHolder,
        create_user: CreateUser,
        create_auth_token: CreateAuthToken
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum",
        description=None,
        creator_id=user.id
    )

    assert forum

    response = await client.delete(
        f"/api/v1/forum/{forum.id}",
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert forum.id == json["id"]

    forum = await holder.forum.read_by_id(forum_id=json["id"])

    assert not forum

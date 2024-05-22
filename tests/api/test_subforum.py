import pytest
from httpx import AsyncClient

from talkcorner.exceptions.subforum import SubforumNotFoundError
from talkcorner.database.holder import DatabaseHolder
from tests.fixtures.protocols.auth_token import CreateAuthAccessToken
from tests.fixtures.protocols.user import CreateUser


async def test_get_subforums(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    parent_forum = await holder.forum.create(
        title="Parent Forum", description=None, creator_id=user.id
    )

    child_forum = await holder.forum.create(
        title="Child Forum", description=None, creator_id=user.id
    )

    subforum = await holder.subforum.create(
        parent_forum_id=parent_forum.id,
        child_forum_id=child_forum.id,
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.get(
        "/api/v1/subforum/",
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert len(json) == 1

    assert subforum.id == json[0]["id"]
    assert subforum.parent_forum_id == json[0]["parent_forum_id"]
    assert subforum.child_forum_id == json[0]["child_forum_id"]
    assert str(subforum.creator_id) == json[0]["creator_id"]


async def test_get_subforum(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    parent_forum = await holder.forum.create(
        title="Parent Forum", description=None, creator_id=user.id
    )

    child_forum = await holder.forum.create(
        title="Child Forum", description=None, creator_id=user.id
    )

    subforum = await holder.subforum.create(
        parent_forum_id=parent_forum.id,
        child_forum_id=child_forum.id,
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.get(
        f"/api/v1/subforum/{subforum.id}",
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert subforum.id == json["id"]
    assert subforum.parent_forum_id == json["parent_forum_id"]
    assert subforum.child_forum_id == json["child_forum_id"]
    assert str(subforum.creator_id) == json["creator_id"]


async def test_create_subforum(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    parent_forum = await holder.forum.create(
        title="Parent Forum", description=None, creator_id=user.id
    )

    child_forum = await holder.forum.create(
        title="Child Forum", description=None, creator_id=user.id
    )

    await holder.commit()

    response = await client.post(
        "/api/v1/subforum/",
        json={"parent_forum_id": parent_forum.id, "child_forum_id": child_forum.id},
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert "id" in json

    subforum = await holder.subforum.read_by_id(subforum_id=json["id"])

    assert subforum

    assert subforum.parent_forum_id == json["parent_forum_id"]
    assert subforum.child_forum_id == json["child_forum_id"]
    assert str(subforum.creator_id) == json["creator_id"]


async def test_patch_subforum(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    parent_forum = await holder.forum.create(
        title="Parent Forum", description=None, creator_id=user.id
    )

    child_forum = await holder.forum.create(
        title="Child Forum", description=None, creator_id=user.id
    )

    subforum = await holder.subforum.create(
        parent_forum_id=parent_forum.id,
        child_forum_id=child_forum.id,
        creator_id=user.id,
    )

    new_child_forum = await holder.forum.create(
        title="New Child Forum", description=None, creator_id=user.id
    )

    await holder.commit()

    response = await client.patch(
        f"/api/v1/subforum/{subforum.id}",
        json={"child_forum_id": new_child_forum.id},
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert subforum.id == json["id"]

    updated_subforum = await holder.subforum.read_by_id(subforum_id=json["id"])

    assert updated_subforum

    assert updated_subforum.child_forum_id == new_child_forum.id


async def test_delete_subforum(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    parent_forum = await holder.forum.create(
        title="Parent Forum", description=None, creator_id=user.id
    )

    child_forum = await holder.forum.create(
        title="Child Forum", description=None, creator_id=user.id
    )

    subforum = await holder.subforum.create(
        parent_forum_id=parent_forum.id,
        child_forum_id=child_forum.id,
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.delete(
        f"/api/v1/subforum/{subforum.id}",
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert subforum.id == json["id"]

    with pytest.raises(SubforumNotFoundError):
        await holder.subforum.read_by_id(subforum_id=json["id"])

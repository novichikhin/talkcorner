import uuid

import pytest
from httpx import AsyncClient

from talkcorner.exceptions.topic.main import TopicNotFoundError
from talkcorner.database.holder import DatabaseHolder
from tests.fixtures.protocols.auth_token import CreateAuthAccessToken
from tests.fixtures.protocols.user import CreateUser


async def test_get_topics(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum", description=None, creator_id=user.id
    )

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.get(
        "/api/v1/topic/",
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert len(json) == 1

    assert str(topic.id) == json[0]["id"]
    assert topic.title == json[0]["title"]
    assert topic.body == json[0]["body"]
    assert str(topic.creator_id) == json[0]["creator_id"]


async def test_get_topic(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum", description=None, creator_id=user.id
    )

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.get(
        f"/api/v1/topic/{topic.id}",
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert str(topic.id) == json["id"]
    assert topic.title == json["title"]
    assert topic.body == json["body"]
    assert str(topic.creator_id) == json["creator_id"]


async def test_create_topic(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum", description=None, creator_id=user.id
    )

    await holder.commit()

    response = await client.post(
        "/api/v1/topic/",
        json={
            "forum_id": forum.id,
            "title": "Test Title Topic",
            "body": "Test Body Topic",
        },
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert "id" in json

    topic = await holder.topic.read_by_id(topic_id=uuid.UUID(json["id"]))

    assert topic

    assert str(topic.id) == json["id"]
    assert topic.title == json["title"]
    assert topic.body == json["body"]
    assert str(topic.creator_id) == json["creator_id"]


async def test_patch_topic(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    new_title = "New Test Title Topic"
    new_body = "New Test Body Topic"

    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum", description=None, creator_id=user.id
    )

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.patch(
        f"/api/v1/topic/{topic.id}",
        json={"title": new_title, "body": new_body},
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert str(topic.id) == json["id"]

    updated_topic = await holder.topic.read_by_id(topic_id=uuid.UUID(json["id"]))

    assert updated_topic

    assert updated_topic.title == new_title
    assert updated_topic.body == new_body


async def test_delete_topic(
    client: AsyncClient,
    holder: DatabaseHolder,
    create_user: CreateUser,
    create_auth_access_token: CreateAuthAccessToken,
):
    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum", description=None, creator_id=user.id
    )

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id,
    )

    await holder.commit()

    response = await client.delete(
        f"/api/v1/topic/{topic.id}",
        headers={
            "Authorization": f"Bearer {create_auth_access_token(user_id=user.id)}"
        },
    )

    assert response.status_code == 200

    json = response.json()

    assert str(topic.id) == json["id"]

    with pytest.raises(TopicNotFoundError):
        await holder.topic.read_by_id(topic_id=uuid.UUID(json["id"]))

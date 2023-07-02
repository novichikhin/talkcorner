import uuid

from httpx import AsyncClient

from talkcorner.common.database.holder import DatabaseHolder
from tests.fixtures.protocols.auth_token import CreateAuthToken
from tests.fixtures.protocols.user import CreateUser


async def test_get_topic_messages(
        client: AsyncClient,
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

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id
    )

    topic_message = await holder.topic_message.create(
        topic_id=topic.id,
        body="Test Body Topic Message",
        creator_id=user.id
    )

    response = await client.get(
        "/api/v1/topic/message/",
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert len(json) == 1

    assert str(topic_message.id) == json[0]["id"]
    assert topic_message.body == json[0]["body"]
    assert str(topic_message.creator_id) == json[0]["creator_id"]


async def test_get_topic_message(
        client: AsyncClient,
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

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id
    )

    topic_message = await holder.topic_message.create(
        topic_id=topic.id,
        body="Test Body Topic Message",
        creator_id=user.id
    )

    response = await client.get(
        f"/api/v1/topic/message/{topic_message.id}",
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert str(topic_message.id) == json["id"]
    assert topic_message.body == json["body"]
    assert str(topic_message.creator_id) == json["creator_id"]


async def test_create_topic_message(
        client: AsyncClient,
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

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id
    )

    response = await client.post(
        "/api/v1/topic/message/",
        json={
            "topic_id": str(topic.id),
            "body": "Test Body Topic Message"
        },
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert "id" in json

    topic_message = await holder.topic_message.read_by_id(topic_message_id=uuid.UUID(json["id"]))

    assert topic_message

    assert str(topic_message.id) == json["id"]
    assert topic_message.body == json["body"]
    assert str(topic_message.creator_id) == json["creator_id"]


async def test_update_topic_message(
        client: AsyncClient,
        holder: DatabaseHolder,
        create_user: CreateUser,
        create_auth_token: CreateAuthToken
):
    new_body = "New Test Body Topic Message"

    user = await create_user()

    forum = await holder.forum.create(
        title="Test Forum",
        description=None,
        creator_id=user.id
    )

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id
    )

    topic_message = await holder.topic_message.create(
        topic_id=topic.id,
        body="Test Body Topic Message",
        creator_id=user.id
    )

    response = await client.put(
        f"/api/v1/topic/message/{topic_message.id}",
        json={
            "body": new_body
        },
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert str(topic_message.id) == json["id"]

    updated_topic_message = await holder.topic_message.read_by_id(topic_message_id=uuid.UUID(json["id"]))

    assert updated_topic_message

    assert updated_topic_message.body == new_body


async def test_delete_topic_message(
        client: AsyncClient,
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

    topic = await holder.topic.create(
        forum_id=forum.id,
        title="Test Title Topic",
        body="Test Body Topic",
        creator_id=user.id
    )

    topic_message = await holder.topic_message.create(
        topic_id=topic.id,
        body="Test Body Topic Message",
        creator_id=user.id
    )

    response = await client.delete(
        f"/api/v1/topic/message/{topic_message.id}",
        headers={"Authorization": f"Bearer {create_auth_token(user_id=user.id)}"}
    )

    assert response.status_code == 200

    json = response.json()

    assert str(topic_message.id) == json["id"]

    deleted_topic_message = await holder.topic_message.read_by_id(topic_message_id=uuid.UUID(json["id"]))

    assert not deleted_topic_message

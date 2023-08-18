import asyncio
import os

import msgpack
import pydantic

from nats.aio.msg import Msg
from nats.errors import TimeoutError

from talkcorner.common.queue.nats.factory import (
    nats_create_connect,
    nats_create_jetstream,
    nats_build_connection_uri
)

from talkcorner.common.settings.environments.base import AppEnvTypes
from talkcorner.common.settings.main import get_app_settings
from talkcorner.common.types.broadcast.email import EmailBroadcast
from talkcorner.queue.nats.broadcaster.email.services.broadcaster.email import EmailBroadcaster


async def send_an_email(msg: Msg, email_broadcaster: EmailBroadcaster) -> None:
    unpacked_data = msgpack.unpackb(msg.data)

    try:
        email_broadcast = EmailBroadcast(**unpacked_data)
    except pydantic.ValidationError:
        return

    if await email_broadcaster.send(
        to_address=email_broadcast.to_address,
        subject=email_broadcast.subject,
        html=email_broadcast.html
    ):
        await msg.ack()


async def main():
    settings = get_app_settings(
        app_env=AppEnvTypes.prod if os.getenv("IS_PRODUCTION") else AppEnvTypes.dev
    )

    nc = await nats_create_connect(
        connection_uri=[
            nats_build_connection_uri(
                host=settings.nats_host,
                port=settings.nats_client_port,
                user=settings.nats_user,
                password=settings.nats_password
            )
        ]
    )
    js = nats_create_jetstream(nats=nc)

    subscribe = await js.pull_subscribe(
        subject=f"{settings.nats_stream_name}.broadcast.email.*",
        durable=f"{settings.nats_stream_name}-broadcast-email-sub",
        stream=settings.nats_stream_name
    )

    if not subscribe:
        await nc.close()
        raise RuntimeError("No consumer subscription")

    email_broadcaster = EmailBroadcaster(
        host=settings.email_host,
        port=settings.email_port,
        from_address=settings.email_from_address,
        password=settings.email_password
    )

    while True:
        await asyncio.sleep(5.)

        try:
            msgs = await subscribe.fetch(5)
        except TimeoutError:
            continue

        tasks = [
            asyncio.create_task(send_an_email(msg=msg, email_broadcaster=email_broadcaster))
            for msg in msgs
        ]
        await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())

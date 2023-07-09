import asyncio

import msgpack
import pydantic

from nats.aio.msg import Msg
from nats.errors import TimeoutError

from talkcorner.common import types
from talkcorner.common.queue.nats.factory import (
    nats_create_connect,
    nats_create_jetstream,
    js_create_or_update_stream
)
from talkcorner.common.services.broadcaster.email import EmailBroadcaster


async def send_an_email(msg: Msg, email_broadcaster: EmailBroadcaster) -> None:
    unpacked_data = msgpack.unpackb(msg.data)

    try:
        email_broadcast = types.EmailBroadcast(**unpacked_data)
    except pydantic.ValidationError:
        return

    if await email_broadcaster.send(
        to_address=email_broadcast.to_address,
        subject=email_broadcast.subject,
        html=email_broadcast.html
    ):
        await msg.ack()


async def main():
    settings = types.Setting()

    nc = await nats_create_connect(connection_uri=settings.nats_url)
    js = nats_create_jetstream(nats=nc)

    await js_create_or_update_stream(js=js, stream_name=settings.nats_stream_name)

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

        tasks = [asyncio.create_task(send_an_email(msg=msg, email_broadcaster=email_broadcaster)) for msg in msgs]
        await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())

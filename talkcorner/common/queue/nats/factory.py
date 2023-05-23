import nats
from nats.js import JetStreamContext, api
from nats.js.errors import NotFoundError


async def nats_create_connect(connection_uri: str) -> nats.NATS:
    return await nats.connect(servers=connection_uri)


def nats_create_jetstream(nats: nats.NATS) -> JetStreamContext:
    return nats.jetstream()


async def js_create_or_update_stream(js: JetStreamContext, stream_name: str) -> None:
    subjects = [
        "talkcorner.broadcast.*"
    ]
    try:
        await js.update_stream(
            config=api.StreamConfig(
                name=stream_name,
                subjects=subjects
            )
        )
    except NotFoundError:
        await js.add_stream(name=stream_name, subjects=subjects)

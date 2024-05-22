from typing import Optional

from nats.js import JetStreamContext, api


class JetStreamContextMock(JetStreamContext):

    async def publish(
        self,
        subject: str,
        payload: bytes = b"",
        timeout: Optional[float] = None,
        stream: Optional[str] = None,
        headers: Optional[dict] = None,
    ) -> api.PubAck:
        return api.PubAck(stream="mocked stream", seq=1)

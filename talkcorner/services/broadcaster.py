from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


@dataclass
class EmailBroadcaster:
    host: str
    port: int
    from_address: str
    password: str

    async def send(self, *, to_address: str, subject: str, html: str) -> bool:
        message = MIMEMultipart("multipart")

        message["From"] = self.from_address
        message["To"] = to_address
        message["Subject"] = subject
        message.attach(payload=MIMEText(html, "html"))

        errors, _ = await aiosmtplib.send(
            message=message,
            hostname=str(self.host),
            port=self.port,
            username=self.from_address,
            password=self.password,
        )

        return not errors

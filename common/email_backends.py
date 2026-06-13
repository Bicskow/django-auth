import os
import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage


class MailgunBackend(BaseEmailBackend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        self.api_url = f"https://api.eu.mailgun.net/v3/{self.domain}/messages"

    def send_messages(self, email_messages):
        for message in email_messages:
            payload = {
                "from": message.from_email,
                "to": ", ".join(message.to),
                "subject": message.subject,
            }

            # Add text body if present
            if message.body:
                payload["text"] = message.body

            # Add HTML body if present
            if hasattr(message, 'alternatives') and message.alternatives:
                for content, mime_type in message.alternatives:
                    if mime_type == "text/html":
                        payload["html"] = content
                        break

            # Add CC recipients
            if message.cc:
                payload["cc"] = ", ".join(message.cc)

            # Add BCC recipients
            if message.bcc:
                payload["bcc"] = ", ".join(message.bcc)

            # Add reply-to
            if message.reply_to:
                payload["h:Reply-To"] = ", ".join(message.reply_to)

            # Add attachments
            files = []
            for attachment in message.attachments:
                if isinstance(attachment, (list, tuple)) and len(attachment) >= 3:
                    filename, content, mime_type = attachment[:3]
                    files.append(("attachment", (filename, content, mime_type)))
                elif hasattr(attachment, 'filename'):
                    files.append(("attachment", (attachment.filename, attachment.content, attachment.mimetype)))

            response = requests.post(
                self.api_url,
                auth=("api", self.api_key),
                data=payload,
                files=files,
            )

            if response.status_code != 200:
                if response.status_code == 401:
                    raise Exception(
                        f"Mailgun API authentication error: Invalid API key. "
                        f"Check your MAILGUN_API_KEY environment variable."
                    )
                raise Exception(
                    f"Mailgun API error: {response.status_code} - {response.text}"
                )
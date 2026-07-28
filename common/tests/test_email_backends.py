import pytest
from unittest.mock import patch, Mock
from django.core.mail import EmailMessage, EmailMultiAlternatives
from common.email_backends import MailgunBackend
import responses

class TestMailgunBackend:
    @patch("common.email_backends.requests.post")
    def test_send_text_email(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        backend = MailgunBackend()

        email = EmailMessage(
            subject="Test Subject",
            body="This is a test email.",
            from_email="sender@example.com",
            to=["recipient@example.com"]
        )
        backend.send_messages([email])

        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]

        assert call_kwargs["data"]["from"] == "sender@example.com"
        assert call_kwargs["data"]["to"] == "recipient@example.com"
        assert call_kwargs["data"]["subject"] == "Test Subject"
        assert call_kwargs["data"]["text"] == "This is a test email."


    @responses.activate
    def test_send_messages_success(self, monkeypatch):
        monkeypatch.setenv("MAILGUN_API_KEY", "key-123")
        monkeypatch.setenv("MAILGUN_DOMAIN", "sandbox.test")

        responses.add(
            responses.POST,
            "https://api.eu.mailgun.net/v3/sandbox.test/messages",
            json={"message": "Queued. Thank you."},
            status=200,
        )

        backend = MailgunBackend()
        msg = EmailMessage(
            subject="Hi", body="Body", from_email="from@test.com", to=["to@test.com"]
        )
        backend.send_messages([msg])

        assert len(responses.calls) == 1
        request = responses.calls[0].request
        
        # Parse the form-encoded body and verify email fields
        from urllib.parse import parse_qs
        body_params = parse_qs(request.body)
        
        assert body_params["from"][0] == "from@test.com"
        assert body_params["to"][0] == "to@test.com"
        assert body_params["subject"][0] == "Hi"
        assert body_params["text"][0] == "Body"


    @responses.activate
    def test_send_messages_raises_on_401(self, monkeypatch):
        monkeypatch.setenv("MAILGUN_API_KEY", "bad")
        monkeypatch.setenv("MAILGUN_DOMAIN", "sandbox.test")
        responses.add(responses.POST, "https://api.eu.mailgun.net/v3/sandbox.test/messages", status=401)

        backend = MailgunBackend()
        with pytest.raises(Exception, match="authentication error"):
            backend.send_messages([EmailMessage("s", "b", "f@t.com", ["t@t.com"])])


    @responses.activate
    def test_send_messages_raises_on_500(self, monkeypatch):
        monkeypatch.setenv("MAILGUN_API_KEY", "key")
        monkeypatch.setenv("MAILGUN_DOMAIN", "sandbox.test")
        responses.add(responses.POST, "https://api.eu.mailgun.net/v3/sandbox.test/messages", status=500, json={})

        backend = MailgunBackend()
        with pytest.raises(Exception, match="Mailgun API error: 500"):
            backend.send_messages([EmailMessage("s", "b", "f@t.com", ["t@t.com"])])


    @patch("common.email_backends.requests.post")
    def test_send_html_email(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        backend = MailgunBackend()

        email = EmailMultiAlternatives(
            subject="HTML Email",
            body="Plain text fallback",
            from_email="sender@example.com",
            to=["recipient@example.com"],
        )
        email.attach_alternative("<h1>Hello</h1>", "text/html")
        backend.send_messages([email])

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["data"]["html"] == "<h1>Hello</h1>"
        assert call_kwargs["data"]["text"] == "Plain text fallback"


    @patch("common.email_backends.requests.post")
    def test_cc_bcc_reply_to(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        backend = MailgunBackend()

        email = EmailMessage(
            subject="Test",
            body="Body",
            from_email="from@example.com",
            to=["to@example.com"],
            cc=["cc@example.com"],
            bcc=["bcc@example.com"],
            reply_to=["reply@example.com"],
        )
        backend.send_messages([email])

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["data"]["cc"] == "cc@example.com"
        assert call_kwargs["data"]["bcc"] == "bcc@example.com"
        assert call_kwargs["data"]["h:Reply-To"] == "reply@example.com"

    
    @patch("common.email_backends.requests.post")
    def test_multiple_recipients(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        backend = MailgunBackend()

        email = EmailMessage(
            subject="Test", body="Body",
            from_email="f@e.com",
            to=["a@e.com", "b@e.com"],
        )
        backend.send_messages([email])

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["data"]["to"] == "a@e.com, b@e.com"


    def test_init_sets_api_key_and_domain(self, monkeypatch):
        monkeypatch.setenv("MAILGUN_API_KEY", "test-api-key")
        monkeypatch.setenv("MAILGUN_DOMAIN", "test.example.com")

        backend = MailgunBackend()

        assert backend.api_key == 'test-api-key'
        assert backend.domain == 'test.example.com'
        assert 'test.example.com' in backend.api_url
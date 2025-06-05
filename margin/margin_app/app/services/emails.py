"""Email service implementation using SendGrid."""

from typing import Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, TemplateId
from app.core.config import settings
from app.services.auth.base import create_access_token, get_expire_time
from mjml import mjml2html
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
import os

logger = logging.getLogger("EmailService")


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "mail", "email-templates")
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["mjml"])
) 

class EmailService:
    """SendGrid email operations."""

    def __init__(self) -> None:
        self.client = SendGridAPIClient(settings.sendgrid_api_key)
        self.sender = Email(
            email=settings.email_sender, name=settings.email_sender_name
        )

    def render_mjml_template(self, template_name: str, context: dict) -> str:
        """
        Render an MJML template with Jinja2 and convert it to HTML.
        """
        template = jinja_env.get_template(template_name)
        mjml_content = template.render(context)
        html_result = mjml2html(mjml_content)
        return html_result['html']      
 
    async def send_email(
        self,
        to_email: str | list[str],
        subject: str,
        content: str,
        is_html: bool = False,
        template_id: Optional[str] = None,
        template_data: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Send email through SendGrid."""
        try:
            to_emails = [to_email] if isinstance(to_email, str) else to_email

            message = Mail(
                from_email=self.sender,
                to_emails=[To(email=email) for email in to_emails],
                subject=subject,
            )

            if template_id:
                message.template_id = TemplateId(template_id)
                if template_data:
                    message.dynamic_template_data = template_data
            else:
                content_type = "text/html" if is_html else "text/plain"
                message.content = [Content(content_type, content)]

            if settings.email_test_mode:
                logger.info(
                    f"Test mode: Would send email:\n"
                    f"To: {to_emails}\n"
                    f"Subject: {subject}\n"
                    f"Content: {content[:100]}..."
                )
                return True

            response = self.client.send(message)
            logger.info(f"Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise

    async def reset_password_mail(self, to_email: str, username:str = None):
        """
        Sends a password reset email to the specified recipient.
        This method generates a password reset token for the given email address
        and sends an email containing a link to reset the password.
        Args:
            to_email (str): The recipient's email address.
        Returns:
            Coroutine: A coroutine that sends the email asynchronously.
        """
        token = create_access_token(
            email=to_email,
            expires_delta=get_expire_time(
                settings.reset_password_expire_minutes),
        )

        reset_link = f"{settings.host}/{settings.forget_password_url}/{token}"
        html_content = render_mjml_template(
            "reset_password.mjml",
            {"username": username, "reset_link": reset_link}
        )
        return await self.send_email(
            to_email=to_email,
            subject="Reset your password",
            content=html_content,
            is_html=True,
        )


email_service = EmailService()

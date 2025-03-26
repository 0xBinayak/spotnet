"""Email service implementation using SendGrid."""

from typing import List, Optional, Union, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, TemplateId
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """SendGrid email operations."""

    def __init__(self) -> None:
        self.client = SendGridAPIClient(settings.sendgrid_api_key)
        self.sender = Email(
            email=settings.email_sender,
            name=settings.email_sender_name
        )

    async def send_email(
        self,
        to_email: Union[str, List[str]],
        subject: str,
        content: str,
        is_html: bool = False,
        template_id: Optional[str] = None,
        template_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send email through SendGrid."""
        try:
            to_emails = [to_email] if isinstance(to_email, str) else to_email
            
            message = Mail(
                from_email=self.sender,
                to_emails=[To(email=email) for email in to_emails],
                subject=subject
            )

            if template_id:
                message.template_id = TemplateId(template_id)
                if template_data:
                    message.dynamic_template_data = template_data
            else:
                content_type = 'text/html' if is_html else 'text/plain'
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

email_service = EmailService() 
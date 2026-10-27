"""
Email Service — Send emails and manage follow-ups.

Supports:
- Send HTML/plain text emails
- Track open rates
- Manage follow-up sequences
- Integration with outreach messages
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.models import Prospect, Message, MessageStatus, MessageOutcome

logger = logging.getLogger(__name__)


class EmailConfig:
    """Email configuration."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_name: str,
        username: str,
        password: str,
        use_tls: bool = True,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.username = username
        self.password = password
        self.use_tls = use_tls


class EmailService:
    """Email sending and follow-up management."""

    def __init__(self, session: Session, config: Optional[EmailConfig] = None):
        self.session = session
        self.config = config
        self.logger = logger

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        prospect_id: Optional[int] = None,
    ) -> bool:
        """
        Send an email.

        Returns: True if sent successfully
        """
        if not self.config:
            self.logger.warning("Email config not set, skipping send")
            return False

        if not to_email:
            self.logger.error("No email address provided")
            return False

        try:
            self.logger.info(f"📧 Sending email to: {to_email}")

            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.config.sender_name} <{self.config.sender_email}>"
            msg["To"] = to_email

            # Add text and HTML parts
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            # Connect and send
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.use_tls:
                    server.starttls()

                server.login(self.config.username, self.config.password)
                server.sendmail(self.config.sender_email, to_email, msg.as_string())

            self.logger.info(f"✅ Email sent to: {to_email}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to send email: {str(e)}")
            return False

    def send_message_email(
        self,
        message: Message,
        prospect: Prospect,
        subject: str,
    ) -> bool:
        """
        Send outreach message as email.

        Marks message as SENT in database.
        """
        if not prospect.email:
            self.logger.error(f"Prospect {prospect.name} has no email")
            return False

        # Send email
        success = self.send_email(
            to_email=prospect.email,
            subject=subject,
            html_body=f"<p>{message.content.replace(chr(10), '<br>')}</p>",
            text_body=message.content,
            prospect_id=prospect.id,
        )

        if success:
            # Update message status
            message.status = MessageStatus.SENT
            message.sent_at = datetime.now(timezone.utc)
            self.session.add(message)
            self.session.commit()

        return success

    def create_signup_email(
        self,
        prospect: Prospect,
        signup_link: str,
    ) -> tuple[str, str]:
        """
        Create a signup email for artist onboarding.

        Returns: (subject, html_body)
        """
        subject = f"Rejoignez Kucibok — Plateforme pour artistes africains"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Bienvenue sur Kucibok! 🎨</h2>

            <p>Bonjour {prospect.name},</p>

            <p>Nous vous avons découvert et pensons que votre travail serait parfait
            pour notre plateforme Kucibok.</p>

            <h3>Qu'est-ce que Kucibok?</h3>
            <p>Kucibok connecte les artistes africains contemporains avec des collectionneurs,
            curateurs et galeries internationales. Cela signifie:</p>
            <ul>
                <li>✅ Visibilité internationale</li>
                <li>✅ Connexions directes (pas d'intermédiaires)</li>
                <li>✅ Gestion logistique complète</li>
                <li>✅ Support pour les exportations</li>
            </ul>

            <h3>Rejoignez-nous</h3>
            <p>Inscrivez-vous gratuitement et présentez votre portfolio:</p>
            <a href="{signup_link}" style="
                display: inline-block;
                padding: 12px 24px;
                background-color: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            ">Créer mon profil</a>

            <p style="margin-top: 40px; font-size: 12px; color: #666;">
                Vous avez des questions? Répondez à cet email.
            </p>

            <p style="font-size: 12px; color: #666;">
                Kucibok Team<br>
                www.kucibok.com
            </p>
        </body>
        </html>
        """

        return subject, html_body

    def create_follow_up_email(
        self,
        prospect: Prospect,
        days_since_first: int,
    ) -> tuple[str, str]:
        """
        Create a follow-up email.

        Returns: (subject, html_body)
        """
        if days_since_first == 3:
            subject = "Vous aviez raison de nous faire confiance — Kucibok"
            body = f"""
            <p>Bonjour {prospect.name},</p>

            <p>On a vu que vous n'aviez pas encore terminé votre inscription
            sur Kucibok. Pas de souci!</p>

            <p>Juste pour vous rappeler: des galeristes et collectionneurs
            internationaux attendent de découvrir votre travail.</p>

            <p><a href="[SIGNUP_LINK]">Finalisez votre inscription (2 min)</a></p>
            """

        elif days_since_first == 7:
            subject = "Besoin d'aide pour votre inscription? — Kucibok"
            body = f"""
            <p>Bonjour {prospect.name},</p>

            <p>Si l'inscription vous pose problème, on peut vous aider.</p>

            <p>Quelques questions?</p>
            <ul>
                <li>📧 <a href="mailto:support@kucibok.com">support@kucibok.com</a></li>
                <li>💬 Chat en direct sur notre site</li>
            </ul>
            """

        else:
            subject = "Dernière chance — Kucibok"
            body = f"""
            <p>Bonjour {prospect.name},</p>

            <p>C'est notre dernier message. Votre profil vous attend.</p>

            <p><a href="[SIGNUP_LINK]">Rejoignez Kucibok maintenant</a></p>
            """

        return subject, body

    def schedule_follow_ups(
        self,
        prospect: Prospect,
        base_date: datetime,
    ) -> list:
        """
        Schedule follow-up emails at days 3, 7, 14.

        Returns: list of scheduled follow-up tasks
        """
        follow_ups = []

        for days in [3, 7, 14]:
            scheduled_date = base_date + timedelta(days=days)

            # TODO: Create scheduled task in database
            follow_ups.append({
                "prospect_id": prospect.id,
                "days": days,
                "scheduled_date": scheduled_date,
            })

        self.logger.info(f"Scheduled {len(follow_ups)} follow-ups for {prospect.name}")
        return follow_ups

    def send_bulk_emails(
        self,
        prospects: list[Prospect],
        template: str,
    ) -> dict:
        """
        Send emails to multiple prospects.

        Returns:
        {
            "total": N,
            "sent": N,
            "failed": N,
            "errors": [(prospect_name, error), ...]
        }
        """
        self.logger.info(f"📧 Sending emails to {len(prospects)} prospects")

        sent = 0
        failed = 0
        errors = []

        for prospect in prospects:
            try:
                if not prospect.email:
                    failed += 1
                    errors.append((prospect.name, "No email address"))
                    continue

                # Create subject and body based on template
                subject, body = self._create_email_from_template(prospect, template)

                success = self.send_email(
                    to_email=prospect.email,
                    subject=subject,
                    html_body=body,
                    prospect_id=prospect.id,
                )

                if success:
                    sent += 1
                else:
                    failed += 1

            except Exception as e:
                self.logger.error(f"Error sending to {prospect.name}: {str(e)}")
                failed += 1
                errors.append((prospect.name, str(e)))

        self.logger.info(
            f"✅ Sent {sent}/{len(prospects)} emails ({failed} failed)"
        )
        return {
            "total": len(prospects),
            "sent": sent,
            "failed": failed,
            "errors": errors,
        }

    @staticmethod
    def _create_email_from_template(prospect: Prospect, template: str) -> tuple[str, str]:
        """Create email from template."""
        if template == "welcome":
            subject = f"Bienvenue sur Kucibok — {prospect.name}!"
            body = f"<p>Bonjour {prospect.name},</p><p>Bienvenue!</p>"
        elif template == "follow_up_3days":
            subject = f"Vous aviez raison de nous faire confiance"
            body = f"<p>Bonjour {prospect.name},</p><p>Suivi après 3 jours...</p>"
        else:
            subject = "Kucibok"
            body = f"<p>Bonjour {prospect.name},</p><p>Message générique</p>"

        return subject, body

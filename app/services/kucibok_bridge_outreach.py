"""
Kucibok Bridge Outreach Service

Implements the Kucibok Bridge Playbook:
1. Two segments: Curators & Auctioneers
2. Personalized messages (80-100 words, no markdown)
3. Proper tone & persona management
4. Email sequencing (day 0, day 5-7 follow-up)
5. HTML template rendering
"""

import logging
from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.models import Prospect, ProspectType, Message, MessageStatus

logger = logging.getLogger(__name__)


class CuratorSegment(str, Enum):
    """Curator types in the Kucibok Bridge playbook."""
    CURATOR = "CURATOR"  # Independent or institutional curator
    AUCTIONEER = "AUCTIONEER"  # Auction house commissaire-priseur


class MessagePersona(str, Enum):
    """Persona for outreach."""
    MOCTAR = "moctar"  # Always use Moctar Sidibé for direct contact


class KucibokBridgeOutreach:
    """
    Kucibok Bridge Outreach Manager

    Implements the playbook rules:
    - No markdown (plain text messages)
    - 80-100 words max
    - Personalization required
    - Two segments with different angles
    - No "IA", "automated", "platform" mentions
    - One follow-up only if no response
    """

    # Message templates by segment
    CURATOR_VARIANTS = [
        """Bonjour {first_name}, je vous contacte depuis Dakar où je travaille sur le sourcing d'artistes émergents d'Afrique de l'Ouest pour des curateurs internationaux. Chaque profil est vérifié sur le terrain avant d'être présenté. Je vous partage volontiers un premier dossier si le sujet vous intéresse, sans engagement.""",

        """Bonjour {first_name}, votre travail sur {context} rejoint ce que je fais au quotidien à Dakar : sourcer et vérifier des artistes émergents pour des curateurs qui ne peuvent pas se déplacer sur place. Je peux vous envoyer un dossier complet sur un premier profil si vous voulez voir le format.""",

        """Bonjour {first_name}, je m'appelle Moctar, basé à Dakar. Je prépare des dossiers de sourcing vérifiés sur des artistes émergents ouest-africains pour des curateurs à l'international. Un appel de 15 minutes vous intéresserait pour voir si ça correspond à vos recherches actuelles ?"""
    ]

    AUCTIONEER_VARIANTS = [
        """Bonjour {first_name}, je travaille à Dakar sur la traçabilité et la vérification d'œuvres d'artistes émergents ouest-africains — provenance, disponibilité, documentation complète. Si vos prochains catalogues incluent une section art contemporain africain, je peux vous transmettre un dossier de consignation type. Bonne journée.""",

        """Bonjour {first_name}, je vous contacte au sujet du marché émergent de l'art contemporain ouest-africain. Je constitue des dossiers de provenance vérifiée sur des artistes encore peu documentés à l'international — utile si vous envisagez d'élargir vos catalogues sur ce segment. Je peux vous envoyer un exemple."""
    ]

    FOLLOWUP_TEMPLATE = """Bonjour {first_name}, je me permets de faire remonter mon message au cas où il serait passé inaperçu. Bonne journée."""

    def __init__(self, session: Session):
        self.session = session

    def detect_segment(self, prospect: Prospect) -> CuratorSegment:
        """
        Detect which segment a prospect belongs to.

        Curator: Individual curator or exhibition commissioner
        Auctioneer: Auction house, commissaire-priseur
        """
        if prospect.type == ProspectType.CURATOR:
            return CuratorSegment.CURATOR
        elif "auctioneer" in (prospect.description or "").lower() or \
             "commissaire" in (prospect.description or "").lower() or \
             any(name in prospect.name.lower() for name in
                 ["christie", "sotheby", "artcurial", "piasa", "aguttes", "drouot"]):
            return CuratorSegment.AUCTIONEER
        else:
            # Default to curator
            return CuratorSegment.CURATOR

    def generate_message(
        self,
        prospect: Prospect,
        variant_index: int = 0,
    ) -> str:
        """
        Generate personalized outreach message for prospect.

        Rules:
        - No markdown (plain text)
        - 80-100 words max
        - Personalization required
        - Different angle based on segment
        - No automation/AI/platform mentions

        Args:
            prospect: Prospect to contact
            variant_index: Which template variant to use

        Returns:
            Personalized message text
        """
        segment = self.detect_segment(prospect)

        # Get appropriate template list
        if segment == CuratorSegment.CURATOR:
            templates = self.CURATOR_VARIANTS
        else:
            templates = self.AUCTIONEER_VARIANTS

        # Cycle through variants
        template = templates[variant_index % len(templates)]

        # Personalize
        first_name = prospect.name.split()[0] if prospect.name else "there"
        context = prospect.description or prospect.specialty or "contemporary art"

        message = template.format(
            first_name=first_name,
            context=context,
        )

        # Verify constraints
        word_count = len(message.split())
        if word_count > 100:
            logger.warning(f"Message exceeds 100 words ({word_count}): {prospect.name}")

        return message

    def generate_followup_message(self, prospect: Prospect) -> str:
        """Generate follow-up message after 5-7 days of no response."""
        first_name = prospect.name.split()[0] if prospect.name else "there"
        return self.FOLLOWUP_TEMPLATE.format(first_name=first_name)

    def render_html_email(
        self,
        prospect: Prospect,
        artist_name: str,
        artist_city: str,
        artist_country: str,
        artist_medium: str,
        works_available: int,
        dossier_url: str,
        opening_message: str = None,
    ) -> str:
        """
        Render the Kucibok Bridge HTML email template.

        This is sent AFTER the prospect responds positively to initial message.
        """
        html = f"""<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kucibok Bridge — Dossier de Sourcing</title>
</head>
<body style="margin:0; padding:0; background-color:#e9e4d8; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%;">

  <!-- Preheader (hidden) -->
  <div style="display:none; max-height:0; overflow:hidden; opacity:0; font-size:1px; line-height:1px; color:#e9e4d8;">
    Un artiste sourcé et vérifié à Dakar — dossier complet à l'intérieur.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#e9e4d8;">
    <tr>
      <td align="center" style="padding: 32px 16px;">

        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px; max-width:600px; background-color:#f3ede1;">

          <!-- HEADER -->
          <tr>
            <td style="background-color:#0c0c0b; padding: 28px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" style="font-family: Arial, Helvetica, sans-serif;">
                    <span style="display:inline-block; width:22px; height:22px; line-height:20px; text-align:center; border:1.5px solid #c9a04f; color:#c9a04f; font-size:12px; font-weight:bold; border-radius:4px; vertical-align:middle;">K</span>
                    <span style="color:#f3ede1; font-size:15px; font-weight:bold; letter-spacing:1.5px; vertical-align:middle; margin-left:8px;">KUCIBOK <span style="color:#c9a04f;">BRIDGE</span></span>
                  </td>
                  <td align="right" style="font-family: Arial, Helvetica, sans-serif; color:#8a8a85; font-size:10px; letter-spacing:1.5px; text-transform:uppercase;">
                    Sourcing &amp; Vetting
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- GOLD RULE -->
          <tr>
            <td style="background-color:#f3ede1; padding:0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="height:3px; background-color:#c9a04f; font-size:0; line-height:0;">&nbsp;</td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- BODY -->
          <tr>
            <td style="background-color:#f3ede1; padding: 40px 40px 8px 40px; font-family: Arial, Helvetica, sans-serif;">

              <p style="margin:0 0 6px 0; color:#b06a3f; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase;">
                Dossier de Sourcing
              </p>

              <h1 style="margin:0 0 4px 0; color:#0c0c0b; font-family: Georgia, 'Times New Roman', serif; font-size:30px; line-height:1.15; font-weight:normal;">
                {artist_name}
              </h1>

              <p style="margin:0 0 24px 0; color:#726c60; font-size:13px;">
                {artist_city}, {artist_country} &nbsp;·&nbsp; {artist_medium} &nbsp;·&nbsp; Identité vérifiée
              </p>

              <p style="margin:0 0 20px 0; color:#333330; font-size:15px; line-height:1.6;">
                Bonjour {prospect.name.split()[0] if prospect.name else 'there'},
              </p>

              <p style="margin:0 0 20px 0; color:#333330; font-size:15px; line-height:1.6;">
                {opening_message or "Voici le dossier complet dont je vous parlais — sourcé et vérifié directement sur le terrain à Dakar. Vous y trouverez le portfolio, la démarche de l'artiste, et les œuvres actuellement disponibles."}
              </p>

              <!-- CTA BUTTON -->
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin: 8px 0 28px 0;">
                <tr>
                  <td align="center" style="background-color:#c9a04f; border-radius:3px;">
                    <a href="{dossier_url}" style="display:inline-block; padding:13px 30px; font-family: Arial, Helvetica, sans-serif; font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#1a1408; text-decoration:none;">
                      Consulter le dossier complet →
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- INFO STRIP -->
          <tr>
            <td style="background-color:#f3ede1; padding: 0 40px 36px 40px; font-family: Arial, Helvetica, sans-serif;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #d8d0bd;">
                <tr>
                  <td style="padding-top:20px;" width="33%">
                    <p style="margin:0; color:#726c60; font-size:10px; letter-spacing:1px; text-transform:uppercase;">Œuvres</p>
                    <p style="margin:2px 0 0 0; color:#0c0c0b; font-size:16px; font-weight:bold;">{works_available} disponibles</p>
                  </td>
                  <td style="padding-top:20px;" width="33%">
                    <p style="margin:0; color:#726c60; font-size:10px; letter-spacing:1px; text-transform:uppercase;">Médium</p>
                    <p style="margin:2px 0 0 0; color:#0c0c0b; font-size:16px; font-weight:bold;">{artist_medium}</p>
                  </td>
                  <td style="padding-top:20px;" width="33%">
                    <p style="margin:0; color:#726c60; font-size:10px; letter-spacing:1px; text-transform:uppercase;">Statut</p>
                    <p style="margin:2px 0 0 0; color:#0f6e56; font-size:16px; font-weight:bold;">Vérifié</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SIGNATURE -->
          <tr>
            <td style="background-color:#ffffff; padding: 28px 40px; font-family: Arial, Helvetica, sans-serif; border-top:1px solid #e5ddc8;">
              <p style="margin:0 0 2px 0; color:#0c0c0b; font-size:14px; font-weight:bold;">
                Moctar Sidibé
              </p>
              <p style="margin:0; color:#726c60; font-size:12px;">
                Kucibok Bridge — Sourcing &amp; Vetting, Dakar
              </p>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background-color:#0c0c0b; padding: 26px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="font-family: Arial, Helvetica, sans-serif; color:#726c60; font-size:11px; line-height:1.7;">
                    KUCIBOK BRIDGE — Infrastructure professionnelle pour l'art africain<br>
                    contact@kucibok.com &nbsp;·&nbsp; +221 76 275 09 18 &nbsp;·&nbsp; kucibok.com
                  </td>
                </tr>
                <tr>
                  <td style="padding-top:14px; font-family: Arial, Helvetica, sans-serif; color:#4a4740; font-size:10px; line-height:1.6;">
                    Vous recevez cet email suite à un échange avec notre équipe.
                    <a href="#" style="color:#8a8a85; text-decoration:underline;">Se désinscrire</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

        return html

    def schedule_followup(
        self,
        prospect: Prospect,
        days_delay: int = 5,
    ) -> Optional[datetime]:
        """
        Schedule follow-up message for prospect.

        Playbook rule: One follow-up only after 5-7 days if no response.

        Args:
            prospect: Prospect to follow up with
            days_delay: Days to wait before follow-up (5-7 days)

        Returns:
            Scheduled datetime for follow-up
        """
        if not prospect.email:
            return None

        # Check if already has a sent message
        existing_message = self.session.exec(
            select(Message).where(Message.prospect_id == prospect.id)
        ).first()

        if not existing_message:
            return None

        # Schedule follow-up
        followup_date = datetime.now(timezone.utc) + timedelta(days=days_delay)

        return followup_date

    def validate_message_rules(self, message: str) -> Dict[str, bool]:
        """
        Validate message against Kucibok Bridge rules.

        Rules:
        - No markdown (no **, ##, -, etc.)
        - 80-100 words max
        - No "Concrètement" at start
        - No "IA", "automatisé", "plateforme"
        """
        errors = {
            "has_markdown": any(marker in message for marker in ["**", "##", "- ", "* ", "__"]),
            "exceeds_word_count": len(message.split()) > 100,
            "has_concrètement": message.strip().startswith("Concrètement"),
            "has_forbidden_words": any(
                word.lower() in message.lower()
                for word in ["ia", "automatisé", "automation", "plateforme", "platform"]
            ),
        }

        return errors

    def log_outreach(
        self,
        prospect: Prospect,
        message: str,
        message_type: str = "initial",
    ) -> Message:
        """
        Log outreach message in database.

        Args:
            prospect: Target prospect
            message: Message text sent
            message_type: "initial" or "followup"

        Returns:
            Created Message record
        """
        msg = Message(
            prospect_id=prospect.id,
            type="KUCIBOK_BRIDGE_PLAYBOOK",
            status=MessageStatus.SENT,
            subject=f"Sourcing & Vetting - {prospect.name}",
            body=message,
            sent_at=datetime.now(timezone.utc),
        )

        self.session.add(msg)
        self.session.commit()

        logger.info(f"✅ Logged {message_type} message for {prospect.name}")

        return msg

"""
Kucibok Bridge Offer Presentation Service

Implements the second playbook stage:
1. After prospect responds positively to initial contact
2. After they've viewed a sourcing dossier
3. When they ask about the platform

Rules:
- Present only what exists (not what's in development)
- Give real numbers, not promises
- Offer simple action (20-min demo or trial access)
- Never upsell before proving value
"""

import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from sqlmodel import Session, select

from app.models import Message, MessageChannel, MessageStatus, Prospect
from app.models.base import require_id
from app.services.outreach import detect_persona

logger = logging.getLogger(__name__)


class OfferPlanType(str, Enum):
    """Kucibok Bridge pricing plans."""

    CURATOR = "CURATOR"  # €21-49/month
    ADVISOR = "ADVISOR"  # €49-99/month
    ENTERPRISE = "ENTERPRISE"  # Custom pricing


class OfferStage(str, Enum):
    """Where in the funnel the prospect is."""

    AFTER_DOSSIER = "AFTER_DOSSIER"  # They liked the dossier
    DIRECT_INQUIRY = "DIRECT_INQUIRY"  # They asked about the platform


class KucibokBridgeOffer:
    """
    Kucibok Bridge Offer Presentation Manager

    Implements second playbook:
    - Present what exists (Catalogue & Shortlist)
    - Mention what's coming (Certification, Logistics)
    - Never overpromise
    - Simple call-to-action (20-min demo)

    Golden Rule: Present real numbers, not promises
    """

    # What's READY to present
    CATALOG_SIZE = 90  # Verified artists
    VERIFIED_REGIONS = ["Senegal", "Mali", "Ivory Coast", "Burkina Faso", "Guinea"]

    # After dossier - confirm interest
    AFTER_DOSSIER_VARIANTS = [
        """Bonjour {first_name}, ravi que le dossier vous ait plu. Pour info, il vient de notre catalogue Kucibok Bridge, qui compte aujourd'hui plus de 90 artistes d'Afrique de l'Ouest, vérifiés et classés par niveau de maturité. Si utile, je peux vous montrer comment ça fonctionne en 20 minutes, sans engagement.""",
        """Bonjour {first_name}, merci pour votre retour. Ce dossier fait partie d'un catalogue plus large qu'on constitue à Dakar, avec un vrai travail de vérification terrain. Curieux de vous montrer ce qu'il y a derrière si ça vous intéresse — un appel rapide suffit.""",
    ]

    # Direct inquiry about platform
    DIRECT_INQUIRY_VARIANTS = [
        """Bonjour {first_name}, Kucibok Bridge est l'outil qu'on construit à Dakar pour sourcer et vérifier des artistes émergents ouest-africains pour des curateurs internationaux. Aujourd'hui le cœur du produit, c'est le catalogue vérifié — le reste (certification, logistique) arrive progressivement. Je peux vous montrer le catalogue en direct si vous voulez."""
    ]

    # Pricing plans
    PLANS: dict[OfferPlanType, dict[str, Any]] = {
        OfferPlanType.CURATOR: {
            "name": "Plan Curateur",
            "price_min": 21,
            "price_max": 49,
            "currency": "€",
            "billing": "month",
            "features": [
                "Accès complet au catalogue",
                "Shortlist personnelle",
                "Vérification terrain documentée",
                "Mise à jour hebdomadaire des nouveaux profils",
            ],
        },
        OfferPlanType.ADVISOR: {
            "name": "Plan Conseiller",
            "price_min": 49,
            "price_max": 99,
            "currency": "€",
            "billing": "month",
            "features": [
                "Deal flow personnalisé",
                "Gestion de portefeuille",
                "Suivi commission",
                "Support prioritaire",
            ],
        },
        OfferPlanType.ENTERPRISE: {
            "name": "Plan Enterprise",
            "price_min": None,
            "price_max": None,
            "currency": "€",
            "billing": "custom",
            "features": [
                "Gouvernance multi-comptes",
                "Intégrations personnalisées",
                "Support dédié",
                "Infrastructure sur mesure",
            ],
        },
    }

    # Common objections & responses
    OBJECTIONS = {
        "small_catalog": {
            "trigger": "C'est encore petit",
            "response": "Le catalogue grandit chaque semaine. Un catalogue vérifié de 90 profils vaut mieux qu'un annuaire de 1000 non vérifiés. Chaque artiste est documenté sur place.",
        },
        "certification": {
            "trigger": "Vous avez une certification",
            "response": "La certification digitale est en construction. Aujourd'hui la vérification repose sur le travail terrain direct : photo, appel, visite avec chaque artiste. C'est plus robuste qu'un badge.",
        },
        "pricing": {
            "trigger": "Quel est le prix",
            "response": "Le Plan Curateur est en €21-49/mois. Je peux détailler selon votre besoin, mais commençons par une démo du catalogue.",
        },
    }

    def __init__(self, session: Session):
        self.session = session

    def detect_stage(
        self,
        prospect: Prospect,
        context: str | None = None,
    ) -> OfferStage:
        """
        Detect which stage of funnel prospect is at.

        Args:
            prospect: The prospect
            context: Optional context about the interaction

        Returns:
            OfferStage (AFTER_DOSSIER or DIRECT_INQUIRY)
        """
        # Check if they've already been sent a dossier
        existing_messages = self.session.exec(
            select(Message).where(Message.prospect_id == prospect.id)
        ).all()

        if existing_messages and context and "dossier" in context.lower():
            return OfferStage.AFTER_DOSSIER
        elif context and "plateforme" in context.lower():
            return OfferStage.DIRECT_INQUIRY
        else:
            # Default to after dossier if they replied positively
            return OfferStage.AFTER_DOSSIER

    def generate_offer_message(
        self,
        prospect: Prospect,
        stage: OfferStage | None = None,
        variant_index: int = 0,
    ) -> str:
        """
        Generate offer presentation message.

        Rules:
        - Present only what's READY
        - Use real numbers (90 artists, verified)
        - Offer simple action (20-min demo)
        - No overpromising

        Args:
            prospect: Target prospect
            stage: Funnel stage (auto-detected if not provided)
            variant_index: Message variant

        Returns:
            Personalized offer message
        """
        if stage is None:
            stage = self.detect_stage(prospect)

        first_name = prospect.name.split()[0] if prospect.name else "there"

        # Select template based on stage
        if stage == OfferStage.AFTER_DOSSIER:
            templates = self.AFTER_DOSSIER_VARIANTS
        else:
            templates = self.DIRECT_INQUIRY_VARIANTS

        template = templates[variant_index % len(templates)]

        message = template.format(
            first_name=first_name,
        )

        # Validate length
        word_count = len(message.split())
        if word_count > 100:
            logger.warning(f"Offer message exceeds 100 words ({word_count})")

        return message

    def get_plan_description(self, plan_type: OfferPlanType) -> dict:
        """
        Get description of a pricing plan.

        Never mention Enterprise pricing in initial emails.
        Only detail it after prospect has understood the value.
        """
        return self.PLANS.get(plan_type, {})

    def format_pricing_for_email(self, plan_type: OfferPlanType) -> str:
        """
        Format pricing information for email presentation.

        Rules:
        - Only show price range
        - No details until prospect asks
        - Never compare plans in cold email
        """
        plan = self.get_plan_description(plan_type)

        if plan_type == OfferPlanType.ENTERPRISE:
            return "Tarif personnalisé selon vos besoins"
        else:
            return f"{plan['price_min']}–{plan['price_max']} {plan['currency']}/{plan['billing']}"

    def handle_objection(
        self,
        objection_type: str,
    ) -> str:
        """
        Handle common objections with honest, confident responses.

        Rules:
        - Never lie or overpromise
        - Be transparent about what's in development
        - Emphasize real value (verified catalog)

        Args:
            objection_type: Type of objection (small_catalog, certification, pricing)

        Returns:
            Response text
        """
        objection = self.OBJECTIONS.get(objection_type)

        if objection:
            return objection["response"]
        else:
            return "Bonne question. Parlez-moi de votre besoin et on trouvera la réponse ensemble."

    def render_offer_email_html(
        self,
        prospect: Prospect,
        offer_stage: OfferStage = OfferStage.AFTER_DOSSIER,
        demo_url: str = "https://kucibok.com/book-demo",
    ) -> str:
        """
        Render the Kucibok Bridge offer presentation HTML email.

        Features:
        - Present catalog size (90 artists)
        - Show what's ready (Catalog & Shortlist)
        - Mention what's coming (Certification, Logistics)
        - Clear CTA (20-min demo or trial)

        Args:
            prospect: Target prospect
            offer_stage: Where they are in funnel
            demo_url: Link to demo booking

        Returns:
            HTML email content
        """
        first_name = prospect.name.split()[0] if prospect.name else "there"

        if offer_stage == OfferStage.AFTER_DOSSIER:
            title = "Un catalogue vérifié de plus de 90 artistes d'Afrique de l'Ouest"
            intro = "Le dossier que vous avez reçu vient de Kucibok Bridge, la plateforme de sourcing qu'on construit à Dakar. Chaque profil est vérifié directement sur le terrain avant d'être présenté à un curateur. Voici ce que ça recouvre aujourd'hui."
        else:
            title = "Kucibok Bridge — Infrastructure pour le sourcing africain"
            intro = "Kucibok Bridge est l'outil qu'on construit à Dakar pour sourcer et vérifier des artistes émergents ouest-africains pour des curateurs internationaux. Voici ce qui existe aujourd'hui et ce qui arrive."

        html = f"""<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kucibok Bridge — Découvrir la plateforme</title>
</head>
<body style="margin:0; padding:0; background-color:#e9e4d8; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%;">

  <div style="display:none; max-height:0; overflow:hidden; opacity:0; font-size:1px; line-height:1px; color:#e9e4d8;">
    Ce que vous avez vu dans le dossier vient d'un catalogue plus large — un aperçu à l'intérieur.
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
            <td style="background-color:#f3ede1;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr><td style="height:3px; background-color:#c9a04f; font-size:0; line-height:0;">&nbsp;</td></tr>
              </table>
            </td>
          </tr>

          <!-- CONTENT -->
          <tr>
            <td style="background-color:#f3ede1; padding: 40px 40px 8px 40px; font-family: Arial, Helvetica, sans-serif;">

              <p style="margin:0 0 6px 0; color:#b06a3f; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase;">
                Derrière le dossier
              </p>

              <h1 style="margin:0 0 16px 0; color:#0c0c0b; font-family: Georgia, 'Times New Roman', serif; font-size:28px; line-height:1.25; font-weight:normal;">
                {title}
              </h1>

              <p style="margin:0 0 20px 0; color:#333330; font-size:15px; line-height:1.6;">
                Bonjour {first_name},
              </p>

              <p style="margin:0 0 24px 0; color:#333330; font-size:15px; line-height:1.6;">
                {intro}
              </p>

            </td>
          </tr>

          <!-- FEATURES -->
          <tr>
            <td style="background-color:#f3ede1; padding: 0 40px 8px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">

                <!-- READY -->
                <tr>
                  <td style="padding-bottom:14px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; border:1px solid #e5ddc8; border-radius:4px;">
                      <tr>
                        <td width="6" style="background-color:#0f6e56; border-radius:4px 0 0 4px; font-size:0; line-height:0;">&nbsp;</td>
                        <td style="padding: 16px 20px; font-family: Arial, Helvetica, sans-serif;">
                          <p style="margin:0 0 3px 0; color:#0f6e56; font-size:10px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">Disponible aujourd'hui</p>
                          <p style="margin:0 0 4px 0; color:#0c0c0b; font-size:15px; font-weight:bold;">Catalogue &amp; Sourcing vérifié</p>
                          <p style="margin:0; color:#726c60; font-size:13px; line-height:1.5;">Chaque artiste est documenté sur place — portfolio, démarche, disponibilité réelle. Pas de profil publié sans vérification.</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

                <tr>
                  <td style="padding-bottom:14px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; border:1px solid #e5ddc8; border-radius:4px;">
                      <tr>
                        <td width="6" style="background-color:#0f6e56; border-radius:4px 0 0 4px; font-size:0; line-height:0;">&nbsp;</td>
                        <td style="padding: 16px 20px; font-family: Arial, Helvetica, sans-serif;">
                          <p style="margin:0 0 3px 0; color:#0f6e56; font-size:10px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">Disponible aujourd'hui</p>
                          <p style="margin:0 0 4px 0; color:#0c0c0b; font-size:15px; font-weight:bold;">Shortlist personnelle</p>
                          <p style="margin:0; color:#726c60; font-size:13px; line-height:1.5;">Suivez les artistes qui vous intéressent et revenez-y quand votre programmation avance.</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

                <!-- COMING SOON -->
                <tr>
                  <td style="padding-bottom:4px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#faf7f0; border:1px dashed #d8c896; border-radius:4px;">
                      <tr>
                        <td width="6" style="background-color:#c9a04f; border-radius:4px 0 0 4px; font-size:0; line-height:0;">&nbsp;</td>
                        <td style="padding: 16px 20px; font-family: Arial, Helvetica, sans-serif;">
                          <p style="margin:0 0 3px 0; color:#b08a2e; font-size:10px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">Bientôt disponible</p>
                          <p style="margin:0; color:#726c60; font-size:13px; line-height:1.5;">Certification digitale, coordination logistique, suivi de budget — en construction, pas encore ouverts.</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td style="background-color:#f3ede1; padding: 28px 40px 40px 40px; font-family: Arial, Helvetica, sans-serif;">
              <p style="margin:0 0 20px 0; color:#333330; font-size:15px; line-height:1.6;">
                Si utile, je peux vous montrer le catalogue en direct — 20 minutes, sans engagement.
              </p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center" style="background-color:#c9a04f; border-radius:3px;">
                    <a href="{demo_url}" style="display:inline-block; padding:13px 30px; font-family: Arial, Helvetica, sans-serif; font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#1a1408; text-decoration:none;">
                      Réserver un appel de 20 minutes →
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SIGNATURE -->
          <tr>
            <td style="background-color:#ffffff; padding: 28px 40px; font-family: Arial, Helvetica, sans-serif; border-top:1px solid #e5ddc8;">
              <p style="margin:0 0 2px 0; color:#0c0c0b; font-size:14px; font-weight:bold;">Moctar Sidibé</p>
              <p style="margin:0; color:#726c60; font-size:12px;">Kucibok Bridge — Sourcing &amp; Vetting, Dakar</p>
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

    def validate_offer_message(self, message: str) -> dict[str, bool]:
        """
        Validate offer message against Kucibok Bridge rules.

        Rules:
        - No overpromising (don't say "in development" features are available)
        - No markdown
        - Under 100 words (unless answering detailed question)
        - No "Concrètement" at start
        """
        errors = {
            "has_markdown": any(marker in message for marker in ["**", "##", "- ", "* "]),
            "exceeds_word_count": len(message.split()) > 100,
            "has_concrètement": message.strip().startswith("Concrètement"),
            "mentions_unavailable_features": any(
                phrase in message.lower()
                for phrase in [
                    "certification disponible",
                    "logistique prête",
                    "budget tracking live",
                ]
            ),
        }

        return errors

    def log_offer_message(
        self,
        prospect: Prospect,
        message: str,
        stage: OfferStage,
    ) -> Message:
        """
        Log offer presentation in database.

        Args:
            prospect: Target prospect
            message: Message sent
            stage: Funnel stage

        Returns:
            Created Message record
        """
        msg = Message(
            prospect_id=require_id(prospect),
            persona=detect_persona(prospect),
            variant_label="KUCIBOK_BRIDGE_OFFER",
            channel=MessageChannel.EMAIL,
            status=MessageStatus.SENT,
            content=f"Subject: Kucibok Bridge — Plateforme de sourcing\n\n{message}",
            sent_at=datetime.now(timezone.utc),
        )

        self.session.add(msg)
        self.session.commit()

        logger.info(f"✅ Logged offer message for {prospect.name} ({stage.value})")

        return msg

"""Bridge playbooks must persist the messages they log."""

from sqlmodel import Session, select

from app.models import Message, MessageStatus, Prospect, ProspectType
from app.services.kucibok_bridge_offer import KucibokBridgeOffer, OfferStage
from app.services.kucibok_bridge_outreach import KucibokBridgeOutreach


def _prospect(session: Session) -> Prospect:
    prospect = Prospect(type=ProspectType.CURATOR, name="Jane Doe", country="FR")
    session.add(prospect)
    session.commit()
    return prospect


def test_log_outreach_persists_message(session: Session):
    prospect = _prospect(session)
    KucibokBridgeOutreach(session).log_outreach(prospect, "Hello there")
    saved = session.exec(select(Message)).one()
    assert saved.status == MessageStatus.SENT
    assert saved.variant_label == "KUCIBOK_BRIDGE_PLAYBOOK"
    assert "Hello there" in saved.content


def test_log_offer_message_persists_message(session: Session):
    prospect = _prospect(session)
    stage = list(OfferStage)[0]
    KucibokBridgeOffer(session).log_offer_message(prospect, "Our offer", stage)
    saved = session.exec(select(Message)).one()
    assert saved.status == MessageStatus.SENT
    assert saved.variant_label == "KUCIBOK_BRIDGE_OFFER"

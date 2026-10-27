"""Cleanup script for generator-made prospects."""

from app.models import (
    Message,
    MessageStatus,
    Prospect,
    ProspectStatus,
    ProspectType,
    Source,
    SourceType,
)
from scripts.cleanup_fake_prospects import (
    delete_prospects,
    find_candidates,
    generator_markers,
)


def _fake(**kw):
    base = dict(
        type=ProspectType.CURATOR,
        name="Marie Dubois",
        country="FR",
        description="Professional curator and exhibition specialist in contemporary art",
    )
    base.update(kw)
    return Prospect(**base)


def test_markers_detect_generated_prospects():
    assert generator_markers(_fake())
    assert generator_markers(_fake(description=None, name="Jean Martin #12"))
    assert generator_markers(_fake(description=None, email="a.b_1a2b3c4d@galerie-paris.fr"))


def test_markers_ignore_real_looking_prospect():
    real = _fake(
        name="Koyo Kouoh",
        description="Curator and director of a museum of contemporary African art",
        email="info@zeitzmocaa.museum",
        website="https://zeitzmocaa.museum",
    )
    assert generator_markers(real) == []


def test_candidates_and_protections(session):
    fake = _fake(email="marie.dubois@artgallery.fr")
    sourced = _fake(name="Has Source", email="s@example.org")
    verified = _fake(name="Verified", email="v@example.org", status=ProspectStatus.VERIFIED_KUCIBOK)
    contacted = _fake(name="Contacted", email="c@example.org")
    kept = _fake(name="Kept", email="me@example.org")
    session.add_all([fake, sourced, verified, contacted, kept])
    session.commit()

    session.add(Source(prospect_id=sourced.id, url="https://example.org", source_type=SourceType.WEBSITE))
    session.add(
        Message(
            prospect_id=contacted.id,
            persona="CURATOR",
            variant_label="v1",
            content="hi",
            status=MessageStatus.SENT,
        )
    )
    session.commit()

    candidates, protected = find_candidates(session, ["me@example.org"])
    assert [p.id for p, _ in candidates] == [fake.id]
    assert {p.id for p, _ in protected} == {verified.id, contacted.id, kept.id}

    delete_prospects(session, [fake.id])
    assert session.get(Prospect, fake.id) is None
    assert session.get(Prospect, sourced.id) is not None

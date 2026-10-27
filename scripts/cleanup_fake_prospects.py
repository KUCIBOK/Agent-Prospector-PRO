"""
Remove prospects that were fabricated by the old generator scripts.

The removed scripts (generate_paris_*.py, recreate_75_prospects.py,
insert_realistic_direct.py, regenerate_realistic.py, insert_paris_direct.py)
created Paris "curators" with invented names, emails and websites.

A prospect is a deletion candidate only when BOTH hold:
  1. it has no Source row (real prospects must be backed by a source URL), and
  2. it matches a generator marker (template description, "#N" in the name,
     generated email/website pattern).

Never touched: VERIFIED_KUCIBOK / ENROLLED prospects, prospects with a
non-DRAFT message (already contacted), and any email passed to --keep-email.

Usage (dry run by default, nothing is written):
    python -m scripts.cleanup_fake_prospects
    python -m scripts.cleanup_fake_prospects --keep-email me@example.com
    python -m scripts.cleanup_fake_prospects --apply

--apply first writes a JSON backup of every row it deletes, then asks you to
type DELETE. Use --yes to skip the prompt (non-interactive runs).
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from sqlmodel import Session, delete, select

from app.db import engine
from app.models import (
    AIAnalysis,
    ArtistContact,
    Message,
    MessageStatus,
    Prospect,
    ProspectStatus,
    Score,
    Signal,
    Source,
)

DESCRIPTION_PATTERNS = [
    re.compile(r"^Professional .*curator.*(exhibition specialist|specializing|in Paris)", re.I),
    re.compile(r"^Independent curator specializing in contemporary and emerging artists$", re.I),
]
NAME_PATTERN = re.compile(r"#\d+\s*$")
EMAIL_PATTERNS = [
    re.compile(r"_[0-9a-f]{6,8}@"),  # uuid suffix added by the generators
    re.compile(r"@galerie-paris\.", re.I),
    re.compile(r"@paris-gallery\.", re.I),
    re.compile(r"^curator[._-]\w+@", re.I),
]
WEBSITE_PATTERNS = [
    re.compile(r"\.paris-gallery\.fr", re.I),
    re.compile(r"-\d{1,3}\.(fr|paris)(/|$)", re.I),
    re.compile(r"://curator-\w+\.paris", re.I),
    re.compile(r"://(www\.)?galerie-\w+\.paris(/|$)", re.I),
]
PROTECTED_STATUSES = {ProspectStatus.VERIFIED_KUCIBOK, ProspectStatus.ENROLLED}


def generator_markers(prospect: Prospect) -> list[str]:
    """Return the reasons a prospect looks generated (empty list = no match)."""
    reasons = []
    if prospect.description and any(p.search(prospect.description) for p in DESCRIPTION_PATTERNS):
        reasons.append("template description")
    if NAME_PATTERN.search(prospect.name or ""):
        reasons.append("name ends with #N")
    if prospect.email and any(p.search(prospect.email) for p in EMAIL_PATTERNS):
        reasons.append("generated email pattern")
    if prospect.website and any(p.search(prospect.website) for p in WEBSITE_PATTERNS):
        reasons.append("generated website pattern")
    return reasons


def find_candidates(session: Session, keep_emails: Iterable[str]):
    """Return (candidates, protected) as lists of (prospect, reasons)."""
    keep = {e.lower() for e in keep_emails}
    with_source = set(session.exec(select(Source.prospect_id).distinct()).all())
    contacted = set(
        session.exec(select(Message.prospect_id).where(Message.status != MessageStatus.DRAFT)).all()
    )

    candidates, protected = [], []
    for prospect in session.exec(select(Prospect)).all():
        reasons = generator_markers(prospect)
        if not reasons or prospect.id in with_source:
            continue
        if prospect.status in PROTECTED_STATUSES:
            protected.append((prospect, reasons + [f"protected: {prospect.status.value}"]))
        elif prospect.id in contacted:
            protected.append((prospect, reasons + ["protected: already contacted"]))
        elif (prospect.email or "").lower() in keep:
            protected.append((prospect, reasons + ["protected: --keep-email"]))
        else:
            candidates.append((prospect, reasons))
    return candidates, protected


def write_backup(session: Session, ids: list[int], directory: Path) -> Path:
    """Dump every row that will be deleted to a JSON file."""
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = directory / f"fake_prospects_backup_{stamp}.json"
    dump = {}
    for model in (Prospect, Signal, Score, Message, AIAnalysis, ArtistContact):
        column = Prospect.id if model is Prospect else model.prospect_id
        rows = session.exec(select(model).where(column.in_(ids))).all()
        dump[model.__tablename__] = [json.loads(r.model_dump_json()) for r in rows]
    path.write_text(json.dumps(dump, indent=2, default=str, ensure_ascii=False))
    return path


def delete_prospects(session: Session, ids: list[int]) -> None:
    """Delete child rows first, then the prospects, in one transaction."""
    for model in (Signal, Score, Message, AIAnalysis, ArtistContact):
        session.exec(delete(model).where(model.prospect_id.in_(ids)))
    session.exec(delete(Prospect).where(Prospect.id.in_(ids)))
    session.commit()


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="actually delete (default: dry run)")
    parser.add_argument("--yes", action="store_true", help="skip the DELETE confirmation prompt")
    parser.add_argument("--keep-email", action="append", default=[], metavar="EMAIL")
    parser.add_argument("--backup-dir", default="backups", type=Path)
    args = parser.parse_args(argv)

    with Session(engine) as session:
        candidates, protected = find_candidates(session, args.keep_email)

        print(f"Database: {engine.url.render_as_string(hide_password=True)}")
        print(f"Candidates to delete: {len(candidates)}")
        print(f"Matched but protected: {len(protected)}")
        for prospect, reasons in candidates[:20]:
            print(f"  - #{prospect.id} {prospect.name} <{prospect.email}> ({', '.join(reasons)})")
        if len(candidates) > 20:
            print(f"  ... and {len(candidates) - 20} more")
        for prospect, reasons in protected:
            print(f"  ! kept #{prospect.id} {prospect.name} <{prospect.email}> ({reasons[-1]})")

        if not candidates:
            return 0
        if not args.apply:
            print("\nDry run: nothing was deleted. Re-run with --apply to delete.")
            return 0

        if not args.yes and input("\nType DELETE to confirm: ").strip() != "DELETE":
            print("Aborted.")
            return 1

        ids = [p.id for p, _ in candidates]
        backup = write_backup(session, ids, args.backup_dir)
        print(f"Backup written: {backup}")
        delete_prospects(session, ids)
        print(f"Deleted {len(ids)} prospects and their dependent rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

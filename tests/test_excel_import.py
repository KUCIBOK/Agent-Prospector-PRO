"""Excel import, including duplicate detection."""

import pandas as pd
from sqlmodel import Session, select

from app.models import Prospect, ProspectType
from app.services.excel_import import ExcelImporter


def _write(path, rows):
    pd.DataFrame(rows).to_excel(path, index=False)


def test_import_skips_duplicates(session: Session, tmp_path):
    session.add(
        Prospect(type=ProspectType.CURATOR, name="Existing", country="FR", email="dup@example.org")
    )
    session.commit()

    path = tmp_path / "prospects.xlsx"
    _write(
        path,
        [
            {"name": "New Person", "type": "CURATOR", "country": "FR", "email": "new@example.org"},
            {"name": "Other Name", "type": "CURATOR", "country": "FR", "email": "dup@example.org"},
        ],
    )

    result = ExcelImporter(session).import_excel(str(path))

    assert result["imported"] == 1
    assert result["duplicates"] == ["Other Name"]
    assert len(session.exec(select(Prospect)).all()) == 2

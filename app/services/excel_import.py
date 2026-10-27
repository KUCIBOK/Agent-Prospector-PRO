"""
Excel Import Service — Load prospects from Excel files.

Supports:
- Bulk import from XLSX
- Email integration
- Message tracking
- Inscription management
- Follow-up workflow
"""

import logging
from datetime import datetime, timezone

import pandas as pd
from sqlmodel import Session

from app.models import (
    Prospect,
    ProspectStatus,
    ProspectType,
    Source,
    SourceType,
)

logger = logging.getLogger(__name__)


class ExcelImporter:
    """Import prospects from Excel files."""

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def validate_row(row: dict) -> tuple[bool, list]:
        """
        Validate an Excel row.

        Required fields: name, type, country
        Optional: email, website, linkedin, instagram, description

        Returns: (is_valid, errors)
        """
        errors = []

        # Check required fields
        if not row.get("name") or str(row["name"]).strip() == "":
            errors.append("Missing: name")

        if not row.get("type") or str(row["type"]).strip() == "":
            errors.append("Missing: type")

        if not row.get("country") or str(row["country"]).strip() == "":
            errors.append("Missing: country")

        # Validate type
        valid_types = ["ARTIST", "ART_ADVISOR", "CURATOR", "GALLERY", "OTHER"]
        if row.get("type") and str(row["type"]).upper() not in valid_types:
            errors.append(f"Invalid type: {row['type']} (must be: {', '.join(valid_types)})")

        return len(errors) == 0, errors

    def import_excel(
        self,
        filepath: str,
        sheet_name: str = 0,
        skip_duplicates: bool = True,
    ) -> dict:
        """
        Import prospects from Excel file.

        Excel columns (case-insensitive):
        - name (required)
        - type (required): ARTIST, ART_ADVISOR, CURATOR, GALLERY, OTHER
        - country (required): Country name or ISO code
        - email (optional)
        - website (optional)
        - linkedin (optional)
        - instagram (optional)
        - description (optional)
        - notes (optional): Internal notes for follow-up

        Returns:
        {
            "total_rows": N,
            "imported": N,
            "skipped": N,
            "errors": [(row_num, error_msg), ...],
            "duplicates": [name1, name2, ...],
            "prospects": [Prospect, ...],
        }
        """
        logger.info(f"📊 Importing Excel file: {filepath}")

        try:
            # Read Excel
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            logger.info(f"📋 Loaded {len(df)} rows from Excel")

        except Exception as e:
            logger.error(f"❌ Failed to read Excel: {e!s}")
            return {
                "total_rows": 0,
                "imported": 0,
                "skipped": 0,
                "errors": [(0, str(e))],
                "duplicates": [],
                "prospects": [],
            }

        # Normalize column names (lowercase, strip whitespace)
        df.columns = [col.strip().lower() for col in df.columns]

        imported = []
        skipped = 0
        errors = []
        duplicates = []

        # Process rows
        for idx, row in df.iterrows():
            row_num = idx + 2  # Excel row numbering starts at 1, plus header

            try:
                # Convert row to dict
                row_dict = {k: v for k, v in row.to_dict().items() if pd.notna(v)}

                # Validate
                is_valid, validation_errors = self.validate_row(row_dict)
                if not is_valid:
                    error_msg = "; ".join(validation_errors)
                    errors.append((row_num, error_msg))
                    skipped += 1
                    continue

                # Check for duplicates
                name = str(row_dict["name"]).strip()
                email = row_dict.get("email")
                website = row_dict.get("website")

                if skip_duplicates:
                    from sqlmodel import select

                    existing = self.session.exec(
                        select(Prospect).where((Prospect.name == name) if name else False)
                        | ((Prospect.email == email) if email and pd.notna(email) else False)
                        | (
                            (Prospect.website == website)
                            if website and pd.notna(website)
                            else False
                        )
                    ).first()

                    if existing:
                        logger.warning(f"Duplicate found: {name}")
                        duplicates.append(name)
                        skipped += 1
                        continue

                # Create prospect
                prospect = Prospect(
                    type=ProspectType[str(row_dict["type"]).upper()],
                    name=name,
                    country=str(row_dict["country"]).strip(),
                    email=row_dict.get("email"),
                    website=row_dict.get("website"),
                    linkedin=row_dict.get("linkedin"),
                    instagram=row_dict.get("instagram"),
                    description=row_dict.get("description"),
                    status=ProspectStatus.IDENTIFIED,
                )

                self.session.add(prospect)
                self.session.commit()
                self.session.refresh(prospect)

                # Add source (Excel import)
                source = Source(
                    prospect_id=prospect.id,
                    url=filepath,
                    source_type=SourceType.OTHER,
                    title="Excel Import",
                    captured_at=datetime.now(timezone.utc),
                )
                self.session.add(source)
                self.session.commit()

                imported.append(prospect)
                logger.info(f"✅ Imported: {name}")

            except Exception as e:
                logger.error(f"Error processing row {row_num}: {e!s}")
                errors.append((row_num, str(e)))
                skipped += 1

        logger.info(
            f"✅ Import complete: {len(imported)} imported, {skipped} skipped, {len(duplicates)} duplicates"
        )

        return {
            "total_rows": len(df),
            "imported": len(imported),
            "skipped": skipped,
            "errors": errors,
            "duplicates": duplicates,
            "prospects": imported,
        }

    def export_prospects_to_excel(
        self,
        prospects: list[Prospect],
        filepath: str,
        include_scores: bool = True,
    ) -> bool:
        """
        Export prospects to Excel file.

        Includes:
        - Basic info (name, type, country, email, etc.)
        - Scores & priority
        - Status
        - Follow-up notes
        """
        try:
            logger.info(f"📤 Exporting {len(prospects)} prospects to Excel")

            rows = []
            for prospect in prospects:
                row = {
                    "ID": prospect.id,
                    "Name": prospect.name,
                    "Type": prospect.type.value,
                    "Country": prospect.country,
                    "Email": prospect.email or "",
                    "Website": prospect.website or "",
                    "LinkedIn": prospect.linkedin or "",
                    "Instagram": prospect.instagram or "",
                    "Status": prospect.status.value,
                    "Score": f"{prospect.score:.1f}" if prospect.score else "",
                    "Priority": prospect.priority.value if prospect.priority else "",
                    "Confidence": prospect.confidence.value,
                    "Description": prospect.description or "",
                    "Created At": prospect.created_at.isoformat(),
                }
                rows.append(row)

            # Create DataFrame & export
            df = pd.DataFrame(rows)
            df.to_excel(filepath, index=False, sheet_name="Prospects")

            logger.info(f"✅ Exported to: {filepath}")
            return True

        except Exception as e:
            logger.error(f"❌ Export failed: {e!s}")
            return False

"""
Create Excel template for prospect import.

Run this to generate a template file.
"""

import pandas as pd
from pathlib import Path


def create_template():
    """Create an Excel template with sample data."""

    # Sample prospects (50 from Paris)
    data = {
        "name": [
            "Marie Dubois",
            "Jean-Pierre Lefebvre",
            "Sophie Bernard",
            "Michel Renault",
            "Amélie Moreau",
            "Pierre Gauthier",
            "Claire Lemaire",
            "David Mercier",
            "Isabelle Leclerc",
            "Thomas Fontaine",
            "Nathalie Dupre",
            "François Rousseau",
            "Viviane Martin",
            "Christian Gillet",
            "Monique Prevost",
            "Andre Thibault",
            "Jacqueline Fournier",
            "Georges Lefevre",
            "Simone Petit",
            "Alain Boucher",
            "Odette Picard",
            "Henri Lamy",
            "Bernadette Lemoine",
            "Edmund Morel",
            "Georgette Girard",
            "Lucien Masson",
            "Mariette Gaston",
            "Victor Lejeune",
            "Pauline Hubert",
            "Rene Garnier",
            "Therese Olivier",
            "Marcel Renard",
            "Yvonne Vernier",
            "Armand Lacroix",
            "Marguerite Barbe",
            "Louis Verdin",
            "Berthe Brun",
            "Etienne Devaux",
            "Camille Arnould",
            "Georges Arnoux",
            "Francine Bachelot",
            "Jules Barbeau",
            "Ginette Barnabe",
            "Oscar Barrat",
            "Hortense Bassot",
            "Albert Bauchet",
            "Lore Beaufort",
            "Claude Beaumont",
            "Marcelle Beaupre",
            "Ernest Becker",
        ],
        "type": [
            "CURATOR",
            "ART_ADVISOR",
            "GALLERY",
            "CURATOR",
            "ART_ADVISOR",
            "GALLERY",
            "CURATOR",
            "ART_ADVISOR",
            "CURATOR",
            "GALLERY",
        ] * 5,  # Repeat pattern for 50 items
        "country": ["France"] * 50,
        "email": [
            f"prospect{i+1}@paris-art.fr" for i in range(50)
        ],
        "website": [
            f"https://gallery-paris-{i+1}.com" if i % 3 == 0 else None
            for i in range(50)
        ],
        "linkedin": [
            f"https://linkedin.com/in/prospect-{i+1}" if i % 2 == 0 else None
            for i in range(50)
        ],
        "instagram": [
            f"@gallery_paris_{i+1}" if i % 4 == 0 else None
            for i in range(50)
        ],
        "description": [
            "Contemporary art specialist in Paris"
            if i % 2 == 0
            else "Emerging African artists curator"
            for i in range(50)
        ],
    }

    df = pd.DataFrame(data)

    # Create output directory
    output_dir = Path("templates")
    output_dir.mkdir(exist_ok=True)

    # Save Excel
    filepath = output_dir / "prospects_import_template.xlsx"
    df.to_excel(filepath, index=False, sheet_name="Prospects")

    print(f"✅ Template created: {filepath}")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")

    return filepath


if __name__ == "__main__":
    create_template()

from pathlib import Path

from app.db.session import SessionLocal
from app.services.ingestion_service import ingest_file


DATA_DIR = Path("data")

def detect_source(filename: str) -> str:
    filename = filename.lower()

    if "1stdibs" in filename:
        return "1stdibs"
    elif "fashionphile" in filename:
        return "fashionphile"
    elif "grailed" in filename:
        return "grailed"
    return "unknown"


def main():
    db = SessionLocal()

    for file in DATA_DIR.glob("*.json"):
        source = detect_source(file.name)

        print(f"Ingesting {file.name} (source={source})...")
        ingest_file(file, db, source)

    db.close()

    print("Ingestion complete.")


if __name__ == "__main__":
    main()
from pathlib import Path

from app.db.session import SessionLocal
from app.services.ingestion_service import ingest_file

DATA_DIR = Path("data")

def detect_source(filename: str)->str:
        filename = filename.lower()
        if "1stdibs" in filename:
                return "1stdibs"
        if "fashionphile" in filename:
                return "fashionphile"
        if "grailed" in filename:
                return "grailed"
        return "unknown" 

def refresh_all_sources():
        db = SessionLocal()
        results = []
        for file in DATA_DIR.glob("*.json"):
                source = detect_source(file.name)
                ingest_file(file, db, source)
                results.append(file.name)
        db.close()
        return results

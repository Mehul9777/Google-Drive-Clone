from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "metadata.db")

class MetaData(BaseModel):
    filename: str
    size: int
    headers: Dict[str, str]
    content_type: str
    upload_time: str = Field(default_factory=lambda: datetime.now().isoformat())

def insert_metadata(meta: MetaData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            filename TEXT PRIMARY KEY,
            size INTEGER,
            headers TEXT,
            content_type TEXT,
            upload_time TEXT
        )
    """)
    cursor.execute("""
        INSERT OR REPLACE INTO metadata (filename, size, headers, content_type, upload_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        meta.filename,
        meta.size,
        json.dumps(meta.headers),
        meta.content_type,
        meta.upload_time
    ))
    conn.commit()
    conn.close()

def delete_metadata(filename: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metadata WHERE filename = ?", (filename,))
    conn.commit()
    conn.close()

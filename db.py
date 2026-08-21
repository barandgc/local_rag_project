import json
import sqlite3
from typing import List, Tuple

DB_PATH = "rag.db"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def clear_documents() -> None:
    conn = get_connection()
    conn.execute("DELETE FROM documents")
    conn.commit()
    conn.close()


def insert_document(source: str, content: str, embedding: List[float]) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO documents (source, content, embedding) VALUES (?, ?, ?)",
        (source, content, json.dumps(embedding)),
    )
    conn.commit()
    conn.close()


def get_all_documents() -> List[Tuple[int, str, str, List[float]]]:
    conn = get_connection()
    rows = conn.execute("SELECT id, source, content, embedding FROM documents").fetchall()
    conn.close()
    return [(row[0], row[1], row[2], json.loads(row[3])) for row in rows]

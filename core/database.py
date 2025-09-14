# core/database.py

import sqlite3
import json

DB_PATH = "data/parser_memory.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Creates the necessary tables if they don't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Signatures table: Stores a unique hash for each document layout
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signature_hash TEXT NOT NULL UNIQUE,
            layout_name TEXT,
            version INTEGER DEFAULT 1
        )
    """)
    
    # Rules table: Stores the extraction rules linked to a signature
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signature_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            json_rules TEXT,
            FOREIGN KEY (signature_id) REFERENCES signatures (id)
        )
    """)
    
    conn.commit()
    conn.close()

def find_rules_by_signature(signature_hash: str) -> dict | None:
    """Finds a set of extraction rules based on a document's signature hash."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.field_name, r.json_rules
        FROM rules r
        JOIN signatures s ON r.signature_id = s.id
        WHERE s.signature_hash = ?
    """, (signature_hash,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return None
    
    # Reconstruct the rules dictionary
    return {row['field_name']: json.loads(row['json_rules']) for row in rows}

def save_signature_and_rules(signature_hash: str, rules: dict):
    """Saves a new signature and its associated extraction rules to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the new signature
        cursor.execute("INSERT INTO signatures (signature_hash, layout_name) VALUES (?, ?)", 
                       (signature_hash, "auto_learned_layout"))
        signature_id = cursor.lastrowid
        
        # Insert each rule linked to this new signature
        for field, rule_details in rules.items():
            cursor.execute("INSERT INTO rules (signature_id, field_name, json_rules) VALUES (?, ?, ?)",
                           (signature_id, field, json.dumps(rule_details)))
        
        conn.commit()
    except sqlite3.IntegrityError:
        # This signature already exists, do nothing.
        # A more advanced system might handle versioning here.
        pass
    finally:
        conn.close()
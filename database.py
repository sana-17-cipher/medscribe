#SQLite setup & queries
import sqlite3
from datetime import datetime

DB_PATH = "medscribe.db"

def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doc_type TEXT NOT NULL,
            transcript TEXT NOT NULL,
            structured_report TEXT NOT NULL,
            status TEXT DEFAULT 'Unknown',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def save_record(patient_name, doc_type, transcript, structured_report, status):
    """Save a new medical record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO records 
        (patient_name, doc_type, transcript, structured_report, status)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_name, doc_type, transcript, structured_report, status))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def get_all_records():
    """Get all records, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, patient_name, doc_type, status, created_at,
               substr(transcript, 1, 100) as preview
        FROM records 
        ORDER BY created_at DESC
    """)
    
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def get_record_by_id(record_id):
    """Get a single full record."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    conn.close()
    return dict(record) if record else None

def search_records(patient_name="", keyword="", doc_type=""):
    """Search records by name, keyword, or doc type."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT id, patient_name, doc_type, status, created_at, substr(transcript,1,100) as preview FROM records WHERE 1=1"
    params = []
    
    if patient_name:
        query += " AND patient_name LIKE ?"
        params.append(f"%{patient_name}%")
    if keyword:
        query += " AND transcript LIKE ?"
        params.append(f"%{keyword}%")
    if doc_type and doc_type != "All":
        query += " AND doc_type = ?"
        params.append(doc_type)
    
    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def delete_record(record_id):
    """Delete a record by ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
import sqlite3
import csv
import os

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect('Data/telligence_platform.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_cyber_incidents_table(conn):
    """Create the cyber_incidents table if it doesn't exist"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()

def import_csv_to_db():
    """Import data from cyber_incidents.csv into the database"""
    conn = get_db_connection()
    create_cyber_incidents_table(conn)
    cursor = conn.cursor()
    
    csv_path = 'Data/cyber_incidents.csv'
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute("""
                INSERT OR REPLACE INTO cyber_incidents 
                (incident_id, timestamp, severity, category, status, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row['incident_id'],
                row['timestamp'],
                row['severity'],
                row['category'],
                row['status'],
                row['description']
            ))
    
    conn.commit()
    conn.close()
    print(f"Data imported successfully from {csv_path}")

def get_all_cyber_incidents(conn):
    """Retrieve all cyber incidents from the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents")
    incidents = cursor.fetchall()
    return incidents

def get_incidents_by_severity(conn, severity):
    """Get incidents filtered by severity"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE severity = ?", (severity,))
    return cursor.fetchall()

def get_incidents_by_status(conn, status):
    """Get incidents filtered by status"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE status = ?", (status,))
    return cursor.fetchall()

def get_incidents_by_category(conn, category):
    """Get incidents filtered by category"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE category = ?", (category,))
    return cursor.fetchall()

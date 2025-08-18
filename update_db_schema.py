import sqlite3
import uuid

def update_database_schema():
    """Update database schema to add teams functionality and meeting_type"""
    try:
        conn = sqlite3.connect('smartcal.db')
        cursor = conn.cursor()
        
        # Check if columns already exist in bookings table
        cursor.execute("PRAGMA table_info(bookings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add jitsi_room column if it doesn't exist
        if 'jitsi_room' not in columns:
            cursor.execute("ALTER TABLE bookings ADD COLUMN jitsi_room TEXT")
            print("Added jitsi_room column to bookings table")
        
        # Add jitsi_link column if it doesn't exist
        if 'jitsi_link' not in columns:
            cursor.execute("ALTER TABLE bookings ADD COLUMN jitsi_link TEXT")
            print("Added jitsi_link column to bookings table")
            
        # Check if meeting_type column exists in agendas table
        cursor.execute("PRAGMA table_info(agendas)")
        agenda_columns = [column[1] for column in cursor.fetchall()]
        
        # Add meeting_type column if it doesn't exist
        if 'meeting_type' not in agenda_columns:
            cursor.execute("ALTER TABLE agendas ADD COLUMN meeting_type TEXT DEFAULT 'virtual'")
            print("Added meeting_type column to agendas table")
        
        # Check if teams table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
        if not cursor.fetchone():
            # Create teams table
            cursor.execute("""
            CREATE TABLE teams (
                team_id TEXT PRIMARY KEY,
                team_name TEXT NOT NULL,
                created_by TEXT NOT NULL,
                meeting_duration INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print("Created teams table")
            
        # Check if team_members table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team_members'")
        if not cursor.fetchone():
            # Create team_members table
            cursor.execute("""
            CREATE TABLE team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT NOT NULL,
                email TEXT NOT NULL,
                is_outsider BOOLEAN NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE CASCADE
            )
            """)
            print("Created team_members table")
            
        # Check if team_availability table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team_availability'")
        if not cursor.fetchone():
            # Create team_availability table
            cursor.execute("""
            CREATE TABLE team_availability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                is_available BOOLEAN NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE CASCADE
            )
            """)
            print("Created team_availability table")
        
        conn.commit()
        print("Database schema updated successfully")
    except Exception as e:
        print(f"Error updating database schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_database_schema()
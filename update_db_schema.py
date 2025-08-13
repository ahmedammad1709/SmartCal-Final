import sqlite3

def update_database_schema():
    """Add Jitsi meeting columns to bookings table"""
    try:
        conn = sqlite3.connect('smartcal.db')
        cursor = conn.cursor()
        
        # Check if columns already exist
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
        
        conn.commit()
        print("Database schema updated successfully")
    except Exception as e:
        print(f"Error updating database schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_database_schema()
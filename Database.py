import sqlite3
import Helpers

# Example implementation for a simple, small, local database

# Creates SQLite database if not existing
def create_database():
    
    config = Helpers.load_config()
    
    connection = sqlite3.connect(config['database']['name']) 
    
    try:
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- internal ID
                device_id TEXT UNIQUE NOT NULL,        -- unique Device-ID
                device_type TEXT NOT NULL              -- type of device
            )
        ''')
        
        # for testing purposes, remove
        cursor.execute('INSERT or IGNORE INTO devices (device_id, device_type) VALUES (?, ?)', ("123test", "test sensor"))

        connection.commit()
    except Exception as e:
        raise e
    finally:
        connection.close()

# Validates given deviceID
def is_valid_device_id(device_id):
    
    config = Helpers.load_config()
    
    connection = sqlite3.connect(config['database']['name']) 
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    result = cursor.fetchone()

    connection.close()
    return result is not None       # true, if deviceID exists in DB

#TODO: die methode wird nicht genutzt, aber finde sie ok drin zu lassen; Aber können sie auch löschen
# adds a new deviceId to the database
#def add_device_id(device_id, device_type):
#    connection = sqlite3.connect('iot_devices.db')
#    cursor = connection.cursor()

#    try:
#        cursor.execute('INSERT INTO devices (device_id, device_type) VALUES (?, ?)', (device_id, device_type))
#        connection.commit()
#    except sqlite3.IntegrityError:
#        print(f"Device ID {device_id} already exists.")

#    connection.close()


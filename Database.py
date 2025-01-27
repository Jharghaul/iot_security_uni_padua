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

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault_keys (
                id INTEGER,
                device_id TEXT,
                vault_key VARBINARY,
                PRIMARY KEY (id)
                FOREIGN KEY (device_id) REFERENCES devices(device_id));
        ''')
        
        
        # TESTING for testing purposes, 
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

# TESTING adds a new deviceId to the database
def add_device_id(device_id, device_type):
    connection = sqlite3.connect('iot_devices.db')
    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO devices (device_id, device_type) VALUES (?, ?)', (device_id, device_type))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"Device ID {device_id} already exists.")

    connection.close()

# Retreives an array of keys that are the Secure Vault connected to the device_id
def get_vault_of(device_id):
    config = Helpers.load_config()
    connection = sqlite3.connect(config['database']['name']) 
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM vault_keys WHERE device_id = ? ORDER BY id ASC', (device_id,))
    keys = []

    # Retreive keys one by one to ensure the correct order
    single_key = cursor.fetchone()
    while(single_key != None):
        keys.append(single_key[2])
        single_key = cursor.fetchone()      

    connection.close()
    return keys

# Save all keys that the new vault is comprised of into the database table vault_keys using their index as id to ensure order when fetching later
def store_vault_of(device_id, new_vault):
    config = Helpers.load_config()
    connection = sqlite3.connect(config['database']['name']) 
    cursor = connection.cursor()

    for i in range(len(new_vault)):
        cursor.execute('INSERT OR REPLACE INTO vault_keys (id, device_id, vault_key) VALUES (?,?,?)', (i, device_id, new_vault[i],))    

    connection.commit()
    connection.close()
    return
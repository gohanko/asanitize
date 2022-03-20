import sqlite3

class MessageDB:
    def __init__(self):
        self.conn = sqlite3.connect('discord_deleted_messages.sqlite3')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS messages ( MSG_ID TEXT PIMARY KEY, CONTENT TEXT);''')

    def insert_row(self, msg_id, content):
        self.conn.execute('''INSERT INTO messages (MSG_ID, CONTENT) VALUES ("{}", "{}");'''.format(msg_id, content))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

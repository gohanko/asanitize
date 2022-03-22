import sqlite3

class MessageDB:
    def __init__(self, database_file):
        self.conn = self.create_server_connection(database_file)
        self.create_database()

    def create_server_connection(self, database_file):
        conn = sqlite3.connect(database_file)
        return conn

    def _execute_queries(self, query):
        self.conn.execute(query)
        self.conn.commit()

    def create_database(self):
        self._execute_queries('''CREATE TABLE IF NOT EXISTS messages (MSG_ID TEXT PIMARY KEY, CONTENT TEXT, CHANNEL_ID TEXT);''')

    def insert_row(self, msg_id, content, channel_id):
        self.conn.execute('''INSERT INTO messages (MSG_ID, CONTENT, CHANNEL_ID) VALUES (?, ?, ?);''', [msg_id, content, channel_id])
        self.conn.commit()

    def __del__(self):
        self.conn.close()

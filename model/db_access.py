import sqlite3
from sqlite3 import Error

class DbAccess:
    def __init__(self, db_file="model/database.db"):
        self.db_file = db_file
        self.conn = self.create_connection()
    
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            return None
    
    def create_tables(self):
        table = {
            "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                question TEXT NOT NULL,
                response TEXT NOT NULL
            );
            """,         
        }
        try:
            c = self.conn.cursor()
            for table_name, create_table in table.items():
                c.execute(create_table)
        except Error as e:
            return e
    
    def create_user(self, username, password, question, response):
        try:
            c = self.conn.cursor()
            
            c.execute("""
                      INSERT INTO users (username, password, question, response)
                      VALUES (?, ?, ?, ?)""", (username, password, question, response))
            self.conn.commit()
            return True, None
        except Error as e:
            return False, e
 
    def valid_login(self, username):
        try:
            c = self.conn.cursor()
            c.execute("""
                    SELECT * FROM users WHERE username = ?
                    """, (username,))   
            result = c.fetchone()
            return result[2] if result else None, None
        except Error as e:
            return False, e    
    def user_rec(self, username):
        try:
            c = self.conn.cursor()
            c.execute("""
                    SELECT * FROM users WHERE username = ?
                    """, (username,))   
            result = c.fetchall()
            return result if result else None, None
        except Error as e:
            return False, e
                
    def user_verify(self):
        vf = self.conn.cursor()
        vf.execute("""
                SELECT EXISTS (SELECT 1 FROM users LIMIT 1)
                """)
        result = vf.fetchone()[0]
        return result == 1
            
    def close_connection(self):
        if self.conn:
            self.conn.close()
        
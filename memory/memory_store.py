import mariadb

class MemoryStore:
    def __init__(self, host="10.1.1.5", port=3307, user="lyra", password="Lyra_PW4321", database="lyra_memory"):
        try:
            self.conn = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("✅ Connected to MariaDB.")
        except mariadb.Error as e:
            print(f"❌ MariaDB connection error: {e}")
            self.conn = None

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                role VARCHAR(10),
                content TEXT
            )
        """)
        self.conn.commit()

    def log_message(self, role, content):
        self.cursor.execute("INSERT INTO chat_log (role, content) VALUES (?, ?)", (role, content))
        self.conn.commit()
    


    def search_messages(self, keyword, role=None, limit=10):
        query = "SELECT role, content, timestamp FROM chat_log WHERE content LIKE %s"
        params = [f"%{keyword}%"]

        if role in ("user", "assistant"):
            query += " AND role = %s"
            params.append(role)

        query += " ORDER BY timestamp DESC LIMIT %s"
        params.append(limit)

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()


        
    def get_recent_history(self, limit=50):
        self.cursor.execute("SELECT role, content FROM chat_log ORDER BY id DESC LIMIT %s", (limit,))
        return self.cursor.fetchall()



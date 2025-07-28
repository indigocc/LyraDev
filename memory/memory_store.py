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
                content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_memory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def log_message(self, role, content):
        if not content.strip():
            print("⚠️ Empty message skipped.")
            return
        self.cursor.execute(
            "INSERT INTO chat_log (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()

    def get_recent_history(self, limit=50):
        self.cursor.execute("SELECT role, content FROM chat_log ORDER BY id DESC LIMIT ?", (limit,))
        return list(reversed(self.cursor.fetchall()))

    def store_long_memory(self, content):
        if not content.strip():
            print("⚠️ Attempted to store empty memory.")
            return
        print(f"🧠 Storing long-term memory: {content}")
        self.cursor.execute("INSERT INTO long_memory (content) VALUES (?)", (content,))
        self.conn.commit()

    def search_long_memory(self, keyword, limit=10):
        query = """
            SELECT content, timestamp FROM long_memory
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        self.cursor.execute(query, (f"%{keyword}%", limit))
        return self.cursor.fetchall()

    def list_all_long_memory(self):
        self.cursor.execute("SELECT id, content, timestamp FROM long_memory ORDER BY id DESC")
        return self.cursor.fetchall()

    def search_chat_log(self, keyword, limit=10):
        query = """
            SELECT role, content FROM chat_log
            WHERE content LIKE ?
            ORDER BY id DESC
            LIMIT ?
        """
        self.cursor.execute(query, (f"%{keyword}%", limit))
        return list(reversed(self.cursor.fetchall()))

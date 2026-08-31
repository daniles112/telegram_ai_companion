import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent



def get_connection():

    conn = sqlite3.connect(BASE_DIR / "bot_database.db")

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn




def init_db():

    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY,
                chat_title TEXT NOT NULL,
                system_prompt TEXT
                );
            ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                username TEXT,
                user_id INTEGER  NOT NULL,
                role VARCHAR(20),
                message_text TEXT NOT NULL,
                token_costs INTEGER DEFAULT 0,
                model TEXT NOT NULL,
                provider VARCHAR(20) NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
                );
            ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS daily_model_status (
                date DATE DEFAULT CURRENT_DATE,
                provider VARCHAR(20) NOT NULL,
                model VARCHAR(30) NOT NULL,
                requests INT DEFAULT 0,
                prompt_tokens INT DEFAULT 0,
                completion_tokens INT DEFAULT 0,
                errors INT DEFAULT 0,
                PRIMARY KEY (date, provider, model)
                );
            ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS image_generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT NOT NULL,
                chat_id BIGINT NOT NULL,
                provider VARCHAR(32) NOT NULL,
                prompt TEXT NOT NULL,
                negative_prompt TEXT,
                model_type VARCHAR(32),
                model_urn TEXT,
                steps INTEGER,
                cfg_scale REAL,
                cost INTEGER DEFAULT 0,
                raw_response JSONB
                );
            ''')


        cur.execute('''
            CREATE TABLE IF NOT EXISTS generated_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation_id INTEGER NOT NULL
                    REFERENCES image_generations(id)
                    ON DELETE CASCADE,
                width INTEGER,
                height INTEGER,
                image_url TEXT,
                preview_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''')

        

        conn.commit()




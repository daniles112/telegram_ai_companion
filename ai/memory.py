import re
from data.db_connect import get_connection


MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_CHARS = 8000




def save_message(chat_id: int, 
                 username: str, 
                 user_id: int,
                 role: str, 
                 message_text: str, 
                 token_costs: int,
                 model: str,
                 provider: str):

    with get_connection() as conn:

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO chat_history (
                chat_id,
                username,
                user_id,
                role,
                message_text,
                token_costs,
                model,
                provider
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (   
                chat_id,
                username,
                user_id,
                role,
                message_text,
                token_costs,
                model,
                provider
            )
        )

    conn.commit()



def clear_history(chat_id: int) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM chat_history WHERE chat_id = ?",
            (chat_id,)
        )
        deleted_count = cur.rowcount

    return deleted_count



def get_history(
    chat_id,
    limit: int = 12,
    max_message_chars: int = MAX_MESSAGE_CHARS,
    max_history_chars: int = MAX_HISTORY_CHARS,
) -> list[dict]:

    with get_connection() as conn:

        cur = conn.cursor()
         
        cur.execute(
            """
            SELECT username, role, message_text
            FROM chat_history
            WHERE chat_id = ?
            ORDER BY message_id DESC
            LIMIT ?
            """,
            (chat_id, limit)
        )

        rows = cur.fetchall()

    history = []
    history_chars = 0

    for username, role, text in rows[::-1]:
        content = f"<username>{username}</username> {text}"
        content = content[:max_message_chars]

        if history_chars + len(content) > max_history_chars:
            break

        history.append(
            {
                "role": role,
                "content": content,
            }
        )
        history_chars += len(content)

    return history


def strip_tags(text: str) -> str:
    """
    Вырезает теги <username>...</username> из текста модели
    перед сохранением в БД
    """
    if not text:
        return text
    # Удаляем теги <username>...</username> в начале или в тексте
    cleaned = re.sub(r'<username>.*?</username>\s*', '', text)
    return cleaned.strip()


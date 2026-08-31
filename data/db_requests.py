from .db_connect import get_connection
from ai.image_gen.client import GenerationResult
import json




def add_chat(chat_id: int, chat_title: str):

    with get_connection() as conn:

        cur = conn.cursor()

        cur.execute(
            """
                INSERT INTO chats (chat_id, chat_title)
                VALUES (?, ?)

                ON CONFLICT(chat_id)

                DO UPDATE SET
                chat_title = excluded.chat_title;
            """, (chat_id, chat_title)
        )

    conn.commit()




def save_generation(
    result: GenerationResult,
    user_id: int,
    chat_id: int,
) -> int:

    with get_connection() as conn:
    
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO image_generations (
                user_id,
                chat_id,
                provider,
                prompt,
                negative_prompt,
                model_type,
                model_urn,
                steps,
                cfg_scale,
                cost,
                raw_response
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
            """,
            (
                user_id,
                chat_id,
                result.provider,
                result.prompt,
                result.negative_prompt,
                result.model_type,
                result.model,
                result.steps,
                result.cfg_scale,
                result.cost,
                json.dumps(result.raw_response),
            ),
        )

        generation_id = cur.lastrowid

    conn.commit()

    return generation_id




def save_generated_image(generation_id: int, result: GenerationResult):

    with get_connection() as conn:
        
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO generated_images (
                generation_id,
                width,
                height,
                image_url,
                preview_url
            )
            VALUES (
                ?, ?, ?, ?, ?
            )
            """,
            (
                generation_id,
                result.width,
                result.height,
                result.image_url,
                result.preview_url
            ),
        )

    conn.commit()





def change_system_prompt(chat_id: int, system_prompt: str):

    with get_connection() as conn:
    
        cur = conn.cursor()
    
        cur.execute(
            """
                UPDATE chats
                SET system_prompt = ?
                WHERE chat_id = ?
            """, (system_prompt, chat_id)
        )

    conn.commit()



def get_system_prompt(chat_id: int):

    with get_connection() as conn:
    
        cur = conn.cursor()
    
        cur.execute(
            """
                SELECT system_prompt from chats
                WHERE chat_id = ?
            """, (chat_id,)
        )

        row = cur.fetchone()

        if row and row[0]:
            return row[0]
        else:
            return "Используется промпт по умолчанию."



def update_daily_status(provider, model, prompt_tokens, answer_tokens):

    with get_connection() as conn:
    
        cur = conn.cursor()
         
        cur.execute(
            """
            INSERT INTO daily_model_status (
                provider,
                model,
                requests,
                prompt_tokens,
                completion_tokens,
                errors)
                VALUES (?, ?, 1, ?, ?, 0)
                ON CONFLICT(date, provider, model)
                DO UPDATE SET
                requests = requests + 1,
                prompt_tokens = prompt_tokens + excluded.prompt_tokens,
                completion_tokens = completion_tokens + excluded.completion_tokens;
            """,
            (provider, model, prompt_tokens, answer_tokens)
        )

    conn.commit()



def update_daily_errors(provider, model):

    with get_connection() as conn:
    
            cur = conn.cursor()
             
            cur.execute(
                """
                INSERT INTO daily_model_status (
                    provider,
                    model,
                    errors)

                VALUES (?, ?, 1)

                ON CONFLICT(date, provider, model)

                DO UPDATE SET

                errors = errors + 1
                """,
                (provider, model)
            )

    conn.commit()
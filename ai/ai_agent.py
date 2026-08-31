from .memory import save_message, get_history, strip_tags
from data.db_requests import update_daily_errors, update_daily_status, get_system_prompt
from ai.config.settings_manager import SettingsManager





async def send_message(provider_manager: object, 
                 history: list[dict], 
                 system_prompt: str) -> str:


    answer = await provider_manager.provider.ask_llm(history, system_prompt)

    return answer
    


async def take_message(provider_manager: object, 
                 username: str, 
                 user_id: int, 
                 user_message: str, 
                 chat_id: int,
                 settings: SettingsManager) -> str:
    """
    Обрабатывает сообщение пользователя:
    - Получает историю с тегами имён
    - Добавляет информацию об имени бота в system prompt
    - Отправляет в LLM
    - Очищает ответ от тегов
    - Сохраняет с именем бота из settings
    
    Args:
        provider_manager: управляющий LLM провайдерами
        username: имя пользователя
        user_id: ID пользователя
        user_message: текст сообщения
        chat_id: ID чата
        settings: объект SettingsManager (создается один раз в main.py)
    """
    
    # Получаем имя бота из переданного settings
    bot_username = settings.get("telegram.bot_trigger_name", "Assistant")

    try:
        history = get_history(chat_id)
        
        history.append({
            "role": "user",
            "content": user_message
        })

        system_prompt = get_system_prompt(chat_id)

        system_prompt = f"Твое имя {bot_username}.\n{system_prompt}"
        
        response = await send_message(provider_manager, history, system_prompt)

        if response is None:
            raise RuntimeError("Провайдер не вернул ответ")

        if response.get("text") is None:
            raise RuntimeError("Провайдер вернул ответ без текста")

    except Exception as e:
        print("Ошибка:", e)

        update_daily_errors(provider_manager.provider.name, 
                            provider_manager.provider.model)

        return None
    
    save_message(chat_id, 
                 username, 
                 user_id, 
                 "user", 
                 user_message, 
                 response["prompt_tokens"], 
                 response["model"],
                 response["provider"],)
    
    # Вырезаем теги из ответа модели перед сохранением
    clean_response_text = strip_tags(response["text"])
    
    save_message(chat_id, 
                 bot_username, 
                 0, 
                 "assistant",
                 clean_response_text, 
                 response["answer_tokens"],
                 response["model"],
                 response["provider"],
                 )

    update_daily_status(response["provider"], 
                        response["model"],
                        response["prompt_tokens"],
                        response["answer_tokens"]
                        )

    return clean_response_text
import aiogram
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from ai.ai_agent import take_message
from ai.memory import clear_history
from ai.config.settings_manager import SettingsManager
from ai.config.models import ModelConfig
from ai.provider_manager import ProviderManager
from ut.bot_utils import get_chat_title, parse_image_params
from data.db_requests import add_chat, change_system_prompt, get_system_prompt, save_generation, save_generated_image
from ai.image_gen.client import CivitaiClient 
from ai.image_gen.client import ImageGenerationError, IncorrectParams



def contains_bot_name(message: Message, bot_name: str) -> bool:
        return (
            message.text is not None
            and bot_name.lower() in message.text.lower()
        )



class TelegramBot:
    def __init__(self, settings: SettingsManager) -> None:
        self.settings = settings
        self._token = self.settings.get("telegram.token")
        self.trigger_name = self.settings.get("telegram.bot_trigger_name")
        self.bot = aiogram.Bot(self._token)
        self.dp = aiogram.Dispatcher()
        self.router = aiogram.Router()
        self.dp.include_router(self.router)
        self.provider_manager = ProviderManager(self.settings)
        self.image_generator = CivitaiClient()
        self._loop = None
        self._stop_lock = asyncio.Lock()
        self._stopped = False
        self._polling_started = False

        self._register_handlers()


    @property
    def loop(self):
        return self._loop



    def _register_handlers(self) -> None:

        @self.router.message(Command("reset"))
        async def reset_handler(message: Message):

            deleted_count = clear_history(message.chat.id)
            await message.reply(
                f"FROM SYSTEM: история этого чата очищена. Удалено сообщений: {deleted_count}."
            )

        @self.router.message(Command("prompt"))
        async def prompt_handler(message: Message):
        
            add_chat(message.chat.id, get_chat_title(message))
        
            text = message.text.removeprefix("/prompt").strip()
        
            if text:
                if len(text) > 2000:
                    await message.reply("FROM SYSTEM: длина sys_prompt не может быть больше 2000 символов.")

                    return
        
                change_system_prompt(
                    message.chat.id,
                    text
                )
        
                await message.reply("FROM SYSTEM: sys_prompt обновлен.")
        
            else:
                await message.reply(f"FROM SYSTEM: Текущий sys_prompt:\n{get_system_prompt(message.chat.id)}")
        
        
        
        # generate_image handler
        @self.router.message(Command("image"))
        async def generate_image_handler(message: Message):
        
            text = message.text.removeprefix("/image").strip()
        
            prompt, params = parse_image_params(text)
        
            status_message = await message.reply("🎨 Рисую...", parse_mode="Markdown")
          
            try:
                gen_result = await self.image_generator.generate_image(prompt, **params)
        
            except ImageGenerationError as e:
                await self.bot.edit_message_text(
                    f"❌ Ошибка генерации: {e}",
                    chat_id=status_message.chat.id,
                    message_id=status_message.message_id,
                )
                return
        
            except IncorrectParams as e:
                await self.bot.edit_message_text(
                    f"❌ Ошибка параметров: {e}",
                    chat_id=status_message.chat.id,
                    message_id=status_message.message_id,

                )
                return
        
            gen_id = save_generation(gen_result, message.from_user.id, message.chat.id)
            save_generated_image(gen_id, gen_result)
        
            await self.bot.delete_message(
                chat_id=status_message.chat.id,
                message_id=status_message.message_id
            )
        
            await self.bot.send_photo(message.chat.id, gen_result.image_url)
        
            
        # main handler
        @self.router.message(lambda message: contains_bot_name(message, self.trigger_name))
        async def send_message_to_client(message):
        
            add_chat(message.chat.id, get_chat_title(message))
        
            await self.bot.send_chat_action(message.chat.id, "typing")

            answer = await take_message(
                self.provider_manager,
                message.from_user.first_name, 
                message.from_user.id, 
                message.text, 
                message.chat.id,
                self.settings)
    
            if answer:
                await message.answer(answer, parse_mode="Markdown")
    
            else:
                await message.reply("...")          

    

    async def run(self, model_info: ModelConfig, on_ready) -> None:
        self._loop = asyncio.get_running_loop()
        
        try:
            self.provider_manager.select(model_info)

            print("Прогрев модели...")

            ping_answer = await self.provider_manager.ping()
            
            if not ping_answer["result"]:
                raise Exception(ping_answer["errors"])
            
            print("Модель готова.")

            on_ready()

            self._polling_started = True
            await self.dp.start_polling(self.bot)
            self._polling_started = False

        finally:
            await self.stop()


    async def stop(self) -> None:
        if self._loop is None:
            return

        async with self._stop_lock:
            if self._stopped:
                return

            self._stopped = True
            if self._polling_started:
                await self.dp.stop_polling()
            await self.image_generator.close()
            await self.provider_manager.close()
            await self.bot.session.close()

            print("Бот остановлен.")


    async def send_message(self, chat_id: int, message: str):
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
        )


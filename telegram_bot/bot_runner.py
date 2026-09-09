from ai.config.settings_manager import SettingsManager
from ai.config.models import ModelConfig
from telegram_bot.bot import TelegramBot
from threading import Lock, Thread
from typing import Any
import asyncio
from enum import Enum, auto


class BotStatus(Enum):
    STOPPED = auto()
    STARTING = auto()
    RUNNING = auto()
    CONNECTING = auto()
    STOPPING = auto()


class BotRunner:
    def __init__(self):
        self._bot_session: TelegramBot | None = None
        self.error = None
        self._thread: Thread | None = None
        self._status = BotStatus.STOPPED
        self._lock = Lock()
        self._restart_config: Any | None = None
        self._restart_settings: SettingsManager | None = None


    @property
    def status(self) -> BotStatus:
        with self._lock:
            return self._status

    @status.setter
    def status(self, status) -> None:
        with self._lock:
            self._status = status
    

    def start(self, model_info: ModelConfig, settings: SettingsManager) -> None:
        self.error = None

        if self._status != BotStatus.STOPPED:
            raise RuntimeError("Бот уже запущен")

        self._status = BotStatus.STARTING

        with self._lock:

            self._thread = Thread(
                target=lambda: asyncio.run(
                    self._run_bot(model_info, settings)
                ),
                daemon=True,
            )
    
            self._thread.start()


    def restart(self, model_info: Any, settings: SettingsManager) -> None:
        if self.status != BotStatus.RUNNING:
            return

        self._restart_config = model_info
        self._restart_settings = settings
    
        self.stop()


    async def _run_bot(self, model_info: ModelConfig, settings: SettingsManager) -> None:
        try:
            self._bot_session = TelegramBot(settings)

            await self._bot_session.run(model_info=model_info, 
                                        on_ready=self._on_bot_ready)

        except Exception as error:
            self.error = error
            print(f"Ошибка работы бота: {error!r}")

        finally:

            self.status = BotStatus.STOPPED

            with self._lock:
                self._bot_session = None
                self._thread = None

                restart_config = self._restart_config
                restart_settings = self._restart_settings

                self._restart_config = None
                self._restart_settings = None

            if restart_settings is not None:
                self.start(
                    restart_config,
                    restart_settings
            )

    def _on_bot_ready(self):
        self._status = BotStatus.RUNNING


    def stop(self) -> None:
        with self._lock:
            bot = self._bot_session
    
        if bot is None:
            return

        self.status = BotStatus.STOPPING

        loop = bot.loop

        if loop is not None:
            try:
                asyncio.run_coroutine_threadsafe(
                    bot.stop(),
                    loop
                )

            except Exception as error:
                print(f"Ошибка при планировании остановки бота: {error!r}")

        else:
            print("Loop отсутствует.")


    def send_message(self, chat_id: str, message: str):

        if self.status != BotStatus.RUNNING:
            raise RuntimeError("Бот не запущен")
        
        with self._lock:
            bot = self._bot_session

        loop = bot.loop

        return asyncio.run_coroutine_threadsafe(
            bot.send_message(chat_id, message),
            loop,
        )

        

        

            





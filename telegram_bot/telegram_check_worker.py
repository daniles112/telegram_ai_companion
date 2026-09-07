from aiogram import Bot
from PySide6.QtCore import QObject, Signal, Slot



class TelegramCheckWorker(QObject):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, token: str):
        super().__init__()
        self.token = token


    @Slot()
    def run(self):
        try:
            import asyncio

            result = asyncio.run(self.check())

            self.finished.emit(result)

        except Exception as error:
            self.error.emit(str(error))


    async def check(self):
        bot = Bot(self.token)

        try:
            return await bot.get_me()

        finally:
            await bot.session.close()
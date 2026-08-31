
from PySide6.QtWidgets import QApplication
from GUI_panel.gui import MainWindow
from telegram_bot.bot_runner import BotRunner
from dotenv import load_dotenv
from data.db_connect import init_db
from ai.config.settings_manager import SettingsManager
from ai.config.models import ModelRegistry
import sys





init_db()

load_dotenv()

def main() -> None:

    app = QApplication(sys.argv)

    settings = SettingsManager()

    model_registry = ModelRegistry(settings)

    window = MainWindow(bot_runner=BotRunner(), 
                        settings=settings,
                        model_registry=model_registry)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()



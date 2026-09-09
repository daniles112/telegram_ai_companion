from PySide6.QtWidgets import QDialog, QHBoxLayout, QStackedWidget, QVBoxLayout

from ai.config.models import ModelRegistry
from ai.config.settings_manager import SettingsManager
from telegram_bot.bot_runner import BotRunner

from GUI_panel.ai_settings_page import AISettingsPage
from GUI_panel.gui_hepler.GUI_styles_helper import *
from GUI_panel.telegram_settings_page import TelegramSettingsPage
from GUI_panel.providers_page import AIProvidersPage
from GUI_panel.system_prompt_page import SystemPromptPage


class SettingsDialog(QDialog):
    def __init__(self, 
                 settings: SettingsManager, 
                 bot_runner: BotRunner, 
                 model_registry: ModelRegistry, 
                 parent=None) -> None:
        super().__init__(parent)
        apply_dialog_style(self)
        self.settings = settings
        self.bot_runner = bot_runner
        self.model_registry = model_registry
        self.setWindowTitle("Настройки")
        self.resize(700, 450)
        self.settings_menu = create_listwidget()
        self.settings_menu.addItems(["Telegram", "LLM-Модели", "Провайдеры (API)", "Системный промпт"])
        self.settings_menu.setSpacing(3)
        self.settings_menu.setFixedWidth(200)
        self.settings_menu.setFixedHeight(400)
        self.settings_pages = QStackedWidget()
        self.telegram_page = TelegramSettingsPage(self.settings, self.bot_runner)
        self.ai_page = AISettingsPage(self.model_registry)
        self.providers_page = AIProvidersPage(self.settings)
        self.system_prompt_page = SystemPromptPage(self.settings)
        self.settings_pages.addWidget(self.telegram_page)
        self.settings_pages.addWidget(self.ai_page)
        self.settings_pages.addWidget(self.providers_page)
        self.settings_pages.addWidget(self.system_prompt_page)
        self.settings_menu.currentRowChanged.connect(self.settings_pages.setCurrentIndex)
        self.settings_menu.setCurrentRow(0)
        self.save_button = create_button("Сохранить", style="secondary")
        self.cancel_button = create_button("Отмена", style="outlined_red")
        self.save_button.setMinimumSize(140, 42)
        self.cancel_button.setMinimumSize(120, 42)
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(self.settings_menu)
        settings_layout.addWidget(self.settings_pages)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        layout = QVBoxLayout()
        layout.addLayout(settings_layout)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.cancel_settings)


    def save_settings(self) -> None:
        telegram = self.telegram_page.get_settings()

        self.settings.set(
            "telegram.token",
            telegram["token"]
        )

        self.settings.set(
            "telegram.bot_trigger_name",
            telegram["bot_trigger_name"]
        )

        providers_config = self.providers_page.get_settings()

        for provider, config in providers_config.items():
            self.settings.set(
                f"ai.providers.{provider}.api_key",
                config.get("api_key", "")
            )
        
            self.settings.set(
                f"ai.providers.{provider}.base_url",
                config.get("base_url", "")
            )

        self.settings.set(
            "telegram.default_prompt",
            self.system_prompt_page.get_settings()
        )

        self.accept()

    def cancel_settings(self) -> None:
        self.reject()
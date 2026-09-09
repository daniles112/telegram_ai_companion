from PySide6.QtCore import QThread, Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QVBoxLayout, QWidget

from ai.config.settings_manager import SettingsManager
from telegram_bot.bot_runner import BotRunner, BotStatus
from telegram_bot.telegram_check_worker import TelegramCheckWorker
from GUI_panel.gui_hepler.GUI_styles_helper import *


class TelegramSettingsPage(QWidget):
    def __init__(self, settings: SettingsManager, bot_runner: BotRunner) -> None:
        super().__init__()
        self.settings = settings
        self.bot_runner = bot_runner
        title = create_title("Telegram")
        description = create_subtitle("Настройка подключения Telegram-бота")
        name_label = create_subtitle("Имя-триггер Telegram-бота")
        self.name_input = create_input()
        token_label = create_subtitle("Bot API Token")
        self.token_input = create_input()
        self.token_input.setPlaceholderText("Введите токен Telegram-бота")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.show_token_button = create_small_button("*", style="secondary")
        self.show_token_button.clicked.connect(self.toggle_token_visibility)
        token_layout = QHBoxLayout()
        token_layout.addWidget(self.token_input)
        token_layout.addWidget(self.show_token_button)
        self.status_label = create_subtitle("Подключение не настроено")
        self.status_light = create_status_light()
        self.check_button = create_button("Проверить подключение", style="secondary")
        self.check_button.clicked.connect(self.check_connection)
        layout = QVBoxLayout()
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_light, alignment=Qt.AlignmentFlag.AlignTop)
        status_layout.addWidget(self.status_label)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addSpacing(10)
        layout.addWidget(token_label)
        layout.addLayout(token_layout)
        layout.addSpacing(15)
        layout.addLayout(status_layout)
        layout.addSpacing(10)
        layout.addWidget(self.check_button)
        layout.addStretch()
        self.setLayout(layout)
        self.load_settings()
        if self.bot_runner.status == BotStatus.RUNNING:
            self.status_label.setText("Бот запущен")
            self.status_light.set_status("success")
        else:
            self.check_connection()

    def toggle_token_visibility(self) -> None:
        if self.token_input.echoMode() == QLineEdit.EchoMode.Password:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Password)

    def check_connection(self) -> None:
        token = self.token_input.text().strip()
        if not token:
            self.status_label.setText("Введите токен.")
            self.status_light.set_status("danger")
            return
        self.check_button.setEnabled(False)
        self.status_label.setText("Проверка подключения...")
        self.status_light.set_status("loading")
        self.thread = QThread()
        self.worker = TelegramCheckWorker(token)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.connection_success)
        self.worker.error.connect(self.connection_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def load_settings(self) -> None:
        self.token_input.setText(self.settings.get("telegram.token", ""))
        self.name_input.setText(self.settings.get("telegram.bot_trigger_name", ""))

    def get_settings(self) -> dict:
        return {"token": self.token_input.text().strip(), "bot_trigger_name": self.name_input.text().strip()}

    def connection_success(self, bot):
        self.check_button.setEnabled(True)
        self.status_light.setStyleSheet("background-color: green; border-radius: 7px;")
        self.status_label.setText(f"Подключение успешно\nБот: {bot.first_name}\nUsername: @{bot.username}")

    def connection_error(self, error: str):
        self.check_button.setEnabled(True)
        self.status_light.setStyleSheet("background-color: red; border-radius: 7px;")
        self.status_label.setText(f"Ошибка подключения:\n{error}")
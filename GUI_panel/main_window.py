from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QVBoxLayout, QWidget

from ai.config.models import ModelRegistry
from ai.config.settings_manager import SettingsManager
from telegram_bot.bot_runner import BotRunner, BotStatus

from GUI_panel.gui_hepler.GUI_styles_helper import *
from GUI_panel.settings_dialog import SettingsDialog
from GUI_panel.chats_dialog import ChatsDialog


class MainWindow(QWidget):
    def __init__(self, bot_runner: BotRunner, settings: SettingsManager, model_registry: ModelRegistry) -> None:
        super().__init__()
        self.resize(420, 260)
        self.bot_runner = bot_runner
        self.chat_dialog = ChatsDialog(self.bot_runner, self)
        self.settings = settings
        self.model_registry = model_registry
        self.model_registry.models_changed.connect(self.update_model_list)
        self.setWindowTitle("AI Bot Manager")
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_status)
        self.animation_dots = 0
        self.animation_text = ""
        self.model_box = create_combobox()
        self.update_model_list()
        self.status_light = create_status_light()
        self.status_label = create_subtitle("")
        self.set_status("stopped")
        self.button_layout = QHBoxLayout()
        self.start_button = create_button("Запустить бота")
        self.stop_button = create_button("Остановить бота", style="danger")
        self.settings_button = create_button("Настройки", style="secondary")
        self.chats_button = create_button("Чаты", style="secondary")
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.stop_button.setEnabled(False)
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_light)
        status_layout.addWidget(self.status_label)
        self.model_box.setToolTip("Модель, которую бот будет использовать для генерации ответов")
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addLayout(status_layout)
        layout.addStretch()
        layout.addWidget(self.model_box)
        layout.addStretch()
        layout.addLayout(self.button_layout)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.chats_button)
        self.setLayout(layout)
        self.start_button.clicked.connect(self.start_bot)
        self.stop_button.clicked.connect(self.stop_bot)
        self.settings_button.clicked.connect(self.open_settings)
        self.chats_button.clicked.connect(self.open_chats)


    def update_model_list(self) -> None:
        self.model_box.clear()
        models = self.model_registry.get_models()
        for model in models:
            self.model_box.addItem(model.name)


    def start_status_animation(self, text: str) -> None:
        self.animation_text = text
        self.animation_dots = 0
        self.animation_timer.start(400)


    def stop_status_animation(self) -> None:
        self.animation_timer.stop()


    def animate_status(self) -> None:
        self.animation_dots = (self.animation_dots + 1) % 4
        dots = "." * self.animation_dots
        self.status_label.setText(f"{self.animation_text}{dots}")


    def start_bot(self) -> None:
        if self.bot_runner.status != BotStatus.STOPPED:
            return
        selected_model = self.model_box.currentText()
        model_info = self.model_registry.get_model_by_name(selected_model)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.model_box.setEnabled(False)
        self.set_status("starting")
        try:
            self.bot_runner.start(model_info, self.settings)
        except RuntimeError as error:
            QMessageBox.warning(self, "Ошибка запуска", error)
            print(f"Ошибка запуска: {error!r}")
            self.set_status("stopped")
            return
        QTimer.singleShot(200, self.check_bot_started)


    def stop_bot(self) -> None:
        self.set_status("stopping")
        self.stop_button.setEnabled(False)
        QTimer.singleShot(0, self.bot_runner.stop)
        QTimer.singleShot(200, self.check_bot_stopped)


    def check_bot_stopped(self) -> None:
        status = self.bot_runner.status

        if status != BotStatus.STOPPED:
            QTimer.singleShot(200, self.check_bot_stopped)
            return
        
        self.set_status("stopped")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.model_box.setEnabled(True)

        return


    def check_bot_started(self) -> None:
        status = self.bot_runner.status

        if status == BotStatus.STOPPED:
            self.set_status("stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.model_box.setEnabled(True)

        if self.bot_runner.error is not None:
            QMessageBox.critical(
                self,
                "Ошибка запуска",
                f"Не удалось запустить бота:\n\n"
                f"{self.bot_runner.error}"
            )
            return
        
        if status != BotStatus.RUNNING:
            QTimer.singleShot(200, self.check_bot_started)
            return
        
        self.set_status("running")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        return


    def set_status(self, status: str) -> None:
        if status == "stopped":
            self.status_light.set_status("inactive")
            self.stop_status_animation()
            self.status_label.setText(f"Бот неактивен")
        elif status == "starting":
            self.status_light.set_status("loading")
            self.start_status_animation("Бот запускается")
        elif status == "running":
            self.status_light.set_status("success")
            selected_model = self.model_box.currentText()
            self.stop_status_animation()
            self.status_label.setText(f"Бот запущен ({selected_model})")
        elif status == "stopping":
            self.status_light.set_status("warning")
            self.start_status_animation("Бот останавливается")


    def open_settings(self) -> None:
        dialog = SettingsDialog(self.settings, self.bot_runner, self.model_registry, self)
        if dialog.exec():
            if self.bot_runner.status == BotStatus.RUNNING:
                selected_model = self.model_box.currentText()
                model_info = self.model_registry.get_model_by_name(selected_model)
                self.set_status("starting")
                QTimer.singleShot(200, self.check_bot_started)
                self.bot_runner.restart(model_info, self.settings)


    def open_chats(self) -> None:
        self.chat_dialog.show()
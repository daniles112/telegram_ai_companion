
from telegram_bot.bot_runner import BotRunner
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from telegram_bot.bot_runner import BotStatus
from ai.config.settings_manager import SettingsManager
from ai.config.models import ModelRegistry, ModelConfig
from telegram_bot.telegram_check_worker import TelegramCheckWorker
from PySide6.QtCore import QThread

from PySide6.QtWidgets import (
    QDialog,
    QListWidget,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QComboBox,
    QPushButton,
    QLineEdit,
    QListWidgetItem
)






class MainWindow(QWidget):
    def __init__(self, 
                 bot_runner: BotRunner, 
                 settings: SettingsManager, 
                 model_registry: ModelRegistry) -> None:
        super().__init__()

        self.resize(420, 260)

        self.bot_runner = bot_runner
        self.settings = settings
        self.model_registry = model_registry

        self.setWindowTitle("AI Bot Manager")

        self.animation_timer = QTimer(self)
        
        self.animation_timer.timeout.connect(self.animate_status)   
        self.animation_dots = 0
        self.animation_text = "" 

        self.model_box = QComboBox()
        self.all_models = [model.name for model in self.model_registry.get_models()]
        self.model_box.addItems(self.all_models)

        self.status_light = QLabel()
        self.status_light.setFixedSize(14, 14)
        self.status_light.setStyleSheet("""
            QLabel {
                background-color: red;
                border-radius: 7px;
            }
        """)
        self.status_label = QLabel("")

        self.set_status("stopped")

        self.button_layout = QHBoxLayout()

        self.start_button = QPushButton("Запустить бота")
        self.stop_button = QPushButton("Остановить бота")
        self.settings_button = QPushButton("⚙ Настройки")

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        self.stop_button.setEnabled(False)

        status_layout = QHBoxLayout()

        status_layout.addWidget(self.status_light)
        status_layout.addWidget(self.status_label)

        self.model_box.setToolTip(
            "Модель, которую бот будет использовать для генерации ответов"
        )   

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addLayout(status_layout)
        layout.addStretch()
        layout.addWidget(self.model_box)
        layout.addStretch()
        layout.addLayout(self.button_layout)
        layout.addWidget(self.settings_button)

        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_bot)
        self.stop_button.clicked.connect(self.stop_bot)
        self.settings_button.clicked.connect(self.open_settings)


    def start_status_animation(self, text: str) -> None:
        self.animation_text = text
        self.animation_dots = 0
        self.animation_timer.start(400)
            
            
    def stop_status_animation(self) -> None:
        self.animation_timer.stop()


    def animate_status(self) -> None:
        self.animation_dots = (self.animation_dots + 1) % 4

        dots = "." * self.animation_dots

        self.status_label.setText(
            f"{self.animation_text}{dots}"
        )


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
            print(f"Ошибка запуска: {error!r}")
            self.set_status("stopped")
            return
   
        QTimer.singleShot(
            200,
            self.check_bot_started
        )
     

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
            self.status_light.setStyleSheet("""
                QLabel {
                    background-color: #e74c3c;
                    border-radius: 7px;
                }
            """)
            self.stop_status_animation()
            self.status_label.setText("Бот остановлен")

        elif status == "starting":
            self.status_light.setStyleSheet("""
                QLabel {
                    background-color: #f39c12;
                    border-radius: 7px;
                }
            """)
            self.start_status_animation("Бот запускается")

        elif status == "running":
            self.status_light.setStyleSheet("""
                QLabel {
                    background-color: #2ecc71;
                    border-radius: 7px;
                }
            """)
            selected_model = self.model_box.currentText()
            self.stop_status_animation()
            self.status_label.setText(f"Бот запущен ({selected_model})")

        elif status == "stopping":
            self.status_light.setStyleSheet("""
                QLabel {
                    background-color: #e74c3c;
                    border-radius: 7px;
                }
            """)
            self.start_status_animation("Бот останавливается")


    def open_settings(self) -> None:
        dialog = SettingsDialog(self.settings, self.bot_runner, self.model_registry, self)

        if dialog.exec():

            if self.bot_runner.status == BotStatus.RUNNING:
                
                selected_model = self.model_box.currentText()
                model_info = self.model_registry.get_model_by_name(selected_model)

                self.set_status("starting")

                QTimer.singleShot(200, self.check_bot_started)

                self.bot_runner.restart(
                    model_info,
                    self.settings
                )






class TelegramSettingsPage(QWidget):

    def __init__(self, settings: SettingsManager, bot_runner: BotRunner) -> None:
        super().__init__()

        self.settings = settings
        self.bot_runner = bot_runner

        title = QLabel("Telegram")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        description = QLabel(
            "Настройка подключения Telegram-бота"
        )

        name_label = QLabel("Имя-триггер Telegram-бота")
        self.name_input = QLineEdit()

        # API token
        token_label = QLabel("Bot API Token")

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText(
            "Введите токен Telegram-бота"
        )

        self.token_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # Кнопка показа токена
        self.show_token_button = QPushButton("👁")
        self.show_token_button.setFixedWidth(40)

        self.show_token_button.clicked.connect(
            self.toggle_token_visibility
        )

        token_layout = QHBoxLayout()
        token_layout.addWidget(self.token_input)
        token_layout.addWidget(self.show_token_button)

        # Статус
        self.status_label = QLabel(
            "Подключение не настроено"
        )

        self.status_light = QLabel()
        self.status_light.setFixedSize(14, 14)
        self.status_light.setStyleSheet("""
            QLabel {
                background-color: gray;
                border-radius: 7px;
                }
        """)

        # Проверка
        self.check_button = QPushButton(
            "Проверить подключение"
        )

        self.check_button.clicked.connect(
            self.check_connection
        )

        # Основной layout
        layout = QVBoxLayout()

        status_layout = QHBoxLayout()
        status_layout.addWidget(
            self.status_light,
            alignment=Qt.AlignmentFlag.AlignTop
        )
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
            self.status_label.setText(
                "Бот запущен"
            )

            self.status_light.setStyleSheet(
                "background-color: green;"
                "border-radius: 7px;"
            )
        else:
            self.check_connection()



    def toggle_token_visibility(self) -> None:
        if self.token_input.echoMode() == QLineEdit.EchoMode.Password:
            self.token_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.token_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )


    def check_connection(self) -> None:
        token = self.token_input.text().strip()

        if not token:
            self.status_label.setText(
            "Введите токен."
            )

            self.status_light.setStyleSheet(
                "background-color: red;"
                "border-radius: 7px;"
            )

            return

        self.check_button.setEnabled(False)
        self.status_label.setText(
            "Проверка подключения..."
        )

        self.status_light.setStyleSheet(
            "background-color: orange;"
            "border-radius: 7px;"
        )

        self.thread = QThread()
        self.worker = TelegramCheckWorker(token)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )
    
        self.worker.finished.connect(
            self.connection_success
        )
    
        self.worker.error.connect(
            self.connection_error
        )
    
        self.worker.finished.connect(
            self.thread.quit
        )
    
        self.worker.error.connect(
            self.thread.quit
        )
    
        self.thread.finished.connect(
            self.worker.deleteLater
        )
    
        self.thread.finished.connect(
            self.thread.deleteLater
        )
    
        self.thread.start()


    def load_settings(self) -> None:
        self.token_input.setText(
            self.settings.get("telegram.token", "")
        )

        self.name_input.setText(
            self.settings.get("telegram.bot_trigger_name", "")
        )

    def get_settings(self) -> dict:
        return {
            "token": self.token_input.text().strip(),
            "bot_trigger_name": self.name_input.text().strip(),
        }


    def connection_success(self, bot):
        self.check_button.setEnabled(True)

        self.status_light.setStyleSheet(
            "background-color: green;"
            "border-radius: 7px;"
        )
        self.status_label.setText(
            f"Подключение успешно\n"
            f"Бот: {bot.first_name}\n"
            f"Username: @{bot.username}"
        )


    def connection_error(self, error: str):
        self.check_button.setEnabled(True)

        self.status_light.setStyleSheet(
                "background-color: red;"
                "border-radius: 7px;"
            )
        self.status_label.setText(
            f"Ошибка подключения:\n{error}"
        )



class SettingsDialog(QDialog):

    def __init__(self, settings: SettingsManager, 
                 bot_runner: BotRunner, 
                 model_registry: ModelRegistry, 
                 parent=None) -> None:
        super().__init__(parent)

        self.settings = settings
        self.bot_runner = bot_runner
        self.model_registry = model_registry

        self.setWindowTitle("Настройки")
        self.resize(700, 450)

        self.settings_menu = QListWidget()
        
        menu_items = [
            "Telegram",
            "AI",
            "Изображения",
            "Интерфейс",
        ]
        self.settings_menu.addItems(menu_items)
        
        # Стилизация меню
        self.settings_menu.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px 10px;
                border-bottom: 1px solid #e8e8e8;
                color: #333333;
                font-size: 13px;
                font-weight: 500;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:selected {
                background-color: #1976d2;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QListWidget::item:focus {
                outline: none;
                border: none;
            }
        """)
        
        # Установка расстояния между элементами
        self.settings_menu.setSpacing(3)
        
        self.settings_menu.setFixedWidth(200)
        self.settings_menu.setFixedHeight(400)

        self.settings_pages = QStackedWidget()
        
        self.telegram_page = TelegramSettingsPage(self.settings, self.bot_runner)

        self.settings_pages.addWidget(
            self.telegram_page
        )

        self.ai_page = AISettingsPage(self.model_registry)

        self.settings_pages.addWidget(self.ai_page)

        self.settings_pages.addWidget(
            QLabel("Настройки изображений")
        )

        self.settings_pages.addWidget(
            QLabel("Настройки интерфейса")
        )

        self.settings_menu.currentRowChanged.connect(
            self.settings_pages.setCurrentIndex
        )

        # Кнопки
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")


        # Верхняя часть окна
        settings_layout = QHBoxLayout()

        settings_layout.addWidget(self.settings_menu)
        settings_layout.addWidget(self.settings_pages)


        # Нижняя часть окна
        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)


        # Главный layout
        layout = QVBoxLayout()

        layout.addLayout(settings_layout)
        layout.addStretch()
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.save_button.clicked.connect(
            self.save_settings
        )      

        self.cancel_button.clicked.connect(
            self.cancel_settings
        )     
        

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

        self.accept()


    def cancel_settings(self) -> None:
        self.reject()




class AISettingsPage(QWidget):

    def __init__(
        self,
        model_registry: ModelRegistry,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.model_registry = model_registry

        # =========================
        # Список моделей
        # =========================

        self.models_list = QListWidget()

        self.models_list.setFixedWidth(220)

        self.load_models()

        self.models_list.currentRowChanged.connect(
            self.show_model_info
        )

        # =========================
        # Информация о модели
        # =========================

        self.name_label = QLabel("Название: —")
        self.provider_label = QLabel("Провайдер: —")
        self.model_id_label = QLabel("ID модели: —")
        self.free_label = QLabel("Бесплатная: —")
        self.builtin_label = QLabel("Встроенная: —")

        # =========================
        # Кнопки
        # =========================

        self.add_button = QPushButton("Добавить модель")
        self.remove_button = QPushButton("Удалить модель")

        self.remove_button.setEnabled(False)

        self.add_button.clicked.connect(
            self.add_model
        )

        self.remove_button.clicked.connect(
            self.remove_model
        )

        # =========================
        # Правая часть
        # =========================

        info_layout = QVBoxLayout()

        info_layout.addWidget(
            QLabel("<b>Информация о модели</b>")
        )

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.provider_label)
        info_layout.addWidget(self.model_id_label)
        info_layout.addWidget(self.free_label)
        info_layout.addWidget(self.builtin_label)

        info_layout.addStretch()

        info_layout.addWidget(self.add_button)
        info_layout.addWidget(self.remove_button)

        # =========================
        # Основной layout
        # =========================

        layout = QHBoxLayout()

        layout.addWidget(self.models_list, 1)
        layout.addLayout(info_layout, 2)

        self.setLayout(layout)

        # Выбираем первую модель
        if self.models_list.count() > 0:
            self.models_list.setCurrentRow(0)


    def load_models(self) -> None:
        self.models_list.clear()

        models = self.model_registry.get_models()

        for model in models:
            item = QListWidgetItem(model.name)

            self.models_list.addItem(item)


    def show_model_info(self, index: int) -> None:
        if index < 0:
            self.clear_model_info()
            return

        models = self.model_registry.get_models()

        if index >= len(models):
            self.clear_model_info()
            return

        model = models[index]

        self.name_label.setText(
            f"Название: {model.name}"
        )

        self.provider_label.setText(
            f"Провайдер: {model.provider}"
        )

        self.model_id_label.setText(
            f"ID модели: {model.model_id}"
        )

        self.free_label.setText(
            f"Бесплатная: {'Да' if model.free else 'Нет'}"
        )

        self.builtin_label.setText(
            f"Встроенная: {'Да' if model.builtin else 'Нет'}"
        )

        # Встроенные модели нельзя удалить
        self.remove_button.setEnabled(
            not model.builtin
        )


    def clear_model_info(self) -> None:
        self.name_label.setText("Название: —")
        self.provider_label.setText("Провайдер: —")
        self.model_id_label.setText("ID модели: —")
        self.free_label.setText("Бесплатная: —")
        self.builtin_label.setText("Встроенная: —")

        self.remove_button.setEnabled(False)


    def add_model(self) -> None:
        # Пока заглушка.
        # Здесь позже появится AddModelDialog.
        pass


    def remove_model(self) -> None:
        index = self.models_list.currentRow()

        if index < 0:
            return

        models = self.model_registry.get_models()
        model = models[index]

        if model.builtin:
            return

        self.model_registry.remove_custom_model(
            model.name
        )

        self.load_models()

        if self.models_list.count() > 0:
            self.models_list.setCurrentRow(0)
        else:
            self.clear_model_info()


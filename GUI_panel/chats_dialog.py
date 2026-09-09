from PySide6.QtWidgets import QDialog, QMessageBox, QStackedWidget, QVBoxLayout, QComboBox
from PySide6.QtCore import Qt

from telegram_bot.bot_runner import BotStatus
from GUI_panel.gui_hepler.GUI_styles_helper import *

from data.db_requests import get_chats, get_system_prompt, change_system_prompt


class ChatsDialog(QDialog):
    def __init__(self,
                 bot_runner,
                 parent=None):
        super().__init__(parent)

        apply_dialog_style(self)

        self.resize(380, 480)

        self.bot_runner = bot_runner
        self.setWindowTitle("Чаты")

        self.title = create_title("Управление чатами")

        self.search_label = create_subtitle("Поиск чата")
        self.search_input = create_input("Поиск...")

        self.chat_box = create_combobox()

        self.all_chats = get_chats()
        self.load_chats()

        self.prompt_label = create_subtitle("Системный промпт")
        self.prompt_input = create_text_input("Если пусто, используется системный промпт по умолчанию.")
        self.prompt_input.setFixedHeight(150)
        self.save_button = create_button("Сохранить", style="secondary")

        self.message_label = create_subtitle("Отправить сообщение от лица бота")
        self.message_input = create_text_input("Сообщение, которое будет отправлено в чат. Например: Привет!")
        self.message_input.setFixedHeight(72)

        self.send_button = create_button("Отправить", style="primary")

        self.search_input.textChanged.connect(
            self.filter_chats
        )

        self.chat_box.currentIndexChanged.connect(
            self.on_chat_changed
        )

        self.save_button.clicked.connect(
            self.save_system_prompt
        )

        self.send_button.clicked.connect(
            self.send_message
        )

        self.on_chat_changed()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        layout.addWidget(self.title)

        layout.addSpacing(12)

        layout.addWidget(self.search_label)

        search_layout = QVBoxLayout()
        search_layout.setSpacing(3)
        search_layout.setContentsMargins(0, 0, 0, 0)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.chat_box)

        layout.addLayout(search_layout)

        layout.addSpacing(12)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.save_button)

        layout.addSpacing(12)

        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        layout.addStretch()


    def load_chats(self):
        self.chat_box.clear()

        for chat_id, chat_title in self.all_chats:
            self.chat_box.addItem(
                f"{chat_id} ({chat_title})",
                userData=chat_id,
            )


    def filter_chats(self, text: str):
        text = text.lower().strip()

        self.chat_box.clear()

        for chat_id, chat_title in self.all_chats:
            display_text = f"{chat_id} ({chat_title})"

            if text in display_text.lower():
                self.chat_box.addItem(
                    display_text,
                    userData=chat_id,
                )


    def get_selected_chat_id(self):
        return self.chat_box.currentData()


    def on_chat_changed(self):
        chat_id = self.get_selected_chat_id()
        system_prompt = get_system_prompt(chat_id)
        self.prompt_input.setText(system_prompt)


    def save_system_prompt(self):
        chat_id = self.chat_box.currentData()
        prompt = self.prompt_input.toPlainText()

        if len(prompt) > 2000:
            QMessageBox.warning(self,
                                "Предупреждение",
                                "Длина системного промпта не может быть больше 2000 символов")
            return

        change_system_prompt(chat_id, prompt)



    def send_message(self):
        chat_id = self.chat_box.currentData()
        message = self.message_input.toPlainText().strip()

        if chat_id is None:
            QMessageBox.warning(self, 
                                "Предупреждение", 
                                "Выберите чат.")
            return

        if not message:
            QMessageBox.warning(self,
                                "Предупреждение",
                                "Сообщение не может быть пустым.")
            return

        if self.bot_runner.status != BotStatus.RUNNING:
            QMessageBox.warning(self,
                                "Предупреждение",
                                "Для отправки сообщения запустите бота.")
            return

        try:
            self.bot_runner.send_message(chat_id, message)

        except RuntimeError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

        
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon

from telegram_bot.bot_runner import BotStatus
from GUI_panel.gui_hepler.GUI_styles_helper import *

from data.db_requests import get_chats, get_system_prompt, change_system_prompt

from PySide6.QtCore import Signal, QSize


class ChatsDialog(QDialog):

    message_sent = Signal(bool, str)
    
    def __init__(self,
                 bot_runner,
                 parent=None):
        super().__init__(parent)

        apply_dialog_style(self)

        self.resize(380, 480)

        self.message_sent.connect(self.handle_message_result)

        self.bot_runner = bot_runner
        self.setWindowTitle("Чаты")
        self.setWindowIcon(QIcon(str(BASE_DIR / "assets" / "chats.png")))

        self.title = create_title("Управление чатами")

        self.search_label = create_subtitle("Поиск чата")
        self.search_input = create_input("Поиск...")

        self.chat_box = create_combobox()
        self.chat_update_button = create_small_button("", style="primary")
        self.chat_update_button.setIcon(UPDATE_ICON)
        self.chat_update_button.setIconSize(QSize(18, 18))

        self.prompt_label = create_subtitle("Системный промпт")
        self.prompt_input = create_text_input("Если пусто, используется системный промпт по умолчанию.")
        self.prompt_input.setFixedHeight(150)
        self.save_button = create_dynamic_button("Сохранить", "Сохранение", "Сохранено!")

        self.message_label = create_subtitle("Отправить сообщение от лица бота")
        self.message_input = create_text_input("Сообщение, которое будет отправлено в чат. Например: Привет!")
        self.message_input.setFixedHeight(72)

        self.send_button = create_dynamic_button("Отправить", "Отправка", "Отправлено!", style="primary")

        self.all_chats = get_chats()
        self.load_chats()

        self.chat_update_button.clicked.connect(
            self.update_chats
        )

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

        chat_box_layout = QHBoxLayout()
        
        chat_box_layout.addWidget(self.chat_box)
        chat_box_layout.addWidget(self.chat_update_button)

        search_layout.addLayout(chat_box_layout)

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

        self.on_chat_changed()


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


    def on_chat_changed(self, index=None):
        chat_id = self.get_selected_chat_id()
        system_prompt = get_system_prompt(chat_id)
        self.prompt_input.setPlainText(system_prompt)


    def update_chats(self):
        self.all_chats = get_chats()
        self.load_chats()


    def save_system_prompt(self):
        chat_id = self.chat_box.currentData()
        prompt = self.prompt_input.toPlainText()

        if len(prompt) > 2000:
            AppMessageBox.show_warning(
                self,
                "Предупреждение",
                "Длина системного промпта не может быть больше 2000 символов"
            )
            return

        try:
            self.save_button.start_loading()
            change_system_prompt(chat_id, prompt)
            self.save_button.show_result()

        except Exception as e:
            print(e)
            self.save_button.reset()


    def send_message(self):
        chat_id = self.chat_box.currentData()
        message = self.message_input.toPlainText().strip()

        if chat_id is None:
            AppMessageBox.show_warning(self, "Предупреждение", "Выберите чат.")
            return

        if not message:
            AppMessageBox.show_warning(
                self,
                "Предупреждение",
                "Сообщение не может быть пустым."
            )
            return

        if self.bot_runner.status != BotStatus.RUNNING:
            AppMessageBox.show_warning(
                self,
                "Предупреждение",
                "Для отправки сообщения запустите бота."
            )
            return

        try:
            future = self.bot_runner.send_message(chat_id, message)

        except RuntimeError as e:
            AppMessageBox.show_error(self, "Ошибка", str(e))

        self.send_button.start_loading()
        future.add_done_callback(self.on_message_sent)


    def on_message_sent(self, future):
        try:
            future.result()

        except Exception as e:
            self.message_sent.emit(False, str(e))

        else:
            self.message_sent.emit(True, "")


    def handle_message_result(self, success: bool, error: str):
        if success:
            self.send_button.show_result("Отправлено!")
            self.message_input.clear()
    
        else:
            self.send_button.reset()
    
            QMessageBox.critical(
                self,
                "Ошибка отправки",
                error
            )
        
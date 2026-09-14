from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout

from GUI_panel.gui_hepler.GUI_styles_helper import *



class SetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Первоначальная настройка")
        self.setFixedSize(420, 280)

        apply_dialog_style(self)

        title = create_title("Добро пожаловать!")

        description = create_subtitle(
            "Перед началом работы необходимо выполнить "
            "первоначальную настройку приложения."
        )
        description.setWordWrap(True)

        requirements = create_subtitle(
            "В настройках необходимо указать:\n"
            "• Telegram Bot Token\n"
            "• AI-Провайдера и API-ключ"
        )
        requirements.setWordWrap(True)

        self.settings_button = create_button(
            "Открыть настройки",
            style="primary",
        )

        self.later_button = create_button(
            "Позже",
            style="secondary",
        )

        self.settings_button.clicked.connect(self.open_settings)
        self.later_button.clicked.connect(self.reject)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.later_button)
        buttons_layout.addWidget(self.settings_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(description)
        layout.addSpacing(8)
        layout.addWidget(requirements)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        

    def open_settings(self):
        self.accept()
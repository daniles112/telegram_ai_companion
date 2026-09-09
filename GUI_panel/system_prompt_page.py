from PySide6.QtWidgets import QVBoxLayout, QWidget

from ai.config.settings_manager import SettingsManager
from GUI_panel.gui_hepler.GUI_styles_helper import *


class SystemPromptPage(QWidget):
    def __init__(self, settings: SettingsManager, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings

        title = create_title("Системный промпт")
        description = create_subtitle(
            "Промпт по умолчанию для чатов без собственного промпта"
        )
        self.prompt_input = create_text_input()
        self.prompt_input.setMinimumHeight(220)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(self.prompt_input)
        layout.addStretch()
        self.setLayout(layout)

        self.load_settings()

    def load_settings(self) -> None:
        self.prompt_input.setPlainText(
            self.settings.get("telegram.default_prompt", "")
        )

    def get_settings(self) -> str:
        return self.prompt_input.toPlainText().strip()
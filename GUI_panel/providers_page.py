from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QVBoxLayout, QWidget

from GUI_panel.gui_hepler.GUI_styles_helper import *
from ai.config.settings_manager import SettingsManager



class AIProvidersPage(QWidget):
    def __init__(
        self,
        settings: SettingsManager,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.settings = settings

        # =========================
        # Заголовок
        # =========================

        title = create_title("Провайдеры")

        description = create_subtitle(
            "Настройки подключения к AI-провайдерам"
        )

        # =========================
        # Несохранненые настройки
        # =========================

        providers = self.settings.get("ai.providers").keys()

        self.temp_settings = {}

        for provider in providers:
            self.temp_settings[provider] = {
                "api_key": self.settings.get(
                    f"ai.providers.{provider}.api_key",
                    ""
                ),
                "base_url": self.settings.get(
                    f"ai.providers.{provider}.base_url",
                    ""
                ),
            }

        # =========================
        # Выбор провайдера
        # =========================

        provider_label = create_subtitle("Провайдер")

        self.provider_box = create_combobox(providers)

        self.current_provider = self.get_provider_id()

        self.provider_box.currentTextChanged.connect(
            self.switch_provider
        )

        # =========================
        # API Key
        # =========================

        api_key_label = create_subtitle("API Key")

        self.api_key_input = create_input("Введите API ключ")
        self.api_key_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.show_key_button = create_small_button("*", style="secondary")

        self.show_key_button.clicked.connect(
            self.toggle_key_visibility
        )

        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(self.api_key_input)
        api_key_layout.addWidget(self.show_key_button)

        # =========================
        # Base URL
        # =========================

        base_url_label = create_subtitle("Base URL")

        self.base_url_input = create_input(
            "Например: https://api.openai.com/v1"
        )

        # =========================
        # Layout
        # =========================

        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addSpacing(20)

        layout.addWidget(provider_label)
        layout.addWidget(self.provider_box)

        layout.addSpacing(10)

        layout.addWidget(api_key_label)
        layout.addLayout(api_key_layout)

        layout.addSpacing(10)

        layout.addWidget(base_url_label)
        layout.addWidget(self.base_url_input)

        layout.addStretch()

        self.setLayout(layout)

        # Загружаем настройки выбранного провайдера
        self.load_provider_settings()


    def save_current_provider(self, provider) -> None:

        self.temp_settings[provider]["api_key"] = (
            self.api_key_input.text().strip()
        )

        self.temp_settings[provider]["base_url"] = (
            self.base_url_input.text().strip()
        )


    def get_provider_id(self) -> str:
        return self.provider_box.currentText().lower()


    def load_provider_settings(self) -> None:
        provider = self.get_provider_id()

        data = self.temp_settings[provider]

        self.api_key_input.setText(data["api_key"])
        self.base_url_input.setText(data["base_url"])


    def switch_provider(self) -> None:
        self.save_current_provider(self.current_provider)

        self.current_provider = self.get_provider_id()

        self.load_provider_settings()


    def get_settings(self) -> dict:
        self.save_current_provider(self.current_provider)
        
        return self.temp_settings


    def toggle_key_visibility(self) -> None:
        if (
            self.api_key_input.echoMode()
            == QLineEdit.EchoMode.Password
        ):
            self.api_key_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.api_key_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )
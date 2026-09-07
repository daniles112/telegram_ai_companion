from PySide6.QtWidgets import QCheckBox, QDialog, QFormLayout, QHBoxLayout, QMessageBox, QVBoxLayout

from GUI_panel.gui_hepler.GUI_styles_helper import *


class AddModelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        apply_dialog_style(self)
        self.setWindowTitle("Добавить модель")
        self.setFixedWidth(400)
        self.name_input = create_input("Например: Qwen 3.6 27B")
        self.provider_box = create_combobox(["Groq", "OpenAI", "OpenRouter"])
        self.model_id_input = create_input("Например: qwen/qwen3.6-27b")
        self.free_checkbox = QCheckBox("Бесплатная модель")
        form_layout = QFormLayout()
        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Provider:", self.provider_box)
        form_layout.addRow("Model ID:", self.model_id_input)
        buttons_layout = QHBoxLayout()
        cancel_button = create_button("Отмена", style="secondary")
        add_button = create_button("Добавить")
        cancel_button.clicked.connect(self.reject)
        add_button.clicked.connect(self.validate_and_accept)
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(add_button)
        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(self.free_checkbox)
        layout.addLayout(buttons_layout)

    def get_model_data(self) -> dict:
        return {"name": self.name_input.text().strip(), "provider": self.provider_box.currentText(), "model_id": self.model_id_input.text().strip(), "is_free": self.free_checkbox.isChecked()}

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название модели.")
            return
        if not self.model_id_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите Model ID.")
            return
        self.accept()
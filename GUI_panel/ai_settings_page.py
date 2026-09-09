from PySide6.QtWidgets import QDialog, QHBoxLayout, QMessageBox, QVBoxLayout, QWidget

from ai.config.models import ModelRegistry
from GUI_panel.add_model_dialog import AddModelDialog
from GUI_panel.gui_hepler.GUI_styles_helper import *


class AISettingsPage(QWidget):
    def __init__(self, model_registry: ModelRegistry, parent=None) -> None:
        super().__init__(parent)
        self.model_registry = model_registry
        title = create_title("LLM Модели")
        description = create_subtitle(
            "Настройка LLM моделей для ответов бота"
        )

        model_label = create_subtitle("Модель")
        self.models_list = create_combobox()
        self.models_list.currentIndexChanged.connect(self.show_model_info)

        self.model_registry.models_changed.connect(self.load_models)

        self.name_label = create_body("Название: —")
        self.provider_label = create_body("Провайдер: —")
        self.model_id_label = create_body("ID модели: —")
        self.free_label = create_body("Бесплатная: —")
        self.builtin_label = create_body("Встроенная: —")
        self.add_button = create_button("Добавить модель")
        self.remove_button = create_button("Удалить модель", style="danger")
        self.remove_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_model)
        self.remove_button.clicked.connect(self.remove_model)

        model_layout = QVBoxLayout()
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.models_list)

        info_layout = QVBoxLayout()
        info_layout.addWidget(create_subtitle("Информация о модели"))
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.provider_label)
        info_layout.addWidget(self.model_id_label)
        info_layout.addWidget(self.free_label)
        info_layout.addWidget(self.builtin_label)
        info_layout.addStretch()
        info_layout.addWidget(self.add_button)
        info_layout.addWidget(self.remove_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addLayout(model_layout)
        layout.addSpacing(15)
        layout.addLayout(info_layout)
        self.setLayout(layout)

        self.load_models()

    def load_models(self) -> None:
        self.models_list.clear()
        for model in self.model_registry.get_models():
            self.models_list.addItem(model.name)

        if self.models_list.count() > 0:
            self.models_list.setCurrentIndex(0)
        else:
            self.clear_model_info()

    def show_model_info(self, index: int) -> None:
        if index < 0:
            self.clear_model_info()
            return
        models = self.model_registry.get_models()
        if index >= len(models):
            self.clear_model_info()
            return
        model = models[index]
        self.name_label.setText(f"Название: {model.name}")
        self.provider_label.setText(f"Провайдер: {model.provider}")
        self.model_id_label.setText(f"ID модели: {model.model_id}")
        self.free_label.setText(f"Бесплатная: {'Да' if model.free else 'Нет'}")
        self.builtin_label.setText(f"Встроенная: {'Да' if model.builtin else 'Нет'}")
        self.remove_button.setEnabled(not model.builtin)

    def clear_model_info(self) -> None:
        self.name_label.setText("Название: —")
        self.provider_label.setText("Провайдер: —")
        self.model_id_label.setText("ID модели: —")
        self.free_label.setText("Бесплатная: —")
        self.builtin_label.setText("Встроенная: —")
        self.remove_button.setEnabled(False)

    def add_model(self) -> None:
        dialog = AddModelDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        model_data = dialog.get_model_data()
        try:
            self.model_registry.add_custom_model(name=model_data["name"], model_id=model_data["model_id"], provider=model_data["provider"].lower(), free=model_data["is_free"])
            self.load_models()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", f"Модель с названием '{model_data['name']}' уже существует.")

    def remove_model(self) -> None:
        index = self.models_list.currentIndex()
        if index < 0:
            return
        model = self.model_registry.get_models()[index]
        if model.builtin:
            return
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Удаление модели")
        msg_box.setText(f'Вы действительно хотите удалить модель "{model.name}"?')
        yes_button = msg_box.addButton("Да", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.ButtonRole.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec()
        if msg_box.clickedButton() != yes_button:
            return
        self.model_registry.remove_custom_model(model.name)
        if self.models_list.count() > 0:
            self.models_list.setCurrentIndex(0)
        else:
            self.clear_model_info()
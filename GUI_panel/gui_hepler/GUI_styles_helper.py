#!/usr/bin/env python3
"""
GUI Styles Helper - Функции для быстрого применения красивых стилей
Используй эти функции при создании виджетов
"""



from PySide6.QtWidgets import (
    QLabel, QLineEdit, QPushButton, 
    QComboBox, QListWidget, QDialog, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPainter
from typing import Dict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent




SHOW_ICON = QIcon(str(BASE_DIR / "assets" / "show.svg"))
HIDE_ICON = QIcon(str(BASE_DIR / "assets" / "hide.svg"))
UPDATE_ICON = QIcon(str(BASE_DIR / "assets" / "update.svg"))


# ============================================================================
# ЦВЕТОВАЯ СХЕМА (Material Design)
# ============================================================================

class Colors:
    """Централизованное управление цветами"""
    PRIMARY = "#1976d2"
    PRIMARY_DARK = "#1565c0"
    PRIMARY_BLUE = "#93bbe9"
    PRIMARY_LIGHT = "#e3f2fd"
    
    ACCENT = "#ff6f00"
    SUCCESS = "#30c06c"
    SUCCESS_LIGHT = "#daf0e3"
    WARNING = "#f39c12"
    DANGER = "#e74c3c"
    DANGER_LIGHT = "#f8dcd9"
    
    BG_LIGHT = "#f5f5f5"
    BG_WHITE = "#ffffff"
    BORDER = "#e0e0e0"
    
    TEXT_DARK = "#212121"
    TEXT_LIGHT = "#5C5B5B"
    TEXT_HINT = "#bdbdbd"
    INACTIVE = "#575656"


# ============================================================================
# СТИЛИ (Шаблоны QSS)
# ============================================================================

class Styles:
    """Предварительно определенные стили"""
    
    # LABELS
    LABEL_TITLE = f"""
        QLabel {{
            color: {Colors.TEXT_DARK};
            font-size: 18px;
            font-weight: bold;
        }}
    """
    
    LABEL_SUBTITLE = f"""
        QLabel {{
            color: {Colors.TEXT_LIGHT};
            font-size: 13px;
        }}
    """
    
    LABEL_BODY = f"""
        QLabel {{
            color: {Colors.TEXT_DARK};
            font-size: 12px;
        }}
    """
    
    LABEL_MUTED = f"""
        QLabel {{
            color: {Colors.TEXT_HINT};
            font-size: 11px;
        }}
    """
    
    # LINE EDIT
    LINEEDIT = f"""
        QLineEdit {{
            background-color: {Colors.BG_WHITE};
            border: 2px solid {Colors.BORDER};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 12px;
            color: {Colors.TEXT_DARK};
            selection-background-color: {Colors.PRIMARY};
        }}
        QLineEdit:focus {{
            border: 2px solid {Colors.PRIMARY};
        }}
        QLineEdit:hover {{
            border: 2px solid {Colors.PRIMARY};
        }}
        QLineEdit:disabled {{
            background-color: {Colors.BG_LIGHT};
            color: {Colors.TEXT_HINT};
        }}
    """

    TEXTEDIT = f"""
        QTextEdit {{
            background-color: {Colors.BG_WHITE};
            border: 2px solid {Colors.BORDER};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 12px;
            color: {Colors.TEXT_DARK};
            selection-background-color: {Colors.PRIMARY};
        }}
        QTextEdit:focus {{
            border: 2px solid {Colors.PRIMARY};
        }}
        QTextEdit:hover {{
            border: 2px solid {Colors.PRIMARY};
        }}
        QTextEdit:disabled {{
            background-color: {Colors.BG_LIGHT};
            color: {Colors.TEXT_HINT};
        }}
    """
    
    # BUTTONS
    BUTTON_PRIMARY = f"""
        QPushButton {{
            background-color: {Colors.PRIMARY};
            color: white;
            border: 2px solid {Colors.PRIMARY_BLUE};
            border-radius: 4px;
            padding: 6px 16px;
            font-weight: bold;
            font-size: 12px;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: {Colors.PRIMARY_DARK};
        }}
        QPushButton:pressed {{
            background-color: #1565c0;
        }}
        QPushButton:disabled {{
            background-color: {Colors.BORDER};
            color: {Colors.TEXT_HINT};
            border: 2px solid {Colors.BORDER};
        }}
    """

    SMALL_BUTTON_PRIMARY = f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_DARK};
            }}
            QPushButton:pressed {{
                background-color: #1565c0;
            }}
            QPushButton:disabled {{
                background-color: {Colors.BORDER};
                color: {Colors.TEXT_HINT};
            }}
        """
    
    BUTTON_SECONDARY = f"""
        QPushButton {{
            background-color: white;
            color: {Colors.PRIMARY};
            border: 2px solid {Colors.PRIMARY};
            border-radius: 4px;
            padding: 6px 14px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {Colors.PRIMARY_LIGHT};
        }}
        QPushButton:pressed {{
            background-color: {Colors.PRIMARY};
            color: white;
        }}
        QPushButton:disabled {{
            border: 2px solid {Colors.BORDER};
            color: {Colors.TEXT_HINT};
        }}
    """

    SMALL_BUTTON_SECONDARY = f"""
            QPushButton {{
                background-color: white;
                color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 24px;
                max-width: 25px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRIMARY};
                color: white;
            }}
            QPushButton:disabled {{
                border: 2px solid {Colors.BORDER};
                color: {Colors.TEXT_HINT};
            }}
        """
    
    BUTTON_DANGER = f"""
        QPushButton {{
            background-color: {Colors.DANGER};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: #c0392b;
        }}
        QPushButton:pressed {{
            background-color: #a93226;
        }}
        QPushButton:disabled {{
            background-color: {Colors.BORDER};
            color: {Colors.TEXT_HINT};
        }}
    """

    BUTTON_OUTLINED_RED = f"""
        QPushButton {{
            background-color: {Colors.BG_WHITE};
            color: {Colors.DANGER};
            border: 2px solid {Colors.DANGER};
            border-radius: 5px;
            padding: 8px 18px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {Colors.DANGER_LIGHT};
        }}
        QPushButton:pressed {{
            color: {Colors.TEXT_LIGHT};
            background-color: {Colors.DANGER};
        }}
        QPushButton:disabled {{
            background-color: {Colors.BG_LIGHT};
            color: {Colors.TEXT_HINT};
            border: 2px solid {Colors.BORDER};
        }}
    """

    SMALL_BUTTON_DANGER = f"""
            QPushButton {{
                background-color: {Colors.DANGER};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 16px;
                max-width: 30px;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
            QPushButton:pressed {{
                background-color: #a93226;
            }}
            QPushButton:disabled {{
                background-color: {Colors.BORDER};
                color: {Colors.TEXT_HINT};
            }}
        """
    
    BUTTON_SUCCESS = f"""
        QPushButton {{
            background-color: {Colors.SUCCESS};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: #27ae60;
        }}
    """

    SMALL_BUTTON_SUCCESS = f"""
            QPushButton {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 16px;
                max_width: 30px;
            }}
            QPushButton:hover {{
                background-color: #27ae60;
            }}
        """
    
    # COMBOBOX
    COMBOBOX = f"""
        QComboBox {{
            background-color: {Colors.BG_WHITE};
            border: 2px solid {Colors.BORDER};
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 12px;
            color: {Colors.TEXT_DARK};
        }}
        QComboBox::item:hover {{
            background-color: {Colors.PRIMARY_LIGHT};
            color: {Colors.PRIMARY};
        }}
        QComboBox:hover {{
            background-color: {Colors.PRIMARY_LIGHT};
                    color: {Colors.PRIMARY};
        }}
        QComboBox QAbstractItemView {{
            background-color: {Colors.BG_WHITE};
            border: 1px solid {Colors.BORDER};
            selection-background-color: {Colors.PRIMARY};
            selection-color: white;
            padding: 4px 0px;
        }}
        QComboBox:disabled {{
                    background-color: {Colors.BORDER};
                    color: {Colors.TEXT_HINT};
                }}
    """
    
    # LISTWIDGET
    LISTWIDGET = f"""
        QListWidget {{
            background-color: {Colors.BG_WHITE};
            border: 2px solid {Colors.BORDER};
            border-radius: 4px;
            outline: none;
        }}
        QListWidget::item {{
            padding: 10px 12px;
            border-bottom: 1px solid {Colors.BORDER};
            color: {Colors.TEXT_DARK};
            font-size: 12px;
        }}
        QListWidget::item:hover {{
            background-color: {Colors.PRIMARY_LIGHT};
            color: {Colors.PRIMARY};
        }}
        QListWidget::item:selected {{
            background-color: {Colors.PRIMARY};
            color: white;
            border-radius: 3px;
        }}
        QListWidget::item:focus {{
            outline: none;
        }}
    """


# ============================================================================
# СОБСТВЕННЫЙ КЛАСС: StatusLight
# ============================================================================

class StatusLight(QLabel):
    """
    Красивый статус-огонек (собственный класс, не просто QLabel)
    
    Содержит встроенную поддержку изменения статуса и правильное управление стилями
    """
    
    def __init__(self, status: str = "inactive", size: int = 14, parent=None):
        super().__init__(parent)
        
        # Словарь статусов -> цвета
        self.status_colors: Dict[str, str] = {
            "success": Colors.SUCCESS,      # Зеленый
            "danger": Colors.DANGER,        # Красный
            "warning": Colors.WARNING,      # Желтый
            "inactive": Colors.INACTIVE,      # Серый
            "loading": Colors.PRIMARY,      # Синий
        }
        
        self.size = size
        self.status = status
        
        self.setFixedSize(size, size)
        self._apply_style()
    
    def _apply_style(self):
        """Применить стиль для текущего статуса"""
        color = self.status_colors.get(self.status, Colors.BORDER)
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: {self.size // 2}px;
                border: none;
            }}
        """)
    
    def set_status(self, status: str):
        """Изменить статус огонька"""
        if status in self.status_colors:
            self.status = status
            self._apply_style()
        else:
            print(f"⚠️ Неизвестный статус: {status}")
            print(f"Доступные статусы: {list(self.status_colors.keys())}")



class FunctionalPushButton(QPushButton):
    def __init__(
        self,
        text: str,
        loading_text: str = "Сохранение",
        result_text: str = "Сохранено!",
        result_duration: int = 2000,
        parent=None,
    ):
        super().__init__(text, parent)

        self.default_text = text
        self.loading_text = loading_text
        self.result_text = result_text
        self.result_duration = result_duration

        self._dots = 0

        self._loading_timer = QTimer(self)
        self._loading_timer.setInterval(350)
        self._loading_timer.timeout.connect(self._update_loading)

        self._result_timer = QTimer(self)
        self._result_timer.setSingleShot(True)
        self._result_timer.timeout.connect(self._show_result)

        self._result_highlighted = False
        self._style_before_result = ""


    def start_loading(self):
        if self._loading_timer.isActive():
            return

        self.setEnabled(False)

        self._dots = 0
        self._update_loading()

        self._loading_timer.start()


    def _update_loading(self):
        self._dots = (self._dots % 3) + 1

        dots = "." * self._dots
        self.setText(f"{self.loading_text}{dots}")


    def show_result(self, text: str | None = None):
        self._loading_timer.stop()

        if not self._result_highlighted:
            self._style_before_result = self.styleSheet()
            self._result_highlighted = True
            self.setStyleSheet(
                f"{self._style_before_result}\n"
                "QPushButton, QPushButton:disabled {"
                f"background-color: {Colors.SUCCESS_LIGHT};"
                f"color: {Colors.SUCCESS};"
                f"border: 2px solid {Colors.SUCCESS};"
                "}"
            )

        self.setText(text or self.result_text)

        self._result_timer.start(self.result_duration)


    def _show_result(self):
        self.setText(self.default_text)
        self.setEnabled(True)
        self._restore_default_style()


    def _restore_default_style(self):
        if self._result_highlighted:
            self.setStyleSheet(self._style_before_result)
            self._style_before_result = ""
            self._result_highlighted = False


    def reset(self):
        self._loading_timer.stop()
        self._result_timer.stop()

        self.setText(self.default_text)
        self.setEnabled(True)
        self._restore_default_style()
             


class AppMessageBox(QMessageBox):
    _icon_paths = {
        "warning": BASE_DIR / "assets" / "warning.png",
        "error": BASE_DIR / "assets" / "error.png",
    }

    def __init__(self, message_type: str = "warning", parent=None):
        super().__init__(parent)
        icon_path = self._icon_paths.get(message_type)
        if icon_path is not None:
            self.setWindowIcon(QIcon(str(icon_path)))

        if message_type == "warning":
            self.setIcon(QMessageBox.Icon.Warning)
        elif message_type == "error":
            self.setIcon(QMessageBox.Icon.Critical)

    @classmethod
    def show_warning(cls, parent, title: str, text: str):
        message_box = cls("warning", parent)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        return message_box.exec()

    @classmethod
    def show_error(cls, parent, title: str, text: str):
        message_box = cls("error", parent)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        return message_box.exec()


# ============================================================================
# ФУНКЦИИ-ПОМОЩНИКИ
# ============================================================================

def create_title(text: str, parent=None) -> QLabel:
    """Создать красивый заголовок"""
    label = QLabel(text, parent)
    label.setStyleSheet(Styles.LABEL_TITLE)
    return label


def create_subtitle(text: str, parent=None) -> QLabel:
    """Создать красивый подзаголовок"""
    label = QLabel(text, parent)
    label.setStyleSheet(Styles.LABEL_SUBTITLE)
    return label


def create_body(text: str, parent=None) -> QLabel:
    """Создать обычный текст"""
    label = QLabel(text, parent)
    label.setStyleSheet(Styles.LABEL_BODY)
    return label


def create_muted(text: str, parent=None) -> QLabel:
    """Создать приглушенный текст"""
    label = QLabel(text, parent)
    label.setStyleSheet(Styles.LABEL_MUTED)
    return label


def create_input(placeholder: str = "", parent=None) -> QLineEdit:
    """Создать красивое поле ввода"""
    input_field = QLineEdit(parent)
    input_field.setPlaceholderText(placeholder)
    input_field.setStyleSheet(Styles.LINEEDIT)
    return input_field


class WrappedPlaceholderTextEdit(QTextEdit):
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self._wrapped_placeholder = placeholder
        self.setPlaceholderText("")
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.textChanged.connect(self.viewport().update)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.toPlainText() or not self._wrapped_placeholder:
            return

        painter = QPainter(self.viewport())
        painter.setPen(self.palette().placeholderText().color())
        placeholder_rect = self.viewport().rect().adjusted(12, 8, -12, -8)
        painter.drawText(placeholder_rect, Qt.TextWordWrap, self._wrapped_placeholder)


def create_text_input(placeholder: str = "", parent=None) -> QTextEdit:
    """Создать красивое поле ввода"""
    input_field = WrappedPlaceholderTextEdit(placeholder, parent)
    input_field.setStyleSheet(Styles.TEXTEDIT)
    return input_field


def create_button(text: str, style: str = "primary", parent=None) -> QPushButton:
    """
    Создать красивую кнопку
    
    style: "primary", "secondary", "danger", "success"
    """
    button = QPushButton(text, parent)
    
    if style == "primary":
        button.setStyleSheet(Styles.BUTTON_PRIMARY)
    elif style == "secondary":
        button.setStyleSheet(Styles.BUTTON_SECONDARY)
    elif style == "danger":
        button.setStyleSheet(Styles.BUTTON_DANGER)
    elif style == "outlined_red":
        button.setStyleSheet(Styles.BUTTON_OUTLINED_RED)
    elif style == "success":
        button.setStyleSheet(Styles.BUTTON_SUCCESS)
    
    return button


def create_dynamic_button(text: str, 
                          loading_text: str,
                          result_text: str,
                          style: str = "secondary", 
                          parent=None):
    
    button = FunctionalPushButton(text, loading_text, result_text, parent=parent)

    if style == "secondary":
        button.setStyleSheet(Styles.BUTTON_SECONDARY)
    elif style == "primary":
        button.setStyleSheet(Styles.BUTTON_PRIMARY)

    return button


def create_small_button(text: str, style: str = "secondary", parent=None) -> QPushButton:
    """
    Создать маленькую кнопку
    
    style: "primary", "secondary", "danger", "success"
    """
    button = QPushButton(text, parent)
    
    if style == "primary":
        button.setStyleSheet(Styles.SMALL_BUTTON_PRIMARY)
    elif style == "secondary":
        button.setStyleSheet(Styles.SMALL_BUTTON_SECONDARY)
    elif style == "danger":
        button.setStyleSheet(Styles.SMALL_BUTTON_DANGER)
    elif style == "success":
        button.setStyleSheet(Styles.SMALL_BUTTON_SUCCESS)
    
    return button


def create_combobox(items: list = None, parent=None) -> QComboBox:
    """Создать красивый выпадающий список"""
    combo = QComboBox(parent)
    if items:
        combo.addItems(items)
    combo.setStyleSheet(Styles.COMBOBOX)
    return combo


def create_listwidget(parent=None) -> QListWidget:
    """Создать красивый список"""
    list_widget = QListWidget(parent)
    list_widget.setStyleSheet(Styles.LISTWIDGET)
    return list_widget


def create_status_light(status: str = "inactive", size: int = 14, parent=None) -> StatusLight:
    """
    Создать красивый статус-огонек (светодиод)
    
    Args:
        status: "success" (зеленый), "danger" (красный), "warning" (желтый), 
                "inactive" (серый), "loading" (синий)
        size: размер в пикселях (по умолчанию 14)
        parent: родитель виджета
    
    Returns:
        StatusLight - собственный класс с поддержкой изменения статуса
        
    Пример:
        light = create_status_light("success")  # Зеленый огонек
        light.set_status("danger")              # Изменить на красный
    """
    return StatusLight(status=status, size=size, parent=parent)


def set_status_light(light: StatusLight, status: str) -> None:
    """
    Изменить статус-огонька (изменить цвет)
    
    Args:
        light: StatusLight, созданный create_status_light()
        status: новый статус
        
    Пример:
        light = create_status_light("inactive")
        set_status_light(light, "success")  # Огонек станет зеленым
        
    Или используй метод напрямую:
        light.set_status("success")
    """
    if isinstance(light, StatusLight):
        light.set_status(status)
    else:
        print("⚠️ Ошибка: светильник должен быть создан через create_status_light()")


def apply_dialog_style(dialog: QDialog):
    """Применить стиль ко всему диалогу"""
    dialog.setStyleSheet(f"""
        QDialog {{
            background-color: {Colors.BG_LIGHT};
        }}
    """)





# ============================================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ============================================================================

EXAMPLE = """
from GUI_styles_helper import *
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

class MyPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Создаем элементы используя функции-помощники
        title = create_title("Мой заголовок")
        subtitle = create_subtitle("Это подзаголовок")
        
        input_email = create_input("Введите email")
        input_password = create_input("Введите пароль")
        
        btn_save = create_button("Сохранить", style="primary")
        btn_cancel = create_button("Отмена", style="secondary")
        btn_delete = create_button("Удалить", style="danger")
        
        combo = create_combobox(["Вариант 1", "Вариант 2"])
        
        # Создаем статус-огонек (красивый светодиод)
        status_light = create_status_light("success")  # Зеленый огонек
        status_label = create_body("Статус: Подключено")
        
        # Собираем layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(input_email)
        layout.addWidget(input_password)
        layout.addWidget(combo)
        
        # Статус с огоньком
        status_layout = QHBoxLayout()
        status_layout.addWidget(status_light)
        status_layout.addWidget(status_label)
        layout.addLayout(status_layout)
        
        buttons = QHBoxLayout()
        buttons.addWidget(btn_save)
        buttons.addWidget(btn_cancel)
        buttons.addWidget(btn_delete)
        
        layout.addLayout(buttons)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Позже можно изменить статус огонька
        # status_light.set_status("danger")  # Станет красным
        # или
        # set_status_light(status_light, "danger")
"""

if __name__ == "__main__":
    print("GUI Styles Helper")
    print("="*70)
    print("\nДоступные функции:")
    print("  - create_title(text)")
    print("  - create_subtitle(text)")
    print("  - create_body(text)")
    print("  - create_muted(text)")
    print("  - create_input(placeholder)")
    print("  - create_button(text, style)")
    print("  - create_combobox(items)")
    print("  - create_listwidget()")
    print("  - create_status_light(status, size)")
    print("  - set_status_light(light, status)")
    print("  - apply_dialog_style(dialog)")
    print("\nДоступные стили кнопок:")
    print("  - 'primary' (синяя, основная)")
    print("  - 'secondary' (белая с синей границей)")
    print("  - 'danger' (красная)")
    print("  - 'success' (зеленая)")
    print("\nДоступные статусы огонька:")
    print("  - 'success' (зеленый)")
    print("  - 'danger' (красный)")
    print("  - 'warning' (желтый)")
    print("  - 'inactive' (серый)")
    print("  - 'loading' (синий)")
    print("\nЦвета в Colors класе:")
    print(f"  - PRIMARY: {Colors.PRIMARY}")
    print(f"  - DANGER: {Colors.DANGER}")
    print(f"  - SUCCESS: {Colors.SUCCESS}")
    print("\n" + EXAMPLE)

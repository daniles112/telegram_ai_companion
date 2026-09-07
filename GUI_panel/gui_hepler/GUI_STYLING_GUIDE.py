#!/usr/bin/env python3
"""
ПОЛНОЕ РУКОВОДСТВО: Красивая стилизация PySide6 интерфейса

Все примеры используют согласованную цветовую схему Material Design
"""

# ============================================================================
# ЦВЕТОВАЯ СХЕМА
# ============================================================================

COLORS = {
    # Основные цвета
    "primary": "#1976d2",      # Синий (основной)
    "primary_dark": "#1565c0",  # Темный синий
    "primary_light": "#e3f2fd", # Светлый синий
    
    # Вторичные цвета
    "accent": "#ff6f00",        # Оранжевый
    "success": "#2ecc71",       # Зеленый
    "warning": "#f39c12",       # Желтый
    "danger": "#e74c3c",        # Красный
    
    # Нейтральные цвета
    "bg_light": "#f5f5f5",      # Светлый фон
    "bg_white": "#ffffff",      # Белый
    "border": "#e0e0e0",        # Граница
    "text_dark": "#212121",     # Темный текст
    "text_light": "#757575",    # Светлый текст
    "text_hint": "#bdbdbd",     # Подсказка
}

# ============================================================================
# 1. СТИЛИЗАЦИЯ DIALOGS / ОКОН
# ============================================================================

DIALOG_STYLE = f"""
    QDialog {{
        background-color: {COLORS["bg_light"]};
    }}
"""

# ============================================================================
# 2. СТИЛИЗАЦИЯ LABELS (ЗАГОЛОВКИ И ТЕКСТ)
# ============================================================================

LABEL_TITLE_STYLE = f"""
    QLabel {{
        color: {COLORS["text_dark"]};
        font-size: 18px;
        font-weight: bold;
        margin: 5px 0px;
    }}
"""

LABEL_SUBTITLE_STYLE = f"""
    QLabel {{
        color: {COLORS["text_light"]};
        font-size: 13px;
        margin: 3px 0px;
    }}
"""

LABEL_BODY_STYLE = f"""
    QLabel {{
        color: {COLORS["text_dark"]};
        font-size: 12px;
    }}
"""

# ============================================================================
# 3. СТИЛИЗАЦИЯ LINEEDIT (ТЕКСТОВЫЕ ПОЛЯ ВВОДА)
# ============================================================================

LINEEDIT_STYLE = f"""
    QLineEdit {{
        background-color: {COLORS["bg_white"]};
        border: 2px solid {COLORS["border"]};
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 12px;
        color: {COLORS["text_dark"]};
        selection-background-color: {COLORS["primary"]};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS["primary"]};
        background-color: {COLORS["bg_white"]};
    }}
    
    QLineEdit:hover {{
        border: 2px solid {COLORS["primary_dark"]};
    }}
    
    QLineEdit:disabled {{
        background-color: {COLORS["bg_light"]};
        color: {COLORS["text_hint"]};
    }}
"""

# ============================================================================
# 4. СТИЛИЗАЦИЯ PUSHBUTTON (КНОПКИ)
# ============================================================================

BUTTON_PRIMARY_STYLE = f"""
    QPushButton {{
        background-color: {COLORS["primary"]};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS["primary_dark"]};
    }}
    
    QPushButton:pressed {{
        background-color: #1565c0;
    }}
    
    QPushButton:disabled {{
        background-color: {COLORS["border"]};
        color: {COLORS["text_hint"]};
    }}
"""

BUTTON_SECONDARY_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLORS["primary"]};
        border: 2px solid {COLORS["primary"]};
        border-radius: 4px;
        padding: 6px 14px;
        font-weight: bold;
        font-size: 12px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS["primary_light"]};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS["primary"]};
        color: white;
    }}
    
    QPushButton:disabled {{
        border: 2px solid {COLORS["border"]};
        color: {COLORS["text_hint"]};
    }}
"""

BUTTON_DANGER_STYLE = f"""
    QPushButton {{
        background-color: {COLORS["danger"]};
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
"""

# ============================================================================
# 5. СТИЛИЗАЦИЯ COMBOBOX (ВЫПАДАЮЩИЕ СПИСКИ)
# ============================================================================

COMBOBOX_STYLE = f"""
    QComboBox {{
        background-color: {COLORS["bg_white"]};
        border: 2px solid {COLORS["border"]};
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 12px;
        color: {COLORS["text_dark"]};
    }}
    
    QComboBox:focus {{
        border: 2px solid {COLORS["primary"]};
    }}
    
    QComboBox:hover {{
        border: 2px solid {COLORS["primary"]};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: url();
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border"]};
        selection-background-color: {COLORS["primary"]};
        selection-color: white;
        padding: 4px 0px;
    }}
"""

# ============================================================================
# 6. СТИЛИЗАЦИЯ LISTWIDGET (СПИСКИ)
# ============================================================================

LISTWIDGET_STYLE = f"""
    QListWidget {{
        background-color: {COLORS["bg_white"]};
        border: 2px solid {COLORS["border"]};
        border-radius: 4px;
        outline: none;
    }}
    
    QListWidget::item {{
        padding: 10px 12px;
        border-bottom: 1px solid {COLORS["border"]};
        color: {COLORS["text_dark"]};
        font-size: 12px;
    }}
    
    QListWidget::item:hover {{
        background-color: {COLORS["primary_light"]};
        color: {COLORS["primary"]};
    }}
    
    QListWidget::item:selected {{
        background-color: {COLORS["primary"]};
        color: white;
        border-radius: 3px;
    }}
    
    QListWidget::item:focus {{
        outline: none;
    }}
"""

# ============================================================================
# 7. ПРИМЕР ИСПОЛЬЗОВАНИЯ В КОДЕ
# ============================================================================

EXAMPLE_CODE = '''
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class MyPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Создаем элементы
        title = QLabel("Мой заголовок")
        subtitle = QLabel("Подзаголовок")
        input_field = QLineEdit()
        button_save = QPushButton("Сохранить")
        button_cancel = QPushButton("Отмена")
        
        # Применяем стили
        title.setStyleSheet(LABEL_TITLE_STYLE)
        subtitle.setStyleSheet(LABEL_SUBTITLE_STYLE)
        input_field.setStyleSheet(LINEEDIT_STYLE)
        button_save.setStyleSheet(BUTTON_PRIMARY_STYLE)
        button_cancel.setStyleSheet(BUTTON_SECONDARY_STYLE)
        
        # Собираем layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(input_field)
        layout.addWidget(button_save)
        layout.addWidget(button_cancel)
        
        self.setLayout(layout)
'''

# ============================================================================
# 8. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

HELPER_FUNCTIONS = '''
def apply_style(widget, style_string):
    """Применить стиль к виджету"""
    widget.setStyleSheet(style_string)

def create_title(text, parent=None):
    """Создать красивый заголовок"""
    label = QLabel(text, parent)
    label.setStyleSheet(LABEL_TITLE_STYLE)
    return label

def create_subtitle(text, parent=None):
    """Создать красивый подзаголовок"""
    label = QLabel(text, parent)
    label.setStyleSheet(LABEL_SUBTITLE_STYLE)
    return label

def create_input(placeholder="", parent=None):
    """Создать красивое поле ввода"""
    input_field = QLineEdit(parent)
    input_field.setPlaceholderText(placeholder)
    input_field.setStyleSheet(LINEEDIT_STYLE)
    return input_field

def create_button(text, style="primary", parent=None):
    """Создать красивую кнопку"""
    button = QPushButton(text, parent)
    if style == "primary":
        button.setStyleSheet(BUTTON_PRIMARY_STYLE)
    elif style == "secondary":
        button.setStyleSheet(BUTTON_SECONDARY_STYLE)
    elif style == "danger":
        button.setStyleSheet(BUTTON_DANGER_STYLE)
    return button
'''

# ============================================================================
# ПРАВИЛА СТИЛИЗАЦИИ
# ============================================================================

GUIDELINES = """
╔══════════════════════════════════════════════════════════════════════════╗
║              ПРАВИЛА КРАСИВОЙ СТИЛИЗАЦИИ ИНТЕРФЕЙСА                     ║
╚══════════════════════════════════════════════════════════════════════════╝

1. 🎨 ЦВЕТОВАЯ СХЕМА
   ✓ Используй Material Design цвета
   ✓ Основной цвет: синий (#1976d2)
   ✓ Вторичный цвет: оранжевый (#ff6f00)
   ✓ Придерживайся 3-4 основных цветов

2. 📏 РАЗМЕРЫ И ОТСТУПЫ
   ✓ Заголовки: 18-20px
   ✓ Подзаголовки: 13-14px
   ✓ Обычный текст: 12px
   ✓ Паддинг кнопок: 8px 16px
   ✓ Паддинг полей: 8px 12px

3. 🔲 ГРАНИЦЫ И СКРУГЛЕНИЯ
   ✓ border-radius: 4px (основное)
   ✓ border-radius: 6-8px (большие элементы)
   ✓ Ширина границы: 2px для активного состояния
   ✓ Ширина границы: 1px для неактивного

4. ⌨️ ИНТЕРАКТИВНОСТЬ
   ✓ :hover → изменение цвета
   ✓ :focus → толще граница + основной цвет
   ✓ :pressed → еще более темный цвет
   ✓ :disabled → серый + пониженная опacity

5. 🔤 ШРИФТЫ
   ✓ Семейство: одно для всего приложения
   ✓ Жирность: bold для заголовков
   ✓ Жирность: normal для текста

6. 🎯 СОГЛАСОВАННОСТЬ
   ✓ Все кнопки одного размера (когда возможно)
   ✓ Все поля ввода одного стиля
   ✓ Одинаковые отступы везде
   ✓ Одна цветовая схема по всему приложению

7. 🌙 ТЕМНЫЙ / СВЕТЛЫЙ РЕЖИМ
   ✓ Светлый фон: #f5f5f5 или #ffffff
   ✓ Текст на светлом: #212121
   ✓ Подсказки: #757575

8. ✨ СОВЕТЫ
   ✓ Тень для глубины: box-shadow (опционально)
   ✓ Плавные переходы: могут замедлить
   ✓ Не более 10 разных цветов
   ✓ Используй одну цветовую палитру везде
"""

if __name__ == "__main__":
    print(GUIDELINES)
    print("\n" + "="*80)
    print("ПРИМЕР КОДА:")
    print("="*80)
    print(EXAMPLE_CODE)
    print("\n" + "="*80)
    print("ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ:")
    print("="*80)
    print(HELPER_FUNCTIONS)

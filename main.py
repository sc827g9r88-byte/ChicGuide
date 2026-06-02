# -*- coding: utf-8 -*-
"""
Fashion Advisor - Capsule Wardrobe & Occasion Styling Tool
A beautiful desktop application for fashion advice powered by AI
"""

import sys
import json
import os
from pathlib import Path
from typing import Optional, List

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QCheckBox,
    QDialog, QDialogButtonBox, QGridLayout, QScrollArea, QFrame,
    QStackedWidget, QTabWidget, QGroupBox, QRadioButton, QButtonGroup,
    QMessageBox, QProgressBar, QSlider, QSpinBox, QListWidget, QListWidgetItem,
    QFileDialog, QInputDialog, QSizePolicy, QSpacerItem, QSplitter,
)
from PySide6.QtCore import (
    Qt, QSize, QThread, Signal, QPropertyAnimation, QEasingCurve,
    QPoint, QTimer, QRect,
)
from PySide6.QtGui import (
    QColor, QPalette, QFont, QIcon, QPainter, QLinearGradient,
    QBrush, QPen, QFontDatabase, QPixmap, QCursor,
)

from color_data import SeasonalPalettes, SCENE_TEMPLATES, STYLE_KEYWORDS, INCOME_LEVELS
from brand_data import BrandDatabase, OCCUPATIONS, OCCUPATION_STYLE_MAP
from ai_client import AIClient, AIConfig


# =============================================================================
# CONSTANTS & STYLE
# =============================================================================

APP_NAME = "ChicGuide 穿搭顾问"
APP_VERSION = "1.0.0"
CONFIG_FILE = Path.home() / ".fashion_advisor_config.json"

# Soft feminine color scheme
COLORS = {
    "primary": "#D4849A",
    "primary_light": "#F5D5DC",
    "primary_dark": "#B06078",
    "secondary": "#9EB4C4",
    "accent": "#F0C9A0",
    "bg_main": "#FFF9FB",
    "bg_card": "#FFFFFF",
    "bg_sidebar": "#FDF5F7",
    "text_main": "#4A4A4A",
    "text_light": "#7A7A7A",
    "text_white": "#FFFFFF",
    "border": "#F0E0E5",
    "success": "#7EB8A0",
    "warning": "#E8C08C",
    "error": "#D48484",
}

SIDEBAR_STYLE = f"""
QWidget#Sidebar {{
    background-color: {COLORS["bg_sidebar"]};
    border-right: 1px solid {COLORS["border"]};
}}
"""

NAV_BUTTON_STYLE = f"""
QPushButton#NavButton {{
    background-color: transparent;
    color: {COLORS["text_light"]};
    border: none;
    padding: 16px 24px;
    text-align: left;
    font-size: 15px;
    font-weight: 500;
    border-radius: 12px;
    margin: 4px 12px;
}}
QPushButton#NavButton:hover {{
    background-color: {COLORS["primary_light"]};
    color: {COLORS["primary_dark"]};
}}
QPushButton#NavButton:checked {{
    background-color: {COLORS["primary"]};
    color: {COLORS["text_white"]};
    font-weight: 600;
}}
"""

CARD_STYLE = f"""
QFrame#Card {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 16px;
    padding: 20px;
}}
QFrame#Card:hover {{
    border: 2px solid {COLORS["primary_light"]};
}}
"""

COLOR_SQUARE_STYLE = """
QFrame#ColorSquare {
    border-radius: 12px;
    border: 2px solid rgba(255,255,255,0.6);
}
"""

BUTTON_PRIMARY_STYLE = f"""
QPushButton#PrimaryButton {{
    background-color: {COLORS["primary"]};
    color: white;
    border: none;
    padding: 12px 32px;
    border-radius: 24px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton#PrimaryButton:hover {{
    background-color: {COLORS["primary_dark"]};
}}
QPushButton#PrimaryButton:pressed {{
    background-color: {COLORS["primary_dark"]};
    padding: 13px 32px 11px 32px;
}}
QPushButton#PrimaryButton:disabled {{
    background-color: #D5D5D5;
    color: #999;
}}
"""

BUTTON_SECONDARY_STYLE = f"""
QPushButton#SecondaryButton {{
    background-color: white;
    color: {COLORS["primary"]};
    border: 2px solid {COLORS["primary"]};
    padding: 10px 28px;
    border-radius: 24px;
    font-size: 14px;
    font-weight: 500;
}}
QPushButton#SecondaryButton:hover {{
    background-color: {COLORS["primary_light"]};
}}
"""

INPUT_STYLE = f"""
QLineEdit, QTextEdit, QComboBox {{
    background-color: white;
    border: 2px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 14px;
    color: {COLORS["text_main"]};
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 2px solid {COLORS["primary"]};
}}
QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {COLORS["text_light"]};
}}
QComboBox::drop-down {{
    border: none;
    width: 30px;
}}
QComboBox QAbstractItemView {{
    background-color: white;
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    selection-background-color: {COLORS["primary_light"]};
    selection-color: {COLORS["text_main"]};
    padding: 8px;
}}
"""

SCROLL_STYLE = f"""
QScrollArea {{
    border: none;
    background-color: transparent;
}}
QScrollBar:vertical {{
    background: {COLORS["bg_main"]};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS["primary_light"]};
    border-radius: 4px;
    min-height: 40px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS["primary"]};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background: {COLORS["bg_main"]};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS["primary_light"]};
    border-radius: 4px;
    min-width: 40px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {COLORS["primary"]};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""

CHECKBOX_STYLE = f"""
QCheckBox {{
    spacing: 8px;
    font-size: 14px;
    color: {COLORS["text_main"]};
    padding: 6px 12px;
    background-color: white;
    border: 2px solid {COLORS["border"]};
    border-radius: 20px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {COLORS["border"]};
    background-color: white;
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS["primary"]};
    border-color: {COLORS["primary"]};
}}
QCheckBox::indicator:checked::after {{
    content: "✓";
    color: white;
    font-size: 12px;
}}
QCheckBox:hover {{
    border-color: {COLORS["primary_light"]};
}}
"""

LABEL_STYLE = f"""
QLabel#Title {{
    font-size: 28px;
    font-weight: 700;
    color: {COLORS["text_main"]};
    padding: 8px 0;
}}
QLabel#Subtitle {{
    font-size: 16px;
    color: {COLORS["text_light"]};
    padding: 4px 0;
}}
QLabel#SectionTitle {{
    font-size: 20px;
    font-weight: 600;
    color: {COLORS["primary_dark"]};
    padding: 16px 0 8px 0;
}}
QLabel#CardTitle {{
    font-size: 16px;
    font-weight: 600;
    color: {COLORS["text_main"]};
}}
QLabel#CardText {{
    font-size: 13px;
    color: {COLORS["text_light"]};
    line-height: 1.5;
}}
QLabel#ColorName {{
    font-size: 12px;
    font-weight: 600;
    color: {COLORS["text_main"]};
}}
QLabel#ColorId {{
    font-size: 10px;
    color: {COLORS["text_light"]};
}}
QLabel#Result {{
    font-size: 14px;
    color: {COLORS["text_main"]};
    line-height: 1.8;
    padding: 12px;
    background-color: white;
    border-radius: 12px;
    border: 1px solid {COLORS["border"]};
}}
"""

TAG_STYLE = f"""
QLabel#Tag {{
    background-color: {COLORS["primary_light"]};
    color: {COLORS["primary_dark"]};
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}}
"""


# =============================================================================
# WORKER THREADS
# =============================================================================

class AIWorker(QThread):
    """Worker thread for AI API calls"""
    result_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, client: AIClient, messages: list):
        super().__init__()
        self.client = client
        self.messages = messages

    def run(self):
        try:
            result = self.client.chat(self.messages)
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))


# =============================================================================
# CUSTOM WIDGETS
# =============================================================================

class ColorCard(QFrame):
    """A color display card widget"""

    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setObjectName("Card")
        self.setFixedSize(140, 180)
        self.setStyleSheet(CARD_STYLE + COLOR_SQUARE_STYLE)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Color square
        color_frame = QFrame()
        color_frame.setObjectName("ColorSquare")
        color_frame.setFixedSize(100, 100)
        color_frame.setStyleSheet(
            f"QFrame#ColorSquare {{"
            f"  background-color: {self.color.hex_value};"
            f"  border-radius: 12px;"
            f"  border: 2px solid rgba(255,255,255,0.6);"
            f"}}"
        )
        layout.addWidget(color_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        # Color ID
        id_label = QLabel(self.color.id)
        id_label.setObjectName("ColorId")
        id_label.setStyleSheet(LABEL_STYLE)
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(id_label)

        # Color name
        name_label = QLabel(self.color.name)
        name_label.setObjectName("ColorName")
        name_label.setStyleSheet(LABEL_STYLE)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)


class SceneTag(QPushButton):
    """Clickable scene tag button"""

    clicked_scene = Signal(str)

    def __init__(self, scene_text, parent=None):
        super().__init__(scene_text, parent)
        self.scene_text = scene_text
        self.setCheckable(True)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {COLORS["text_main"]};
                border: 2px solid {COLORS["border"]};
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                border-color: {COLORS["primary"]};
                color: {COLORS["primary"]};
            }}
            QPushButton:checked {{
                background-color: {COLORS["primary"]};
                color: white;
                border-color: {COLORS["primary"]};
            }}
        """)
        self.clicked.connect(self._on_click)

    def _on_click(self):
        self.clicked_scene.emit(self.scene_text)


class StyleCheckbox(QWidget):
    """Custom styled checkbox for style selection"""

    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.checkbox = QCheckBox(text)
        self.checkbox.setStyleSheet(f"""
            QCheckBox {{
                spacing: 6px;
                font-size: 14px;
                color: {COLORS["text_main"]};
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 2px solid {COLORS["border"]};
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS["primary"]};
                border-color: {COLORS["primary"]};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIgNkM1IDkgMTAgMiAxMCAyIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
            }}
            QCheckBox::indicator:hover {{
                border-color: {COLORS["primary"]};
            }}
        """)
        layout.addWidget(self.checkbox)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, checked):
        self.checkbox.setChecked(checked)


# =============================================================================
# API SETTINGS DIALOG
# =============================================================================

class APISettingsDialog(QDialog):
    """Dialog for configuring AI API settings"""

    def __init__(self, parent=None, current_config: Optional[AIConfig] = None):
        super().__init__(parent)
        self.setWindowTitle("API 设置")
        self.setMinimumWidth(520)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS["bg_main"]};
            }}
            {INPUT_STYLE}
            {BUTTON_PRIMARY_STYLE}
            {LABEL_STYLE}
        """)
        self.config = current_config or AIConfig()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)

        # Title
        title = QLabel("AI 模型 API 设置")
        title.setObjectName("Title")
        title.setStyleSheet(LABEL_STYLE)
        layout.addWidget(title)

        subtitle = QLabel("选择并配置你想要使用的大模型 API")
        subtitle.setObjectName("Subtitle")
        subtitle.setStyleSheet(LABEL_STYLE)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        # Provider selection
        provider_label = QLabel("选择 API 提供商")
        provider_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_main']};")
        layout.addWidget(provider_label)

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "通义千问 (Qwen)", "Kimi (Moonshot)", "DeepSeek", "自定义"])
        self.provider_combo.currentIndexChanged.connect(self.on_provider_change)
        layout.addWidget(self.provider_combo)
        layout.addSpacing(12)

        # Model selection
        model_label = QLabel("选择模型")
        model_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_main']};")
        layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        layout.addWidget(self.model_combo)
        layout.addSpacing(12)

        # API Base URL
        base_label = QLabel("API Base URL（一般保持默认即可）")
        base_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_main']};")
        layout.addWidget(base_label)

        self.base_input = QLineEdit()
        self.base_input.setPlaceholderText("https://api.openai.com/v1")
        layout.addWidget(self.base_input)
        layout.addSpacing(12)

        # API Key
        key_label = QLabel("API Key")
        key_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_main']};")
        layout.addWidget(key_label)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("输入你的 API Key...")
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.key_input)

        # Show key checkbox
        show_key = QCheckBox("显示 API Key")
        show_key.stateChanged.connect(self.toggle_key_visibility)
        layout.addWidget(show_key)
        layout.addSpacing(12)

        # Temperature
        temp_layout = QHBoxLayout()
        temp_label = QLabel("Temperature（创造性）：")
        temp_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_main']};")
        temp_layout.addWidget(temp_label)
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(80)
        self.temp_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 8px;
                background: {COLORS["border"]};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                width: 20px;
                height: 20px;
                background: {COLORS["primary"]};
                border-radius: 10px;
                margin: -6px 0;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS["primary"]};
                border-radius: 4px;
            }}
        """)
        temp_layout.addWidget(self.temp_slider)
        self.temp_value = QLabel("0.8")
        self.temp_value.setStyleSheet(f"color: {COLORS['primary']}; font-weight: 600;")
        temp_layout.addWidget(self.temp_value)
        self.temp_slider.valueChanged.connect(
            lambda v: self.temp_value.setText(f"{v/100:.1f}")
        )
        layout.addLayout(temp_layout)
        layout.addSpacing(20)

        # Test connection button
        test_btn = QPushButton("测试连接")
        test_btn.setObjectName("SecondaryButton")
        test_btn.setStyleSheet(BUTTON_SECONDARY_STYLE)
        test_btn.clicked.connect(self.test_connection)
        layout.addWidget(test_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        # Buttons
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        # Style the buttons
        ok_btn = btn_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setText("保存")
        ok_btn.setObjectName("PrimaryButton")
        ok_btn.setStyleSheet(BUTTON_PRIMARY_STYLE)

        cancel_btn = btn_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_btn.setText("取消")
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.setStyleSheet(BUTTON_SECONDARY_STYLE)

        layout.addWidget(btn_box)

        # Load current config
        self.load_config()

    def load_config(self):
        """Load current configuration into UI"""
        provider_map = {
            "openai": 0, "qwen": 1, "kimi": 2, "deepseek": 3, "custom": 4
        }
        idx = provider_map.get(self.config.provider, 0)
        self.provider_combo.setCurrentIndex(idx)
        self.on_provider_change(idx)

        self.model_combo.setCurrentText(self.config.model)
        self.base_input.setText(self.config.api_base)
        self.key_input.setText(self.config.api_key)
        self.temp_slider.setValue(int(self.config.temperature * 100))

    def on_provider_change(self, index):
        """Handle provider selection change"""
        providers = ["openai", "qwen", "kimi", "deepseek", "custom"]
        provider = providers[index]

        if provider == "custom":
            self.model_combo.clear()
            self.model_combo.setPlaceholderText("输入自定义模型名称...")
            self.base_input.setPlaceholderText("输入自定义 API URL...")
            self.base_input.setReadOnly(False)
        else:
            models = AIClient.get_models_for_provider(provider)
            self.model_combo.clear()
            self.model_combo.addItems(models)
            default_model = AIClient.get_default_model(provider)
            self.model_combo.setCurrentText(default_model)

            defaults = AIClient.PROVIDER_DEFAULTS.get(provider, {})
            self.base_input.setText(defaults.get("api_base", ""))
            self.base_input.setReadOnly(True)

    def toggle_key_visibility(self, state):
        """Toggle API key visibility"""
        if state == Qt.CheckState.Checked:
            self.key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def test_connection(self):
        """Test the API connection"""
        config = self.get_config()
        if not config.api_key:
            QMessageBox.warning(self, "警告", "请先输入 API Key")
            return

        client = AIClient(config)
        btn = self.sender()
        btn.setText("测试中...")
        btn.setEnabled(False)
        QApplication.processEvents()

        success = client.test_connection()

        btn.setText("测试连接")
        btn.setEnabled(True)

        if success:
            QMessageBox.information(self, "成功", "API 连接成功！")
        else:
            QMessageBox.critical(self, "失败", "API 连接失败，请检查设置。")

    def get_config(self) -> AIConfig:
        """Get the configured AIConfig"""
        providers = ["openai", "qwen", "kimi", "deepseek", "custom"]
        provider = providers[self.provider_combo.currentIndex()]

        return AIConfig(
            provider=provider,
            api_key=self.key_input.text().strip(),
            api_base=self.base_input.text().strip(),
            model=self.model_combo.currentText(),
            temperature=self.temp_slider.value() / 100,
        )


# =============================================================================
# SUBSYSTEM 1: SEASONAL COLOR CARD
# =============================================================================

class ColorCardSubsystem(QWidget):
    """Seasonal Color Palette Browser"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 16)

        title = QLabel("四季色卡")
        title.setObjectName("Title")
        title.setStyleSheet(LABEL_STYLE)
        header_layout.addWidget(title)

        subtitle = QLabel("选择你当前的季节，发现最适合你的色彩灵感")
        subtitle.setObjectName("Subtitle")
        subtitle.setStyleSheet(LABEL_STYLE)
        header_layout.addWidget(subtitle)

        # Season selector tabs
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(32, 8, 32, 16)
        tab_layout.setSpacing(12)

        self.season_buttons = []
        seasons = [
            ("spring", "春 Spring", "#F4A198"),
            ("summer", "夏 Summer", "#87CEEB"),
            ("autumn", "秋 Autumn", "#C68E53"),
            ("winter", "冬 Winter", "#9EB4C4"),
        ]

        for key, label, color in seasons:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("season", key)
            btn.setFixedSize(140, 44)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    color: {COLORS["text_main"]};
                    border: 2px solid {COLORS["border"]};
                    border-radius: 22px;
                    font-size: 14px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    border-color: {color};
                    color: {color};
                }}
                QPushButton:checked {{
                    background-color: {color};
                    color: white;
                    border-color: {color};
                }}
            """)
            btn.clicked.connect(lambda checked, k=key: self.on_season_change(k))
            self.season_buttons.append(btn)
            tab_layout.addWidget(btn)

        tab_layout.addStretch()
        header_layout.addWidget(tab_widget)
        layout.addWidget(header)

        # Scroll area for colors
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(SCROLL_STYLE)

        self.color_container = QWidget()
        self.color_container.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        self.color_layout = QGridLayout(self.color_container)
        self.color_layout.setContentsMargins(32, 16, 32, 32)
        self.color_layout.setSpacing(16)
        self.color_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.scroll.setWidget(self.color_container)
        layout.addWidget(self.scroll)

        # Select spring by default
        self.on_season_change("spring")
        self.season_buttons[0].setChecked(True)

    def on_season_change(self, season_key: str):
        """Handle season tab change"""
        # Update button states
        for btn in self.season_buttons:
            btn.setChecked(btn.property("season") == season_key)

        # Clear current colors
        while self.color_layout.count():
            item = self.color_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Load season data
        season_data = SeasonalPalettes.get_season(season_key)
        if not season_data:
            return

        # Season description
        desc = QLabel(f"{season_data['description']} — 共 {len(season_data['colors'])} 色")
        desc.setStyleSheet(f"font-size: 14px; color: {COLORS['text_light']}; padding: 8px 0;")
        self.color_layout.addWidget(desc, 0, 0, 1, 4)

        # Color cards
        row = 1
        col = 0
        for color in season_data["colors"]:
            card = ColorCard(color)
            self.color_layout.addWidget(card, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

        self.color_layout.setRowStretch(row + 1, 1)


# =============================================================================
# SUBSYSTEM 2: SCENE OUTFIT ADVISOR
# =============================================================================

class OutfitAdvisorSubsystem(QWidget):
    """AI-powered outfit advice for different scenes"""

    def __init__(self, parent=None, ai_client: Optional[AIClient] = None):
        super().__init__(parent)
        self.ai_client = ai_client
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 16)

        title = QLabel("场合穿搭顾问")
        title.setObjectName("Title")
        title.setStyleSheet(LABEL_STYLE)
        header_layout.addWidget(title)

        subtitle = QLabel("告诉我你的出行场景，AI 为你量身定制穿搭方案")
        subtitle.setObjectName("Subtitle")
        subtitle.setStyleSheet(LABEL_STYLE)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        # Content area with splitter
        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 8, 32, 32)
        content_layout.setSpacing(20)

        # Scene input section
        input_section = QFrame()
        input_section.setObjectName("Card")
        input_section.setStyleSheet(CARD_STYLE)
        input_layout = QVBoxLayout(input_section)
        input_layout.setContentsMargins(24, 24, 24, 24)
        input_layout.setSpacing(16)

        # Scene input
        scene_label = QLabel("今天要去哪里？")
        scene_label.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {COLORS['text_main']};")
        input_layout.addWidget(scene_label)

        self.scene_input = QLineEdit()
        self.scene_input.setPlaceholderText("描述你的场景，比如：去参加面试、下雨天去上课、美术馆看展...")
        self.scene_input.setMinimumHeight(44)
        self.scene_input.setStyleSheet(INPUT_STYLE)
        input_layout.addWidget(self.scene_input)

        # Quick scene tags
        tags_label = QLabel("或选择常见场景：")
        tags_label.setStyleSheet(f"font-size: 13px; color: {COLORS['text_light']}; margin-top: 8px;")
        input_layout.addWidget(tags_label)

        tags_container = QWidget()
        tags_grid = QGridLayout(tags_container)
        tags_grid.setContentsMargins(0, 0, 0, 0)
        tags_grid.setSpacing(8)
        tags_grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.scene_tags = []
        row, col = 0, 0
        for scene in SCENE_TEMPLATES:
            tag = SceneTag(scene)
            tag.clicked_scene.connect(self.on_scene_tag_clicked)
            self.scene_tags.append(tag)
            tags_grid.addWidget(tag, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

        tags_scroll = QScrollArea()
        tags_scroll.setWidgetResizable(True)
        tags_scroll.setMaximumHeight(100)
        tags_scroll.setStyleSheet(SCROLL_STYLE + "QScrollArea { border: none; background: transparent; }")
        tags_scroll.setWidget(tags_container)
        input_layout.addWidget(tags_scroll)

        # Optional: season & style
        options_layout = QHBoxLayout()

        season_label = QLabel("季节（可选）：")
        season_label.setStyleSheet(f"font-size: 13px; color: {COLORS['text_light']};")
        options_layout.addWidget(season_label)

        self.season_combo = QComboBox()
        self.season_combo.addItems(["自动检测", "春季", "夏季", "秋季", "冬季"])
        self.season_combo.setFixedWidth(120)
        self.season_combo.setStyleSheet(INPUT_STYLE)
        options_layout.addWidget(self.season_combo)
        options_layout.addSpacing(20)

        style_label = QLabel("风格偏好（可选）：")
        style_label.setStyleSheet(f"font-size: 13px; color: {COLORS['text_light']};")
        options_layout.addWidget(style_label)

        self.style_input = QLineEdit()
        self.style_input.setPlaceholderText("如：简约、优雅...")
        self.style_input.setFixedWidth(200)
        self.style_input.setStyleSheet(INPUT_STYLE)
        options_layout.addWidget(self.style_input)
        options_layout.addStretch()

        input_layout.addLayout(options_layout)

        # Submit button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.submit_btn = QPushButton("获取穿搭建议")
        self.submit_btn.setObjectName("PrimaryButton")
        self.submit_btn.setStyleSheet(BUTTON_PRIMARY_STYLE)
        self.submit_btn.setFixedSize(180, 48)
        self.submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.submit_btn.clicked.connect(self.on_get_advice)
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addStretch()

        input_layout.addLayout(btn_layout)
        content_layout.addWidget(input_section)

        # Result area
        result_section = QFrame()
        result_section.setObjectName("Card")
        result_section.setStyleSheet(CARD_STYLE)
        result_layout = QVBoxLayout(result_section)
        result_layout.setContentsMargins(24, 24, 24, 24)
        result_layout.setSpacing(12)

        result_header = QHBoxLayout()
        result_title = QLabel("穿搭建议")
        result_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['text_main']};")
        result_header.addWidget(result_title)

        self.loading_label = QLabel("思考中...")
        self.loading_label.setStyleSheet(f"color: {COLORS['primary']}; font-size: 14px;")
        self.loading_label.setVisible(False)
        result_header.addWidget(self.loading_label)
        result_header.addStretch()

        result_layout.addLayout(result_header)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("点击上方按钮获取 AI 穿搭建议...")
        self.result_text.setMinimumHeight(300)
        self.result_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.8;
                color: {COLORS['text_main']};
            }}
        """)
        result_layout.addWidget(self.result_text)

        content_layout.addWidget(result_section)
        layout.addWidget(content)

    def on_scene_tag_clicked(self, scene: str):
        """Handle scene tag click"""
        self.scene_input.setText(scene)
        # Uncheck other tags
        for tag in self.scene_tags:
            if tag.scene_text != scene:
                tag.setChecked(False)

    def on_get_advice(self):
        """Get outfit advice from AI"""
        scene = self.scene_input.text().strip()
        if not scene:
            QMessageBox.warning(self, "提示", "请先描述你的出行场景")
            return

        if not self.ai_client or not self.ai_client.config.api_key:
            QMessageBox.warning(self, "提示", "请先配置 AI API 设置（点击左下角设置按钮）")
            return

        season = self.season_combo.currentText()
        if season == "自动检测":
            season = ""

        style = self.style_input.text().strip()

        self.submit_btn.setEnabled(False)
        self.loading_label.setVisible(True)
        self.result_text.setText("")

        # Create worker thread
        messages = [
            {"role": "system", "content": """你是一位专业的时尚穿搭顾问，擅长为女性用户提供场合穿搭建议。
请根据用户描述的场景，提供1-2套完整的搭配方案。

每套方案需要包含：
1. 整体搭配概述
2. 上装、下装、鞋履、配饰的具体推荐
3. 从以下四个维度分析为什么这样搭配：
   - 色彩：选择的色系如何适合该场合
   - 款式：单品款式如何符合场合需求
   - 风格：整体风格如何匹配场景氛围
   - 场合逻辑：为什么这样的穿搭在该场合得体且实用

请用中文回答，语言亲切友好，像闺蜜在分享穿搭建议一样。
格式清晰，使用emoji让内容更生动。"""},
            {"role": "user", "content": f"场景：{scene}\n季节：{season}\n风格偏好：{style}"},
        ]

        self.worker = AIWorker(self.ai_client, messages)
        self.worker.result_ready.connect(self.on_advice_ready)
        self.worker.error_occurred.connect(self.on_advice_error)
        self.worker.start()

    def on_advice_ready(self, result: str):
        """Handle advice result"""
        self.submit_btn.setEnabled(True)
        self.loading_label.setVisible(False)
        self.result_text.setText(result)

    def on_advice_error(self, error: str):
        """Handle advice error"""
        self.submit_btn.setEnabled(True)
        self.loading_label.setVisible(False)
        self.result_text.setText(f"获取建议时出错：{error}")


# =============================================================================
# SUBSYSTEM 3: BRAND RECOMMENDATION
# =============================================================================

class BrandRecommendationSubsystem(QWidget):
    """Brand recommendation based on income and style preferences"""

    def __init__(self, parent=None, ai_client: Optional[AIClient] = None):
        super().__init__(parent)
        self.ai_client = ai_client
        self.selected_styles = []
        self.current_recommendations = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 16)

        title = QLabel("品牌选购指南")
        title.setObjectName("Title")
        title.setStyleSheet(LABEL_STYLE)
        header_layout.addWidget(title)

        subtitle = QLabel("根据你的职业、收入和风格偏好，为你推荐最适合的服装品牌")
        subtitle.setObjectName("Subtitle")
        subtitle.setStyleSheet(LABEL_STYLE)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        # Scroll content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(SCROLL_STYLE)

        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 8, 32, 32)
        content_layout.setSpacing(20)

        # Input section
        input_section = QFrame()
        input_section.setObjectName("Card")
        input_section.setStyleSheet(CARD_STYLE)
        input_layout = QVBoxLayout(input_section)
        input_layout.setContentsMargins(24, 24, 24, 24)
        input_layout.setSpacing(20)

        # Occupation
        occ_label = QLabel("你的职业")
        occ_label.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {COLORS['text_main']};")
        input_layout.addWidget(occ_label)

        self.occ_combo = QComboBox()
        self.occ_combo.addItems(OCCUPATIONS)
        self.occ_combo.setStyleSheet(INPUT_STYLE)
        self.occ_combo.currentTextChanged.connect(self.on_occupation_change)
        input_layout.addWidget(self.occ_combo)

        # Income
        income_label = QLabel("月薪/可支配收入水平")
        income_label.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {COLORS['text_main']};")
        input_layout.addWidget(income_label)

        self.income_combo = QComboBox()
        self.income_combo.addItems(INCOME_LEVELS)
        self.income_combo.setStyleSheet(INPUT_STYLE)
        input_layout.addWidget(self.income_combo)

        # Style selection
        style_label = QLabel("喜欢的穿搭风格（可多选）")
        style_label.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {COLORS['text_main']};")
        input_layout.addWidget(style_label)

        style_container = QWidget()
        style_grid = QGridLayout(style_container)
        style_grid.setContentsMargins(0, 0, 0, 0)
        style_grid.setSpacing(10)
        style_grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.style_checkboxes = []
        row, col = 0, 0
        for style in STYLE_KEYWORDS:
            cb = StyleCheckbox(style)
            self.style_checkboxes.append(cb)
            style_grid.addWidget(cb, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

        input_layout.addWidget(style_container)

        # Submit button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.submit_btn = QPushButton("获取品牌推荐")
        self.submit_btn.setObjectName("PrimaryButton")
        self.submit_btn.setStyleSheet(BUTTON_PRIMARY_STYLE)
        self.submit_btn.setFixedSize(180, 48)
        self.submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.submit_btn.clicked.connect(self.on_get_recommendations)
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addStretch()

        input_layout.addLayout(btn_layout)
        content_layout.addWidget(input_section)

        # Results section
        self.results_section = QFrame()
        self.results_section.setObjectName("Card")
        self.results_section.setStyleSheet(CARD_STYLE)
        self.results_section.setVisible(False)
        self.results_layout = QVBoxLayout(self.results_section)
        self.results_layout.setContentsMargins(24, 24, 24, 24)
        self.results_layout.setSpacing(16)

        content_layout.addWidget(self.results_section)
        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def on_occupation_change(self, occupation: str):
        """Auto-select styles based on occupation"""
        suggested = OCCUPATION_STYLE_MAP.get(occupation, [])
        for cb in self.style_checkboxes:
            cb.setChecked(cb.checkbox.text() in suggested)

    def get_selected_styles(self) -> List[str]:
        """Get list of selected style keywords"""
        return [cb.checkbox.text() for cb in self.style_checkboxes if cb.isChecked()]

    def on_get_recommendations(self):
        """Generate brand recommendations"""
        styles = self.get_selected_styles()
        if not styles:
            QMessageBox.warning(self, "提示", "请至少选择一个穿搭风格")
            return

        occupation = self.occ_combo.currentText()
        income = self.income_combo.currentText()

        # Clear previous results
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get recommendations from database
        recommendations = BrandDatabase.recommend(income, styles, limit=3)

        if not recommendations:
            no_result = QLabel("抱歉，暂时没有找到匹配的品牌推荐。请尝试调整你的风格偏好。")
            no_result.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 14px;")
            self.results_layout.addWidget(no_result)
            self.results_section.setVisible(True)
            return

        self.current_recommendations = recommendations

        # Header
        result_title = QLabel(f"为你推荐 {len(recommendations)} 个品牌")
        result_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['primary_dark']};")
        self.results_layout.addWidget(result_title)

        # User profile summary
        profile = QLabel(f"职业：{occupation}  |  收入：{income}  |  风格：{'、'.join(styles)}")
        profile.setStyleSheet(f"font-size: 13px; color: {COLORS['text_light']}; padding: 4px 0;")
        self.results_layout.addWidget(profile)
        self.results_layout.addSpacing(8)

        # Recommendation cards
        for i, rec in enumerate(recommendations, 1):
            brand = rec["brand"]
            card = QFrame()
            card.setObjectName("Card")
            card.setStyleSheet(f"""
                QFrame#Card {{
                    background-color: {COLORS['bg_main']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 12px;
                    padding: 16px;
                }}
                QFrame#Card:hover {{
                    border: 2px solid {COLORS['primary_light']};
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(10)

            # Brand header
            header_layout = QHBoxLayout()

            brand_name = QLabel(f"{i}. {brand.name}")
            brand_name.setStyleSheet(f"font-size: 17px; font-weight: 700; color: {COLORS['text_main']};")
            header_layout.addWidget(brand_name)
            header_layout.addStretch()

            # Price tag
            price_tag = QLabel(f"{brand.price_range_cn}")
            price_tag.setObjectName("Tag")
            price_tag.setStyleSheet(TAG_STYLE)
            header_layout.addWidget(price_tag)

            # Category tag
            cat_tag = QLabel(brand.category)
            cat_tag.setObjectName("Tag")
            cat_tag.setStyleSheet(TAG_STYLE)
            header_layout.addWidget(cat_tag)

            card_layout.addLayout(header_layout)

            # Description
            desc = QLabel(brand.description)
            desc.setStyleSheet(f"font-size: 13px; color: {COLORS['text_light']}; line-height: 1.5;")
            desc.setWordWrap(True)
            card_layout.addWidget(desc)

            # Matching styles
            styles_layout = QHBoxLayout()
            styles_layout.setSpacing(6)
            ms_label = QLabel("匹配风格：")
            ms_label.setStyleSheet(f"font-size: 12px; color: {COLORS['text_light']};")
            styles_layout.addWidget(ms_label)

            for ms in rec["matching_styles"]:
                ms_tag = QLabel(ms)
                ms_tag.setStyleSheet(f"""
                    QLabel {{
                        background-color: {COLORS['primary']};
                        color: white;
                        padding: 2px 10px;
                        border-radius: 10px;
                        font-size: 12px;
                    }}
                """)
                styles_layout.addWidget(ms_tag)
            styles_layout.addStretch()
            card_layout.addLayout(styles_layout)

            # Recommendation reason
            reason_title = QLabel("推荐理由：")
            reason_title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {COLORS['primary_dark']};")
            card_layout.addWidget(reason_title)

            reason = QLabel(rec["reason"])
            reason.setStyleSheet(f"font-size: 13px; color: {COLORS['text_main']}; line-height: 1.6;")
            reason.setWordWrap(True)
            card_layout.addWidget(reason)

            # Feedback buttons
            feedback_layout = QHBoxLayout()
            feedback_layout.addStretch()

            like_btn = QPushButton("满意")
            like_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['success']};
                    color: white;
                    border: none;
                    padding: 6px 20px;
                    border-radius: 16px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: #6BA088;
                }}
            """)
            like_btn.clicked.connect(lambda: self.on_feedback(brand.name, True))
            feedback_layout.addWidget(like_btn)

            dislike_btn = QPushButton("不太合适")
            dislike_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    color: {COLORS['text_light']};
                    border: 1px solid {COLORS['border']};
                    padding: 6px 20px;
                    border-radius: 16px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    border-color: {COLORS['error']};
                    color: {COLORS['error']};
                }}
            """)
            dislike_btn.clicked.connect(lambda checked, b=brand: self.on_feedback(b, False))
            feedback_layout.addWidget(dislike_btn)

            card_layout.addLayout(feedback_layout)
            self.results_layout.addWidget(card)
            self.results_layout.addSpacing(8)

        # AI feedback section
        ai_feedback_title = QLabel("对推荐有疑问？")
        ai_feedback_title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {COLORS['text_main']}; margin-top: 16px;")
        self.results_layout.addWidget(ai_feedback_title)

        ai_hint = QLabel("可以直接向 AI 提问，比如：\"我想找更平价的品牌\"、\"想要更多鞋履推荐\"")
        ai_hint.setStyleSheet(f"font-size: 13px; color: {COLORS['text_light']};")
        self.results_layout.addWidget(ai_hint)

        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText("输入你的问题...")
        self.ai_input.setStyleSheet(INPUT_STYLE)
        self.ai_input.returnPressed.connect(self.on_ai_feedback)
        self.results_layout.addWidget(self.ai_input)

        ai_btn = QPushButton("向 AI 咨询")
        ai_btn.setObjectName("PrimaryButton")
        ai_btn.setStyleSheet(f"{BUTTON_PRIMARY_STYLE} QPushButton {{ padding: 8px 24px; }}")
        ai_btn.clicked.connect(self.on_ai_feedback)
        self.results_layout.addWidget(ai_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # AI response
        self.ai_response = QTextEdit()
        self.ai_response.setReadOnly(True)
        self.ai_response.setPlaceholderText("AI 的回复会显示在这里...")
        self.ai_response.setMaximumHeight(200)
        self.ai_response.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
            }}
        """)
        self.ai_response.setVisible(False)
        self.results_layout.addWidget(self.ai_response)

        self.results_section.setVisible(True)

    def on_feedback(self, brand_name, is_positive):
        """Handle feedback on recommendations"""
        if is_positive:
            QMessageBox.information(self, "反馈", f" glad you like {brand_name}!")
        else:
            reply = QMessageBox.question(
                self, "调整推荐",
                f"是否需要为你重新推荐类似品牌替代 {brand_name}？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.on_get_recommendations()

    def on_ai_feedback(self):
        """Send feedback to AI for dynamic adjustment"""
        question = self.ai_input.text().strip()
        if not question:
            return

        if not self.ai_client or not self.ai_client.config.api_key:
            QMessageBox.warning(self, "提示", "请先配置 AI API 设置")
            return

        occupation = self.occ_combo.currentText()
        income = self.income_combo.currentText()
        styles = self.get_selected_styles()

        context = {
            "occupation": occupation,
            "income": income,
            "styles": styles,
        }

        self.ai_response.setVisible(True)
        self.ai_response.setText("AI 正在思考...")

        prev_brands = ", ".join([r["brand"].name for r in self.current_recommendations])
        style_str = "、".join(styles)
        user_content = (
            f"用户背景：\n职业：{occupation}\n收入：{income}\n"
            f"风格：{style_str}\n\n"
            f"之前推荐的品牌：{prev_brands}\n\n"
            f"用户反馈：{question}\n\n请根据用户反馈调整推荐。"
        )
        messages = [
            {"role": "system", "content": (
                "你是一位专业的时尚购物顾问。用户对你的品牌推荐有疑问或需要调整，"
                "请根据用户的需求友好地调整推荐。请保持专业、亲切的态度，"
                "像闺蜜在聊天一样给出建议。根据用户的职业、收入和风格，给出2-3个调整后的品牌推荐。"
            )},
            {"role": "user", "content": user_content},
        ]

        self.worker = AIWorker(self.ai_client, messages)
        self.worker.result_ready.connect(lambda r: self.ai_response.setText(r))
        self.worker.error_occurred.connect(lambda e: self.ai_response.setText(f"Error: {e}"))
        self.worker.start()


# =============================================================================
# MAIN WINDOW
# =============================================================================

class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.ai_client = None
        self.ai_config = AIConfig()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1200, 800)

        self.load_config()
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Set up the main UI"""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 24, 12, 16)
        sidebar_layout.setSpacing(8)

        # App logo/title
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(12, 0, 0, 0)

        logo_label = QLabel("ChicGuide")
        logo_label.setStyleSheet(f"""
            font-size: 22px;
            font-weight: 700;
            color: {COLORS["primary_dark"]};
        """)
        logo_layout.addWidget(logo_label)
        sidebar_layout.addWidget(logo_widget)

        tagline = QLabel("穿搭顾问")
        tagline.setStyleSheet(f"font-size: 12px; color: {COLORS['text_light']}; padding: 0 12px;")
        sidebar_layout.addWidget(tagline)
        sidebar_layout.addSpacing(24)

        # Navigation buttons
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.nav_buttons = []
        nav_items = [
            ("color", "🎨  四季色卡", "浏览四季色彩灵感"),
            ("outfit", "👗  穿搭顾问", "AI 场景搭配建议"),
            ("brand", "🛍️  品牌指南", "智能品牌推荐"),
        ]

        for key, label, tooltip in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.setProperty("page", key)
            btn.setMinimumHeight(48)
            btn.setStyleSheet(NAV_BUTTON_STYLE)
            btn.clicked.connect(self.on_nav_change)
            self.nav_group.addButton(btn)
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Settings button
        settings_btn = QPushButton("⚙️  API 设置")
        settings_btn.setObjectName("NavButton")
        settings_btn.setStyleSheet(NAV_BUTTON_STYLE)
        settings_btn.setMinimumHeight(44)
        settings_btn.clicked.connect(self.on_settings)
        sidebar_layout.addWidget(settings_btn)

        # Help text
        help_label = QLabel("配置 AI API 后可以使用智能推荐功能")
        help_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_light']}; padding: 4px 12px;")
        help_label.setWordWrap(True)
        sidebar_layout.addWidget(help_label)

        main_layout.addWidget(sidebar)

        # Content area (stacked widget)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {COLORS['bg_main']};")

        # Initialize AI client
        if self.ai_config.api_key:
            self.ai_client = AIClient(self.ai_config)

        # Add subsystems
        self.color_system = ColorCardSubsystem()
        self.outfit_system = OutfitAdvisorSubsystem(ai_client=self.ai_client)
        self.brand_system = BrandRecommendationSubsystem(ai_client=self.ai_client)

        self.stack.addWidget(self.color_system)
        self.stack.addWidget(self.outfit_system)
        self.stack.addWidget(self.brand_system)

        main_layout.addWidget(self.stack, 1)

        # Select first page
        self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

    def on_nav_change(self):
        """Handle navigation change"""
        btn = self.sender()
        page = btn.property("page")

        page_map = {"color": 0, "outfit": 1, "brand": 2}
        self.stack.setCurrentIndex(page_map.get(page, 0))

    def on_settings(self):
        """Open API settings dialog"""
        dialog = APISettingsDialog(self, self.ai_config)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ai_config = dialog.get_config()
            self.save_config()

            # Reinitialize AI client
            if self.ai_config.api_key:
                self.ai_client = AIClient(self.ai_config)
                self.outfit_system.ai_client = self.ai_client
                self.brand_system.ai_client = self.ai_client

                QMessageBox.information(self, "保存成功", "API 设置已保存，你现在可以使用 AI 功能了！")
            else:
                QMessageBox.warning(self, "注意", "你没有输入 API Key，AI 功能将不可用。")

    def apply_styles(self):
        """Apply global styles"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS["bg_main"]};
            }}
            QWidget {{
                font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
            }}
            QToolTip {{
                background-color: white;
                color: {COLORS["text_main"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }}
        """)

    def load_config(self):
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.ai_config = AIConfig(**data)
            except:
                pass

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.ai_config.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"无法保存配置：{e}")

    def closeEvent(self, event):
        """Handle window close"""
        self.save_config()
        event.accept()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    # Set application font
    font = QFont("PingFang SC", 10)
    if not QFontDatabase.hasFamily("PingFang SC"):
        font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    # Set application palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS["bg_main"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS["text_main"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS["bg_card"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS["bg_main"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS["text_main"]))
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS["bg_card"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS["text_main"]))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

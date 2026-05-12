# config.py
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os

load_dotenv()

# =========================================
# TELEGRAM BOT
# =========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================================
# TEMPLATES
# =========================================

TEMPLATES = [

    # =====================================
    # TEMPLATE 1
    # =====================================

    {
        # Имя шаблона
        "name": "thanks_1",

        # PDF шаблон
        "template_pdf": "templates/thanks.pdf",

        # ШРИФТ

        # Внутреннее имя
        "font_name": "Arial",

        # Путь к TTF
        "font_path": "fonts/arialmt.ttf",

        # Размер шрифта
        "font_size": 62,

        # Цвет
        "text_color": "#000000",

        # Межстрочный интервал
        "line_height": 72,

        # ПОЗИЦИЯ ТЕКСТА

        # X центра текста
        "text_center_x": None,

        # Y НИЖНЕЙ строки
        # Блок растёт вверх
        "bottom_y": 1020,
    },

    # =====================================
    # TEMPLATE 2
    # =====================================

    {
        "name": "thanks_2",

        "template_pdf": "templates/thanks2.pdf",

        "font_name": "MontserratBold",
        "font_path": "fonts/Montserrat-Bold.ttf",

        "font_size": 28,
        "line_height": 34,

        "text_center_x": None,
        "text_color": "#fdd22b",

        "bottom_y": 400,
    },
]


# =========================================
# PNG QUALITY
# =========================================

# 1 = минимально
# 2 = нормально
# 3 = хорошо
PNG_SCALE = 2


# =========================================
# LIMITS
# =========================================

MAX_TEXT_LENGTH = 300


# =========================================
# OUTPUT
# =========================================

PDF_OUTPUT_DIR = "output/pdf"

PNG_OUTPUT_DIR = "output/png"


# =========================================
# LOGGING
# =========================================

LOG_LEVEL = "INFO"
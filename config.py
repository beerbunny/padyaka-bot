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
        "name": "thanks_1",

        "template_pdf": "templates/thanks.pdf",

        "font_name": "Arial",
        "font_path": "fonts/arialmt.ttf",

        "font_size": 62,
        "line_height": 72,

        "text_center_x": None,
        "bottom_y": 1020,

        "text_color": "#000000",

        "fake_bold": True,

        # сила утолщения
        "fake_bold_offset": 0.35,
        "letter_spacing": 1.0,
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

        "bottom_y": 435,
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
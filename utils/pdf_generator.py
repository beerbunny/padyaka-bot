# utils/pdf_generator.py
# -*- coding: utf-8 -*-

from io import BytesIO

import fitz

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor

from config import PNG_SCALE


REGISTERED_FONTS = set()


def register_font_once(font_name, font_path):
    if font_name in REGISTERED_FONTS:
        return

    pdfmetrics.registerFont(
        TTFont(font_name, font_path)
    )

    REGISTERED_FONTS.add(font_name)


def split_user_lines(text):
    return [
        line.strip()
        for line in text.strip().splitlines()
        if line.strip()
    ]


def draw_text_with_spacing(
    c,
    text,
    x,
    y,
    font_name,
    font_size,
    letter_spacing=0,
):
    text_width = pdfmetrics.stringWidth(
        text,
        font_name,
        font_size
    )

    extra_spacing = max(len(text) - 1, 0) * letter_spacing

    total_width = text_width + extra_spacing

    current_x = x - (total_width / 2)

    for char in text:
        c.drawString(
            current_x,
            y,
            char
        )

        char_width = pdfmetrics.stringWidth(
            char,
            font_name,
            font_size
        )

        current_x += char_width + letter_spacing


def draw_line(
    c,
    line,
    x,
    y,
    font_name,
    font_size,
    letter_spacing=0,
    fake_bold=False,
    fake_bold_offset=0,
):
    if fake_bold:
        offsets = [
            (0, 0),
            (fake_bold_offset, 0),
            (0, fake_bold_offset),
            (fake_bold_offset, fake_bold_offset),
        ]

        for dx, dy in offsets:
            draw_text_with_spacing(
                c=c,
                text=line,
                x=x + dx,
                y=y + dy,
                font_name=font_name,
                font_size=font_size,
                letter_spacing=letter_spacing,
            )

    else:
        draw_text_with_spacing(
            c=c,
            text=line,
            x=x,
            y=y,
            font_name=font_name,
            font_size=font_size,
            letter_spacing=letter_spacing,
        )


def make_pdf_and_png(
    template_pdf,
    output_pdf,
    output_png,
    text,

    font_name,
    font_path,
    font_size,
    line_height,
    text_color,

    bottom_y,
    text_center_x,

    letter_spacing=0,
    fake_bold=False,
    fake_bold_offset=0,
):
    register_font_once(
        font_name,
        font_path
    )

    reader = PdfReader(template_pdf)
    page = reader.pages[0]

    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    if text_center_x is None:
        text_center_x = page_width / 2

    packet = BytesIO()

    c = canvas.Canvas(
        packet,
        pagesize=(page_width, page_height)
    )

    c.setFont(
        font_name,
        font_size
    )

    c.setFillColor(
        HexColor(text_color)
    )

    lines = split_user_lines(text)

    start_y = bottom_y + (
        (len(lines) - 1) * line_height
    )

    for i, line in enumerate(lines):
        y = start_y - (
            i * line_height
        )

        draw_line(
            c=c,
            line=line,
            x=text_center_x,
            y=y,
            font_name=font_name,
            font_size=font_size,
            letter_spacing=letter_spacing,
            fake_bold=fake_bold,
            fake_bold_offset=fake_bold_offset,
        )

    c.save()

    packet.seek(0)

    overlay = PdfReader(packet)

    page.merge_page(
        overlay.pages[0]
    )

    writer = PdfWriter()
    writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    doc = fitz.open(output_pdf)
    pdf_page = doc[0]

    matrix = fitz.Matrix(
        PNG_SCALE,
        PNG_SCALE
    )

    pix = pdf_page.get_pixmap(
        matrix=matrix,
        alpha=False
    )

    pix.save(output_png)

    doc.close()
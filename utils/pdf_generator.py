# utils/pdf_generator.py
# -*- coding: utf-8 -*-

from io import BytesIO

import fitz

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

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


def make_pdf_and_png(
    template_pdf,
    output_pdf,
    output_png,
    text,

    font_name,
    font_path,
    font_size,
    line_height,

    bottom_y,
    text_center_x,
):

    register_font_once(
        font_name,
        font_path
    )

    reader = PdfReader(template_pdf)

    page = reader.pages[0]

    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    packet = BytesIO()

    c = canvas.Canvas(
        packet,
        pagesize=(page_width, page_height)
    )

    lines = split_user_lines(text)

    start_y = bottom_y + (
        (len(lines) - 1) * line_height
    )

    c.setFont(
        font_name,
        font_size
    )

    for i, line in enumerate(lines):

        y = start_y - (
            i * line_height
        )

        c.drawCentredString(
            text_center_x,
            y,
            line
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

    # PDF -> PNG

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
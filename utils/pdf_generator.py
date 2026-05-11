# -*- coding: utf-8 -*-

from io import BytesIO

import fitz

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from config import (
    FONT_NAME,
    FONT_PATH,
    FONT_SIZE,
    LINE_HEIGHT,
    BOTTOM_Y,
    PNG_SCALE,
)

pdfmetrics.registerFont(
    TTFont(FONT_NAME, FONT_PATH)
)


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
):

    reader = PdfReader(template_pdf)

    page = reader.pages[0]

    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    text_center_x = page_width / 2

    packet = BytesIO()

    c = canvas.Canvas(
        packet,
        pagesize=(page_width, page_height)
    )

    lines = split_user_lines(text)

    start_y = BOTTOM_Y + (
        (len(lines) - 1) * LINE_HEIGHT
    )

    c.setFont(
        FONT_NAME,
        FONT_SIZE
    )

    for i, line in enumerate(lines):

        y = start_y - (
            i * LINE_HEIGHT
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
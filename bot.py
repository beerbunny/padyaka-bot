# bot.py
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import uuid

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from config import (
    BOT_TOKEN,
    TEMPLATES,
    MAX_TEXT_LENGTH,
    PDF_OUTPUT_DIR,
    PNG_OUTPUT_DIR,
)

from utils.cleanup import cleanup_old_files
from utils.pdf_generator import make_pdf_and_png


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def ensure_dirs():
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    os.makedirs(PNG_OUTPUT_DIR, exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    os.makedirs("logs", exist_ok=True)


def normalize_user_text(text: str) -> str:
    lines = [
        line.strip()
        for line in text.strip().splitlines()
        if line.strip()
    ]

    return "\n".join(lines)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Надішліть текст для подяки.\n\n"
        "Рядки збережуться як у повідомленні.\n\n"
        "Приклад:\n"
        "Благодійний фонд\n"
        "Діани Подолянчук"
    )


@dp.message(F.text)
async def handle_text(message: Message):
    user_text = normalize_user_text(message.text)

    if not user_text:
        await message.answer("Текст порожній.")
        return

    if len(user_text) > MAX_TEXT_LENGTH:
        await message.answer(
            f"Текст занадто довгий. Максимум {MAX_TEXT_LENGTH} символів."
        )
        return

    cleanup_old_files(PDF_OUTPUT_DIR)
    cleanup_old_files(PNG_OUTPUT_DIR)

    file_id = uuid.uuid4().hex
    generated_files = []

    try:
        loop = asyncio.get_running_loop()

        # Генерируем шаблоны по очереди, чтобы не душить CPU/RAM.
        for template in TEMPLATES:
            template_name = template["name"]

            output_pdf = os.path.join(
                PDF_OUTPUT_DIR,
                f"{template_name}_{file_id}.pdf"
            )

            output_png = os.path.join(
                PNG_OUTPUT_DIR,
                f"{template_name}_{file_id}.png"
            )

            await loop.run_in_executor(
                None,
                lambda template=template, output_pdf=output_pdf, output_png=output_png: make_pdf_and_png(
                    template_pdf=template["template_pdf"],
                    output_pdf=output_pdf,
                    output_png=output_png,
                    text=user_text,

                    font_name=template["font_name"],
                    font_path=template["font_path"],
                    font_size=template["font_size"],
                    line_height=template["line_height"],
                    text_color=template["text_color"],

                    bottom_y=template["bottom_y"],
                    text_center_x=template["text_center_x"],
                )
            )

            generated_files.append(
                {
                    "template_name": template_name,
                    "pdf": output_pdf,
                    "png": output_png,
                }
            )

        for item in generated_files:
            await message.answer_document(
                FSInputFile(item["pdf"]),
                caption=f"{item['template_name']} PDF готовий."
            )

            await message.answer_document(
                FSInputFile(item["png"]),
                caption=f"{item['template_name']} PNG готовий."
            )

    except Exception as e:
        logging.exception("Generation failed")

        await message.answer(
            "Помилка при генерації файлів.\n\n"
            f"{type(e).__name__}: {e}"
        )


@dp.message()
async def handle_other(message: Message):
    await message.answer(
        "Надішліть саме текст."
    )


async def main():
    ensure_dirs()

    if not BOT_TOKEN or BOT_TOKEN == "TOKEN":
        raise RuntimeError(
            "Встав нормальний BOT_TOKEN у .env. "
            "Бот без токена, на жаль, не телепат."
        )

    if not TEMPLATES:
        raise RuntimeError(
            "У config.py немає жодного шаблону в TEMPLATES."
        )

    for template in TEMPLATES:
        template_pdf = template["template_pdf"]
        font_path = template["font_path"]

        if not os.path.exists(template_pdf):
            raise FileNotFoundError(
                f"Не знайдено шаблон PDF: {template_pdf}"
            )

        if not os.path.exists(font_path):
            raise FileNotFoundError(
                f"Не знайдено шрифт: {font_path}"
            )

    logging.info("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
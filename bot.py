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
    TEMPLATE_PDF,
    MAX_TEXT_LENGTH,
    PDF_OUTPUT_DIR,
    PNG_OUTPUT_DIR,
)

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

    file_id = uuid.uuid4().hex

    output_pdf = os.path.join(
        PDF_OUTPUT_DIR,
        f"thanks_{file_id}.pdf"
    )

    output_png = os.path.join(
        PNG_OUTPUT_DIR,
        f"thanks_{file_id}.png"
    )

    try:
        make_pdf_and_png(
            template_pdf=TEMPLATE_PDF,
            output_pdf=output_pdf,
            output_png=output_png,
            text=user_text,
        )

        await message.answer_document(
            FSInputFile(output_pdf),
            caption="PDF готовий."
        )

        await message.answer_document(
            FSInputFile(output_png),
            caption="PNG готовий."
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
            "Встав нормальний BOT_TOKEN у config.py. "
            "Бот без токена, на жаль, не телепат."
        )

    if not os.path.exists(TEMPLATE_PDF):
        raise FileNotFoundError(
            f"Не знайдено шаблон PDF: {TEMPLATE_PDF}"
        )

    logging.info("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
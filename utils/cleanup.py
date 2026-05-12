# utils/cleanup.py
# -*- coding: utf-8 -*-

import os
import time


MAX_FILE_AGE = 60 * 60 * 24 * 2  # 2 дня


def cleanup_old_files(folder):

    now = time.time()

    if not os.path.exists(folder):
        return

    for filename in os.listdir(folder):

        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            continue

        try:
            file_age = now - os.path.getmtime(filepath)

            if file_age > MAX_FILE_AGE:
                os.remove(filepath)

        except Exception as e:
            print(f"Cleanup error: {filepath}: {e}")
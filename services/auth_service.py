import csv
import os
from config import RC_ROLE_FOLDER

def get_role_from_csv(rc, telegram_id):
    file_path = os.path.join(RC_ROLE_FOLDER, f"{rc}.csv")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue

            csv_telegram_id = row[0].strip()
            role = row[1].strip()

            if csv_telegram_id == str(telegram_id):
                return role

    return None

import os
import shutil
from datetime import datetime


def auto_backup():
    if not os.path.exists("expenses.db"):
        return

    if not os.path.exists("backups"):
        os.makedirs("backups")

    today = datetime.now().strftime("%Y-%m-%d")
    backup_file = f"backups/expenses_backup_{today}.db"

    if not os.path.exists(backup_file):
        shutil.copy2("expenses.db", backup_file)
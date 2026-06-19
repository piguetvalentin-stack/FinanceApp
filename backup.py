import os
import shutil
from datetime import datetime


def auto_backup():
    if not os.path.exists("backups"):
        os.makedirs("backups")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = f"backups/expenses_backup_{timestamp}.db"

    if os.path.exists("expenses.db"):
        shutil.copy2("expenses.db", backup_file)
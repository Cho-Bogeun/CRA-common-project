from pathlib import Path

from mission2.src.user import User

FILE = "attendance_weekday_500.txt"

FILE_ABS_PATH = (Path(__file__).parent / FILE).resolve()

def run():
    users = User.from_record_file(FILE_ABS_PATH)

    for user in users:
        user.evaluate()
        user.print_status()

    print()
    print("Removed player")
    print("==============")
    for removed_user in (u for u in users if u.is_removed()):
        print(removed_user.name)
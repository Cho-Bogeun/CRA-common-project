from enum import Enum
from pathlib import Path

POINT_FOR_SILVER_GRADE = 30

POINT_FOR_GOLD_GRADE = 50

ATTEND_COUNT_FOR_BONUS = 9

BONUS_POINT = 10

FILE = "attendance_weekday_500.txt"

FILE_ABS_PATH = (Path(__file__).parent / FILE).resolve()

NAME2USER_ID = {}
ID_CNT = 0

CNT_ATTEND = [[0] * 100 for _ in range(100)]
POINTS = [0] * 100

NAMES = [''] * 100
CNT_WEDNESDAY_ATTEND = [0] * 100
CNT_WEEKEND_ATTEND = [0] * 100

class AttendDay(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

NORMAL_DAY_NAME_LIST = [d.name for d in (
    AttendDay.monday, AttendDay.tuesday, AttendDay.thursday, AttendDay.friday
)]
WEDNES_DAY_NAME_LIST = [AttendDay.wednesday.name]
WEEKEND_DAY_NAME_LIST = [d.name for d in (AttendDay.saturday, AttendDay.sunday)]
WEEKEND_DAY_INDEX_LIST: list[int] = [AttendDay.saturday.value, AttendDay.sunday.value]

def get_attend_index(attend_day: str) -> int:
    _day_index = -1
    for day in AttendDay:
        if day.name == attend_day:
            _day_index = day.value
            return _day_index

    assert _day_index != -1
    return _day_index

def get_attend_point(attend_day: str) -> int:
    if attend_day in NORMAL_DAY_NAME_LIST:
        return 1
    elif attend_day in WEEKEND_DAY_NAME_LIST:
        return 2
    else:
        return 3

def record_attendance(name, attend_day):
    global ID_CNT

    if name not in NAME2USER_ID:
        ID_CNT += 1
        NAME2USER_ID[name] = ID_CNT
        NAMES[ID_CNT] = name

    user_id = NAME2USER_ID[name]

    attend_point = get_attend_point(attend_day)
    day_index = get_attend_index(attend_day)

    if attend_day in WEDNES_DAY_NAME_LIST:
        CNT_WEDNESDAY_ATTEND[user_id] += 1
    elif attend_day in WEEKEND_DAY_NAME_LIST:
        CNT_WEEKEND_ATTEND[user_id] += 1

    CNT_ATTEND[user_id][day_index] += 1
    POINTS[user_id] += attend_point

class Grade(Enum):
    GOLD = 50
    SILVER = 30
    NORMAL = 0

GRADE = [Grade.NORMAL] * 100

def input_file():
    try:
        with open(FILE_ABS_PATH, encoding='utf-8') as f:
            for line in f.readlines():
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    record_attendance(parts[0], parts[1])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    else:
        update_point_and_grade()

        print("\nRemoved player")
        print("==============")
        print_removed_players()


def print_removed_players():
    for i in range(1, 1+ID_CNT):
        if GRADE[i] not in (Grade.GOLD, Grade.SILVER) and CNT_WEDNESDAY_ATTEND[i] == 0 and CNT_WEEKEND_ATTEND[i] == 0:
            print(NAMES[i])


def update_point_and_grade():
    for i in range(1, 1+ID_CNT):
        if CNT_ATTEND[i][AttendDay.wednesday.value] > ATTEND_COUNT_FOR_BONUS:
            POINTS[i] += BONUS_POINT
        if sum([CNT_ATTEND[i][we_ix] for we_ix in WEEKEND_DAY_INDEX_LIST]) > ATTEND_COUNT_FOR_BONUS:
            POINTS[i] += BONUS_POINT

        if POINTS[i] >= Grade.GOLD.value:
            GRADE[i] = Grade.GOLD
        elif POINTS[i] >= Grade.SILVER.value:
            GRADE[i] = Grade.SILVER
        else:
            GRADE[i] = Grade.NORMAL

        print(f"NAME : {NAMES[i]}, POINT : {POINTS[i]}, GRADE : ", end="")
        print(GRADE[i].name)


if __name__ == "__main__":
    input_file()

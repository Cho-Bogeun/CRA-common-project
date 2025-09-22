from enum import Enum
from pathlib import Path

POINT_FOR_SILVER_GRADE = 30

POINT_FOR_GOLD_GRADE = 50

ATTEND_COUNT_FOR_BONUS = 9

BONUS_POINT = 10

FILE = "attendance_weekday_500.txt"

FILE_ABS_PATH = (Path(__file__).parent / FILE).resolve()

name2user_id = {}
id_cnt = 0

cnt_attend = [[0] * 100 for _ in range(100)]
points = [0] * 100

names = [''] * 100
cnt_wednesday_attend = [0] * 100
cnt_weekend_attend = [0] * 100

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
WEEKEND_DAY_INDEX_LIST: list[int] = [d.value for d in (AttendDay.saturday, AttendDay.sunday)]

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
    global id_cnt

    if name not in name2user_id:
        id_cnt += 1
        name2user_id[name] = id_cnt
        names[id_cnt] = name

    user_id = name2user_id[name]

    attend_point = get_attend_point(attend_day)
    day_index = get_attend_index(attend_day)

    if attend_day in WEDNES_DAY_NAME_LIST:
        cnt_wednesday_attend[user_id] += 1
    elif attend_day in WEEKEND_DAY_NAME_LIST:
        cnt_weekend_attend[user_id] += 1

    cnt_attend[user_id][day_index] += 1
    points[user_id] += attend_point

class Grade(Enum):
    GOLD = 50
    SILVER = 30
    NORMAL = 0

grade = [Grade.NORMAL] * 100

def input_file():
    try:
        with open(FILE_ABS_PATH, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    record_attendance(parts[0], parts[1])

        for i in range(1, id_cnt + 1):
            if cnt_attend[i][AttendDay.wednesday.value] > ATTEND_COUNT_FOR_BONUS:
                points[i] += BONUS_POINT
            if sum([cnt_attend[i][we_ix] for we_ix in WEEKEND_DAY_INDEX_LIST]) > ATTEND_COUNT_FOR_BONUS:
                points[i] += BONUS_POINT

            if points[i] >= Grade.GOLD.value:
                grade[i] = Grade.GOLD
            elif points[i] >= Grade.SILVER.value:
                grade[i] = Grade.SILVER
            else:
                grade[i] = Grade.NORMAL

            print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
            print(grade[i].name)

        print("\nRemoved player")
        print("==============")
        for i in range(1, id_cnt + 1):
            if grade[i] not in (Grade.GOLD, Grade.SILVER) and cnt_wednesday_attend[i] == 0 and cnt_weekend_attend[i] == 0:
                print(names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    input_file()

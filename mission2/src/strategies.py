from abc import ABC, abstractmethod

from mission2.src.type import AttendDay

class PointStrategy(ABC):
    @abstractmethod
    def run(self, attend_day_counter: dict[AttendDay, int]) -> int:...

class DefaultPointStrategy(PointStrategy):
    def run(self, attend_day_counter: dict[AttendDay, int]) -> int:
        point = 0
        for day, count in attend_day_counter.items():
            match day:
                case AttendDay.wednesday:
                    point += count * 3
                case AttendDay.saturday | AttendDay.sunday:
                    point += count * 2
                case _:
                    point += count

        if attend_day_counter[AttendDay.wednesday] >= 10:
            point += 10

        if (attend_day_counter[AttendDay.saturday] +
                attend_day_counter[AttendDay.sunday] >= 10):
            point += 10

        return point

class Grade:
    def __init__(self, name, lower_point = None, upper_point = None):
        self.name = name
        self.lower_point = lower_point
        self.upper_point = upper_point

    def __str__(self):
        return f"{self.name}"

    def does_meet(self, point):
        if self.lower_point is None and self.upper_point is None:
            raise RuntimeError("Should not reach here")
        elif self.lower_point is not None and self.upper_point is None:
            return self.lower_point <= point
        elif self.lower_point is None and self.upper_point is not None:
            return self.upper_point > point
        else:
            return self.lower_point <= point < self.upper_point


GOLD_GRADE = Grade("GOLD", 50)
SILVER_GRADE = Grade("SILVER", 30, 50)
NORMAL_GRADE = Grade("NORMAL", 0, 30)
GRADE_LIST = [GOLD_GRADE, SILVER_GRADE, NORMAL_GRADE]

class RemovalStrategy(ABC):
    @abstractmethod
    def run(self, attend_day_counter: dict[AttendDay, int], grade: Grade) -> bool:...

class DefaultRemovalStrategy(RemovalStrategy):
    def run(self, attend_day_counter: dict[AttendDay, int], grade: Grade) -> bool:
        if grade in [GOLD_GRADE, SILVER_GRADE]:
            return False

        if attend_day_counter[AttendDay.wednesday] != 0:
            return False

        if (attend_day_counter[AttendDay.saturday] != 0
            or attend_day_counter[AttendDay.sunday] != 0):
            return False

        return True

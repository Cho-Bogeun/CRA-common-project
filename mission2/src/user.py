from mission2.src.strategies import DefaultPointStrategy, GRADE_LIST, DefaultRemovalStrategy
from mission2.src.type import AttendDay


class User:
    user_id = 0
    map_name2instance = {}
    instances = []
    @classmethod
    def clear(cls):
        cls.map_name2instance.clear()
        cls.user_id = 0

    @classmethod
    def _user_create_factory(cls, name):
        if name not in cls.map_name2instance:
            cls.user_id += 1
            instance = cls(name, cls.user_id)
            cls.instances.append(instance)
            cls.map_name2instance[name] = instance
        return cls.map_name2instance[name]

    @classmethod
    def from_record_file(cls, record_file):
        try:
            with open(record_file, encoding='utf-8') as f:
                for line in f.readlines():
                    if not line:
                        break
                    parts = line.strip().split()
                    if len(parts) == 2:
                        user = cls._user_create_factory(parts[0])
                        user._attend(parts[1])
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        else:
            return cls.instances

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.point = 0
        self.grade = None

        self._point_strategy = DefaultPointStrategy()
        self._grade_list = GRADE_LIST
        self._remove_strategy = DefaultRemovalStrategy()

        self._attend_day_counter = {
            AttendDay.monday: 0,
            AttendDay.tuesday: 0,
            AttendDay.wednesday: 0,
            AttendDay.thursday: 0,
            AttendDay.friday: 0,
            AttendDay.saturday: 0,
            AttendDay.sunday: 0
        }

    def _attend(self, attend_day: str):
        for day in AttendDay:
            if attend_day == day.name:
                self._attend_day_counter[day] += 1
                return
        raise RuntimeError(f"Should not reach here: {attend_day}")

    def _evaluate_point(self):
        self.point = self._point_strategy.run(self._attend_day_counter)

    def _evaluate_grade(self):
        for grade in self._grade_list:
            if grade.does_meet(self.point):
                self.grade = grade
                return
        raise RuntimeError(f"Should not reach here: {self.point}")

    def evaluate(self):
        self._evaluate_point()
        self._evaluate_grade()

    def print_status(self):
        print(f"NAME : {self.name}, POINT : {self.point}, GRADE : {self.grade}")

    def is_removed(self) -> bool:
        return self._remove_strategy.run(self._attend_day_counter, self.grade)
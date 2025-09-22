import pytest

from mission2.src.type import AttendDay
from mission2.src.user import User

@pytest.fixture(scope="class")
def example_users():

    user1 = User._user_create_factory("One")
    user1._attend("monday")
    user1 = User._user_create_factory("One")
    user1._attend("monday")

    user2 = User._user_create_factory("Two")
    user2._attend("wednesday")

    return (user1, user2)

class TestUser:
    def test_user_id(self, example_users):
        # Arrange, Act
        user1, user2 = example_users

        # Assert
        assert user1.user_id == 1
        assert user2.user_id == 2
        assert User.user_id == 2

    def test_map_name2instance(self, example_users):
        # Arrange, Act
        user1, user2 = example_users

        # Assert
        assert len(User.map_name2instance) == 2
        assert User.map_name2instance[user1.name] is user1
        assert User.map_name2instance[user2.name] is user2

    def test_user_attend_day_counter(self, example_users):
        # Arrange, Act
        user1, user2 = example_users

        # Assert
        assert user1._attend_day_counter[AttendDay.monday] == 2
        assert user2._attend_day_counter[AttendDay.wednesday] == 1

@pytest.fixture(scope="class")
def example_oscar():
    oscar = User._user_create_factory("Oscar")
    oscar._attend("sunday")
    oscar._attend("sunday")
    oscar._attend("tuesday")
    oscar._attend("saturday")
    oscar._attend("monday")
    oscar._attend("tuesday")
    oscar._attend("saturday")
    oscar._attend("thursday")
    oscar._attend("thursday")
    return oscar

class TestOscar:
    def test_point_evaluation(self, example_oscar):
        # Arrange
        oscar = example_oscar

        # Act
        oscar._evaluate_point()

        # Assert
        assert oscar.point == 13

    def test_grade_evaluation(self, example_oscar):
        # Arrange
        oscar = example_oscar
        oscar._evaluate_point()

        # Act
        oscar._evaluate_grade()

        # Assert
        assert oscar.grade.name == "NORMAL"
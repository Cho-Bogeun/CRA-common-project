import pytest

from mission2.src.strategies import Grade


@pytest.mark.parametrize("grade, point", [
    (Grade("GOLD", 50), 70),
    (Grade("SILVER", 30, 50),40),
    (Grade("NORMAL", 0, 30),10),
    (Grade("NOT_YET",None,100),90)
])
def test_does_meat(grade, point):
    # Act
    result = grade.does_meet(point)

    # Assert
    assert result == True
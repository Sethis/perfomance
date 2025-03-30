

import time

from src.common.timer import ContextTimer, PointsCalculator


def test_timing():
    timer = ContextTimer()

    timer.start_point("some")
    timer.end_point("some")

    difference = timer.points[1][2] - timer.points[0][2]

    assert difference >= 0
    assert difference < 0.01


def test_right_timing():
    timer = ContextTimer()

    timer.start_point("some")

    time.sleep(0.5)

    timer.end_point("some")

    difference = timer.points[1][2] - timer.points[0][2]

    assert difference >= 0
    assert 0.499 < difference < 0.502


def test_calculating():
    timer = ContextTimer()

    timer.start_point("some")

    time.sleep(0.5)

    timer.end_point("some")

    timer.start_point("another")

    time.sleep(0.5)

    timer.end_point("another")

    calculator = PointsCalculator(timer=timer, framework="", started_by="")

    some = calculator.calculated_points[0]
    another = calculator.calculated_points[1]

    assert some.name == "some"
    assert another.name == "another"

    assert some.get_difference() >= 0
    assert 0.499 < some.get_difference() < 0.502

    assert another.get_difference() >= 0
    assert 0.499 < another.get_difference() < 0.502

    assert 0.499 < another.started < 0.502

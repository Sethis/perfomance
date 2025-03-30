

import time
import statistics
from typing import Sequence
from dataclasses import dataclass

from pydantic import BaseModel

from src.suits.const import ROUTE_POINT_NAME, RESULTING_POINT_NAME


Point = tuple[str, str, float]


class PointsPydanticModel(BaseModel):
    points: list[Point]
    framework: str
    start_from: str


@dataclass(slots=True, kw_only=True)
class PointsDataclassModel:
    points: list[Point]
    framework: str
    start_from: str


class ContextTimer:
    __slots__ = ("points", "_timer")

    def __init__(self):
        self.points: list[Point] = []
        self._timer = time.time

    def _add_point(self, name: str, as_: str):
        self.points.append((name, as_, self._timer()))

    def start_point(self, name: str):
        self._add_point(name, "start")

    def end_point(self, name: str):
        self._add_point(name, "end")

    def include_points(self, points: list[Point]):
        self.points.extend(points)


@dataclass(slots=True)
class CalculatedPoint:
    name: str
    started: float  # Определяется относительно времени, прошедшего с первого Point
    end: float  # Определяется относительно времени, прошедшего с первого Point

    def get_difference(self) -> float:
        return self.end - self.started


@dataclass(slots=True)
class SummingPointsData:
    all_program_time: float

    mean_route_time: float
    mean_resulting_time: float

    median_route_time: float
    median_resulting_time: float

    framework: str = ""
    started_by: str = ""


class PointsCalculator:
    __slots__ = ("calculated_points", "framework", "started_by")

    def __init__(self, timer: ContextTimer, framework: str, started_by: str):
        self.calculated_points = self._calculate(timer.points)
        self.framework = framework
        self.started_by = started_by

    @staticmethod
    def _calculate(points: list[Point]) -> list[CalculatedPoint]:
        pre_calculated_data: dict[str, dict[str, float]] = {}
        result: list[CalculatedPoint] = []

        minimum = min(points, key=lambda x: x[2])[2]
        # Считаем стартовую точку, чтобы у наших расчётов появилась ось отсчёта

        for point in points:
            if not pre_calculated_data.get(point[0]):
                pre_calculated_data[point[0]] = {}

            pre_calculated_data[point[0]][point[1]] = point[2]

        for name, dirty_data in pre_calculated_data.items():
            point = CalculatedPoint(
                name=name,
                started=dirty_data["start"] - minimum,
                end=dirty_data["end"] - minimum
            )

            result.append(point)

        return result


def summing_data(calculators: Sequence[PointsCalculator]) -> SummingPointsData:
    data: dict[str, list[float]] = {}

    min_start = 0
    max_end = 0

    framework = ""
    started_by = ""

    for calculated in calculators:
        if not framework:
            framework = calculated.framework
            started_by = calculated.started_by

        for point in calculated.calculated_points:
            if point.started < min_start:
                min_start = point.started

            if point.end > max_end:
                max_end = point.end

            arr_data = data.get(point.name, [])
            arr_data.append(point.end - point.started)
            data[point.name] = arr_data

    return SummingPointsData(
        all_program_time=max_end-min_start,
        mean_route_time=statistics.mean(data[ROUTE_POINT_NAME]),
        median_route_time=statistics.median(data[ROUTE_POINT_NAME]),
        mean_resulting_time=statistics.mean(data[RESULTING_POINT_NAME]),
        median_resulting_time=statistics.median(data[RESULTING_POINT_NAME]),
        framework=framework,
        started_by=started_by
    )

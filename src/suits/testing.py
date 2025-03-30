

import asyncio

from aiohttp import ClientSession
from rich.console import Console
from rich.table import Table

from src.common.timer import (
    ContextTimer,
    PointsPydanticModel,
    PointsCalculator,
    summing_data,
    SummingPointsData
)
from src.suits.const import (
    ROUTE_POINT_NAME,
    RESULTING_POINT_NAME,
    PATH_GENERATOR_NUMBER,
    PATH_GENERATOR_NUMBER_SHIFT
)
from src.common.path_generator import path_generator


async def route(path: str, session: ClientSession, backend: str) -> PointsCalculator:
    path = path.replace("{first}", "some")
    path = path.replace("{second}", "100")
    path = f"http://127.0.0.1:8000{path}"

    timer = ContextTimer()
    timer.start_point(ROUTE_POINT_NAME)

    points = PointsPydanticModel(points=timer.points, start_from=backend, framework="asdas")

    async with session.post(path, json=points.model_dump()) as result:
        text = await result.text()

    points = PointsPydanticModel.model_validate_json(text)
    timer = ContextTimer()
    timer.include_points(points=points.points)
    timer.end_point(RESULTING_POINT_NAME)

    return PointsCalculator(timer=timer, started_by=backend, framework=points.framework)


def render(data: list[SummingPointsData]):
    table = Table(title="Benchmark test")

    table.add_column("Counter", style="cyan", justify="center")
    table.add_column("Framework", style="magenta", justify="center")
    table.add_column("Started by", style="magenta", justify="center")
    table.add_column("Program time, s", style="green", justify="center")
    table.add_column("Mean routing, s", style="green", justify="center")
    table.add_column("Median routing, s", style="green", justify="center")
    table.add_column("Mean output, s", style="green", justify="center")
    table.add_column("Median output, s", style="green", justify="center")

    for index, row in enumerate(data):
        table.add_row(
            str(index),
            row.framework,
            row.started_by,
            str(row.all_program_time),
            str(row.mean_route_time),
            str(row.median_route_time),
            str(row.mean_resulting_time),
            str(row.median_resulting_time)
        )

    console = Console()
    console.print(table)


async def run(backend: str) -> SummingPointsData:
    async with ClientSession() as session:
        tasks = []

        for i in range(100):
            for path in path_generator(n=PATH_GENERATOR_NUMBER, n_shift=PATH_GENERATOR_NUMBER_SHIFT):
                tasks.append(route(path=path, session=session, backend=backend))

        results = await asyncio.gather(*tasks)

    return summing_data(results)


async def main():
    results = []

    while True:
        user_text = input(
            "Enter /q or text which server is the starting point. Granian, unicorn, etc"
        )

        if user_text in ("/q", "q", "\\q"):
            render(results)
            print("Good luck!")
            break

        results.append(
            await run(user_text)
        )


asyncio.run(main())

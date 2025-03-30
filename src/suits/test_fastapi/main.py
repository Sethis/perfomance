

from typing import Annotated

from fastapi import FastAPI, Depends

from src.common.database import MemorySessionMaker, AbstractDatabaseInterface
from src.common.path_generator import path_generator
from src.suits.const import (
    PATH_GENERATOR_NUMBER_SHIFT,
    PATH_GENERATOR_NUMBER,
    RESULTING_POINT_NAME,
    ROUTE_POINT_NAME
)
from src.common.timer import PointsPydanticModel, ContextTimer


app = FastAPI()


sessionmaker = MemorySessionMaker()


async def get_database() -> AbstractDatabaseInterface:
    async with sessionmaker as session:
        yield session


for path in path_generator(
    n=PATH_GENERATOR_NUMBER,
    n_shift=PATH_GENERATOR_NUMBER_SHIFT
):
    @app.post(path)
    async def func(
            points: PointsPydanticModel,
            first: str,
            second: int,
            database: Annotated[AbstractDatabaseInterface, Depends(get_database)]
    ) -> PointsPydanticModel:
        timer = ContextTimer()
        timer.include_points(points.points)
        timer.end_point(ROUTE_POINT_NAME)

        await database.set(first, second)

        timer.start_point(RESULTING_POINT_NAME)

        return PointsPydanticModel(
            points=timer.points,
            start_from=points.start_from,
            framework="Fastapi"
        )

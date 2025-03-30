

from typing import AsyncIterable
from contextlib import asynccontextmanager

from litestar import Litestar, post
from litestar.dto import DataclassDTO
from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.base import FromDishka
from dishka.integrations.litestar import inject, LitestarProvider, setup_dishka

from src.common.database import MemorySessionMaker, AbstractDatabaseInterface
from src.common.path_generator import path_generator
from src.suits.const import (
    PATH_GENERATOR_NUMBER_SHIFT,
    PATH_GENERATOR_NUMBER,
    RESULTING_POINT_NAME,
    ROUTE_POINT_NAME
)
from src.common.timer import PointsDataclassModel, ContextTimer


sessionmaker = MemorySessionMaker()


class DatabaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db(self) -> AsyncIterable[AbstractDatabaseInterface]:
        async with sessionmaker as session:
            yield session


routers = []

for path in path_generator(
    n=PATH_GENERATOR_NUMBER,
    n_shift=PATH_GENERATOR_NUMBER_SHIFT,
    str_postfix=":str",
    int_postfix=":int"
):
    @post(
        path,
        dto=DataclassDTO[PointsDataclassModel],
        return_dto=DataclassDTO[PointsDataclassModel]
    )
    @inject
    async def func(
            data: PointsDataclassModel,
            first: str,
            second: int,
            database: FromDishka[AbstractDatabaseInterface]
    ) -> PointsDataclassModel:
        timer = ContextTimer()
        timer.include_points(data.points)
        timer.end_point(ROUTE_POINT_NAME)

        await database.set(first, second)

        timer.start_point(RESULTING_POINT_NAME)

        return PointsDataclassModel(
            points=timer.points,
            start_from=data.start_from,
            framework="Litestar"
        )

    routers.append(func)


@asynccontextmanager
async def lifespan(app: Litestar):
    yield
    await app.state.dishka_container.close()


container = make_async_container(DatabaseProvider(), LitestarProvider())

app = Litestar(route_handlers=routers, lifespan=[lifespan])
setup_dishka(container=container, app=app)

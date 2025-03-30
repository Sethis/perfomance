

from typing import Any

from abc import ABC, abstractmethod


class AbstractDatabaseInterface(ABC):
    @abstractmethod
    async def get(self, name: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def set(self, name: str, value: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()


class MemoryDatabaseInterface(AbstractDatabaseInterface):
    __slots__ = ("_data", )

    def __init__(self):
        self._data = {}

    async def get(self, name: str) -> Any:
        self._data.get(name, None)

    async def set(self, name: str, value: Any) -> None:
        self._data[name] = value

    async def close(self):
        pass


class AbstractSessionMaker(ABC):
    @abstractmethod
    async def __call__(self) -> AbstractDatabaseInterface:
        raise NotImplementedError()

    @abstractmethod
    async def __aenter__(self) -> AbstractDatabaseInterface:
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()


class MemorySessionMaker(AbstractSessionMaker):
    __slots__ = ("_session", )

    def __init__(self):
        self._session = MemoryDatabaseInterface()

    async def __aenter__(self) -> AbstractDatabaseInterface:
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def __call__(self) -> AbstractDatabaseInterface:
        return self._session

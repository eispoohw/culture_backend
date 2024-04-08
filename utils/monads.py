from typing import Any, Generic, TypeVar

_T = TypeVar("_T")


class Maybe(Generic[_T]):
    def __init__(self, value: _T | None):
        self._value = value

    def __getattr__(self, item: Any) -> Any | None:
        if self._value is None:
            return None
        else:
            return getattr(self._value, item)


def mb(value: _T | None) -> Maybe:
    return Maybe(value)

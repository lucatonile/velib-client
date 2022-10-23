from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional


class Cache:
    def __init__(self, ttl: timedelta, getter: Callable[[Any], Any]):
        self._data = dict()
        self._ttl = ttl
        self._getter = getter

    def __getitem__(self, key: Any) -> Any:
        if self._should_refresh_cache():
            self._refresh_cache()

        return self._data["data"][key]

    def _refresh_cache(self):
        self._data = {
            "last_fetch_at": datetime.now(),
            "data": self._getter(),
        }

    def _should_refresh_cache(self) -> bool:
        last_fetch_at: Optional[datetime] = self._data.get(
            "last_fetch_at", None)
        if not last_fetch_at:
            return True

        return datetime.now() - last_fetch_at >= self._ttl

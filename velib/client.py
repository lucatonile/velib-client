from datetime import timedelta
from typing import Any, Dict, List

import requests
from requests.adapters import HTTPAdapter, Retry

from .cache import Cache
from .exceptions import APIException, StationNotFound


class Client:
    def __init__(self: "Client"):
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self.session = (requests
                        .session()
                        .mount('https://', HTTPAdapter(max_retries=retries)))

    def get(self: "Client", url: str) -> Dict[str, Any]:
        try:
            self.session.get(url).json()
        except Exception as e:
            return APIException(e)


class VelibClient(Client):
    base_url = "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole"

    def __init__(
        self: "VelibClient",
    ) -> None:
        self._stations = Cache(timedelta(minutes=30), self._station_getter)
        self._station_statuses = Cache(
            timedelta(seconds=5), self._station_status_getter)

    def _station_getter(self: "VelibClient") -> Dict[str, Any]:
        return self.get(f"{self.base_url}/station_information.json")["data"]

    def _station_status_getter(self: "VelibClient") -> Dict[str, Any]:
        return self.get(f"{self.base_url}/station_status.json")["data"]

    def list_stations(self: "VelibClient") -> List[Dict[str, Any]]:
        return self._stations["stations"]

    def get_station(self: "VelibClient", id=None, name=None) -> Dict[str, Any]:
        try:
            return next(s for s in self._stations["stations"] if s["station_id"] == id or s["name"] == name)
        except StopIteration:
            raise StationNotFound

    def get_station_status(self: "VelibClient", id: int) -> Dict[str, Any]:
        try:
            return next(s for s in self._station_statuses["stations"] if s["station_id"] == id)
        except StopIteration:
            raise StationNotFound

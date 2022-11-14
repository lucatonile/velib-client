from http import HTTPStatus
import pytest
import requests_mock
from typing import Iterator

from velib import VelibClient, StationNotFound


velib_station_information = {
    "stations": [
        {
            "station_id": 1,
            "name": "Gare du Nord",
            "lat": 48.83,
            "lon": 2.225,
            "capacity": 35,
            "stationCode": "1"
        },
        {
            "station_id": 2,
            "name": "Concorde",
            "lat": 18.83,
            "lon": 13.225,
            "capacity": 5,
            "stationCode": "2"
        },
    ]
}

velib_station_status = {
    "stations": [
        {
            "station_id": 1,
            "stationCode": "1234",
            "num_bikes_available": 2,
            "numBikesAvailable": 2,
            "num_bikes_available_types": [
                {"mechanical": 2}, {"ebike": 0}
            ],
            "num_docks_available": 32,
            "numDocksAvailable": 32,
            "is_installed": 1,
            "is_returning": 1,
            "is_renting": 1,
            "last_reported": 1668124660
        }
    ]
}


base_url = "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole"


@pytest.fixture(autouse=True)
def adapter() -> Iterator[requests_mock.Adapter]:
    with requests_mock.mock() as adapter:
        adapter.register_uri(
            "GET",
            f"{base_url}/station_information.json",
            json={"data": velib_station_information},
            status_code=HTTPStatus.OK
        )

        adapter.register_uri(
            "GET",
            f"{base_url}/station_status.json",
            json={"data": velib_station_status},
            status_code=HTTPStatus.OK
        )

        yield adapter


def test_client__list_stations():
    assert VelibClient().list_stations(
    ) == velib_station_information["stations"]


def test_client__get_station():
    c = VelibClient()

    assert c.get_station(id=1) == velib_station_information["stations"][0]
    assert c.get_station(
        name="Gare du Nord"
    ) == velib_station_information["stations"][0]

    assert c.get_station(id=2) == velib_station_information["stations"][1]
    assert c.get_station(
        name="Concorde"
    ) == velib_station_information["stations"][1]


def test_client__get_station_station_not_found():
    c = VelibClient()

    with pytest.raises(StationNotFound):
        c.get_station(id=-1)
    with pytest.raises(StationNotFound):
        c.get_station(name="asdf")
    with pytest.raises(StationNotFound):
        c.get_station()


def test_client__get_station_status():
    c = VelibClient()
    assert c.get_station_status(id=1) == velib_station_status["stations"][0]


def test_client__get_station_status_not_found():
    with pytest.raises(StationNotFound):
        VelibClient().get_station_status(id=-1)

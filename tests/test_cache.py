from datetime import datetime, timedelta
from mock import Mock
from freezegun import freeze_time

from velib.cache import Cache


def test_refresh_cache() -> None:
    getter = Mock(return_value={
        "some": "thing"
    })

    cache = Cache(timedelta(hours=1), getter)

    assert cache["some"] == "thing"
    getter.assert_called_once()

    assert cache["some"] == "thing"
    getter.assert_called_once()

    with freeze_time(datetime.now() + timedelta(hours=2)):
        assert cache["some"] == "thing"
        assert getter.call_count == 2

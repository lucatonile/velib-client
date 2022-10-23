class VelibClientException(Exception):
    """VelibClient base exception"""


class StationNotFound(VelibClientException):
    """Queried station was not found"""


class APIException(VelibClientException):
    """An exception coming from the API"""

from typing import IO, Any, Dict, Optional, Union
from urllib.request import urlopen

import yaml

from .lazy import LazySchema
from .schemas import BaseSchema, OpenApi30, SwaggerV20
from .types import Filter, PathLike
from .utils import NOT_SET, deprecated, get_base_url


def from_path(
    path: PathLike, base_url: Optional[str] = None, method: Optional[Filter] = None, endpoint: Optional[Filter] = None
) -> BaseSchema:
    """Load a file from OS path and parse to schema instance.."""
    with open(path) as fd:
        return from_file(fd, base_url=base_url, method=method, endpoint=endpoint)


def from_uri(
    uri: str, base_url: Optional[str] = None, method: Optional[Filter] = None, endpoint: Optional[Filter] = None
) -> BaseSchema:
    """Load a remote resource and parse to schema instance."""
    response = urlopen(uri)
    data = response.read()
    if base_url is None:
        base_url = get_base_url(uri)
    return from_file(data, base_url=base_url, method=method, endpoint=endpoint)


def from_file(
    file: Union[IO[str], str],
    base_url: Optional[str] = None,
    method: Optional[Filter] = None,
    endpoint: Optional[Filter] = None,
) -> BaseSchema:
    """Load a file content and parse to schema instance.

    `file` could be a file descriptor, string or bytes.
    """
    raw = yaml.safe_load(file)
    return from_dict(raw, base_url=base_url, method=method, endpoint=endpoint)


def from_dict(
    raw_schema: Dict[str, Any],
    base_url: Optional[str] = None,
    method: Optional[Filter] = None,
    endpoint: Optional[Filter] = None,
) -> BaseSchema:
    """Get a proper abstraction for the given raw schema."""
    if "swagger" in raw_schema:
        return SwaggerV20(raw_schema, base_url=base_url, method=method, endpoint=endpoint)

    if "openapi" in raw_schema:
        return OpenApi30(raw_schema, base_url=base_url, method=method, endpoint=endpoint)
    raise ValueError("Unsupported schema type")


def from_pytest_fixture(
    fixture_name: str, method: Optional[Filter] = NOT_SET, endpoint: Optional[Filter] = NOT_SET
) -> LazySchema:
    """Needed for a consistent library API."""
    return LazySchema(fixture_name, method=method, endpoint=endpoint)


# Backward compatibility
class Parametrizer:
    from_path = deprecated(from_path, "`Parametrizer.from_path` is deprecated, use `schemathesis.from_path` instead.")
    from_uri = deprecated(from_uri, "`Parametrizer.from_uri` is deprecated, use `schemathesis.from_uri` instead.")

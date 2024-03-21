"""Configuration handling class."""

import dataclasses
import logging
import os
import sys
from typing import Dict, Any, List, Optional

import yaml


class Error(Exception):
    """Base Exception handling class."""


class ConfigFileNotFoundError(Error):
    """File could not be found on disk."""


WG_ALLOWLIST_OS_ENV = "WGKEX_ALLOWLIST_FILE"
WG_ALLOWLIST_DEFAULT_LOCATION = "/etc/allowlist.yaml"


@dataclasses.dataclass
class Allowlist:
    """A representation of the Allowlist file.

    Attributes:
        allowlist: The list of wireguard public keys.
    """

    allowlist: List[str]

    @classmethod
    def from_dict(cls, cfg: Dict[str, Any]) -> "Allowlist":
        """Creates a Allowlist object from a configuration file.
        Arguments:
            cfg: The configuration file as a dict.
        Returns:
            A Config object.
        """
        
        return cls(
            allowlist=cfg["allowlist"]
        )

    def get(self, key: str) -> Any:
        """Get the value of key from the raw dict representation of the config file"""
        return self.raw.get(key)


_parsed_allowlist: Optional[Allowlist] = None


def get_pubkeys() -> Allowlist:
    """Returns a parsed Allowlist object.

    Raises:
        AllowlistFileNotFoundError: If we could not find the configuration file on disk.
    Returns:
        The Allowlist representation of the config file
    """
    global _parsed_allowlist
    if _parsedallowlist is None:
        cfg_contents = fetch_allowlist_from_disk()
        try:
            allowlist = yaml.safe_load(cfg_contents)
        except yaml.YAMLError as e:
            print("Failed to load YAML file: %s" % e)
            sys.exit(1)
        try:
            allowlist = Allowlist.from_dict(allowlist)
        except (KeyError, TypeError, AttributeError) as e:
            print("Failed to lint file: %s" % e)
            sys.exit(2)
        _parsed_allowlist = allowlist
    return _parsed_allowlist


def fetch_allowlist_from_disk() -> str:
    """Fetches allowlist file from disk and returns as string.

    Raises:
        allowlistFileNotFoundError: If we could not find the configuration file on disk.
    Returns:
        The file contents as string.
    """
    allowlist_file = os.environ.get(WG_ALLOWLIST_OS_ENV, WG_ALLOWLIST_DEFAULT_LOCATION)
    logging.debug("getting allowlist_file: %s", repr(allowlist_file))
    try:
        with open(allowlist_file, "r") as stream:
            return stream.read()
    except FileNotFoundError as e:
        raise AllowlistFileNotFoundError(
            f"Could not locate allowlist file in {allowlist_file}"
        ) from e

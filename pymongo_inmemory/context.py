from configparser import ConfigParser
import hashlib
import logging
import os
from os import path
import platform

from ._utils import make_semver, mkdir_ifnot_exist
from .downloader._urls import best_url

DEFAULT_CONF = {}
CACHE_FOLDER = path.join(path.dirname(__file__), "..", ".cache")

logger = logging.getLogger("PYMONGOIM_UTILS")


class OperatingSystemNotFound(ValueError):
    pass


def _coercion(constructor, value):
    pass


def _check_environment_vars(option, fallback=None):
    "Check if `option` is defined in environment variables"
    pass


def _check_cfg(option, filename, fallback=None):
    "Check if `option` is defined in `filename` ini file in the root folder"
    pass


def conf(option, fallback=None, optional=True, coerce_with=str):
    """Retrieve asked `option` if possible. There are number of places that are checked.
    In the order of precedence,
    1. Environment variables
    2. setup.cfg in the root folder
    3. pymongo_inmemory.ini in the root folder
    4. `DEFAULT_CONF`

    Root folder is where the Python interpreter is invoked.

    Environment variables should be prefixed with `PYMONGOIM__`. For instance,
    `PYMONGOIM__DOWNLOAD_FOLDER`.

    Parameters
    ----------
    option: str
        Asked option

    Returns
    -------
    any or None: If there is a value, it'll return it otherwise it'll return `None`.
    """
    pass


class Context:
    def __init__(
        self, os_name=None, version=None, os_ver=None, ignore_cache=False
    ) -> None:
        self.mongo_version = conf("mongo_version", version)
        self.mongod_port = conf("mongod_port", None, coerce_with=int)
        self.mongod_data_folder = conf("mongod_data_folder", None)
        self.dbname = conf("dbname", "pimtest")
        self.mongo_client_host = conf("mongo_client_host", None)

        self.operating_system = self._build_operating_system_info(os_name)
        self.os_version = conf("os_version", os_ver)

        # For now order of the following line is important
        self.downloaded_version = None
        self.download_url = conf("download_url", self._build_download_url())

        self.url_hash = hashlib.sha256(bytes(self.download_url, "utf-8")).hexdigest()

        self.ignore_cache = conf("ignore_cache", ignore_cache, coerce_with=bool)
        self.use_local_mongod = conf("use_local_mongod", False, coerce_with=bool)

        self.download_folder = conf(
            "download_folder", mkdir_ifnot_exist(CACHE_FOLDER, "download")
        )
        self.extract_folder = conf(
            "extract_folder", mkdir_ifnot_exist(CACHE_FOLDER, "extract")
        )
        self.archive_folder = mkdir_ifnot_exist(self.download_folder, self.url_hash)
        self.extracted_folder = mkdir_ifnot_exist(self.extract_folder, self.url_hash)
        self.storage_engine = self._build_storage_engine()

    def __str__(self):
        return (
            f"Mongo Version {self.mongo_version}\n"
            f"MongoD Port {self.mongod_port}\n"
            f"MongoD Data Folder {self.mongod_data_folder}\n"
            f"Database Name {self.dbname}\n"
            f"OS Name {self.operating_system}\n"
            f"OS Version {self.os_version}\n"
            f"Download URL {self.download_url}\n"
            f"URL Hash {self.url_hash}\n"
            f"Download Version {self.downloaded_version}\n"
            f"Ignore Cache {self.ignore_cache}\n"
            f"Use Local MongoD {self.use_local_mongod}\n"
            f"Download Folder {self.download_folder}\n"
            f"Extract Folder {self.extract_folder}\n"
            f"Storage engine {self.storage_engine}\n"
        )

    def _build_operating_system_info(self, os_name=None):
        pass

    def _build_download_url(self):
        pass

    def _build_storage_engine(self):
        pass

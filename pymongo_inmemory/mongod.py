"""MongoDB daemon process wrapper

This module can be used for spinning up an ephemeral MongoDB instance:
::
    python -m python_inmemory.mongod
"""
import atexit
import logging
import os
import signal
import subprocess
import time
import threading
from tempfile import TemporaryDirectory

import pymongo

from ._utils import find_open_port
from .downloader import download
from .context import Context

logger = logging.getLogger("PYMONGOIM_MONGOD")
# Holds references to open Popen objects which spawn MongoDB daemons.
_popen_objs = []


@atexit.register
def cleanup():
    logger.info("Cleaning created processes.")
    for o in _popen_objs:
        if o.poll() is None:
            logger.debug("Found {}".format(o.pid))
            o.terminate()


def clean_before_kill(signum, stack):
    pass


# as per https://docs.python.org/3.6/library/signal.html#signals-and-threads
# only the main thread is allowed to set a new signal handler.
# This means that if this module is imported by a thread other than the
# main one it will raise an error.
if threading.current_thread() is threading.main_thread():
    signal.signal(signal.SIGTERM, clean_before_kill)


class MongodConfig:
    def __init__(self, pim_context: Context):
        self._pim_context = pim_context
        self.local_address = "127.0.0.1"
        self.engine = pim_context.storage_engine

    @property
    def port(self):
        pass

    @property
    def connection_string(self):
        pass


class Mongod:
    """Wrapper for MongoDB daemon instance. Can be used with context managers.
    During contruction it calls `download` function of `downloader` to get the
    defined MongoDB version.

    Daemon is managed by `subprocess.Popen`. all Popen objects are registered
    with `atexit` module to ensure clean up.
    """

    def __init__(self, pim_context: Context):
        self._pim_context = Context() if pim_context is None else pim_context
        logger.info("Running MongoD in the following context")
        logger.info(self._pim_context)

        logger.info("Checking binary")
        if self._pim_context.use_local_mongod:
            logger.warn("Using local mongod instance")
            self._bin_folder = ""
        else:
            self._bin_folder = download(self._pim_context)

        self._proc = None
        self._connection_string = None

        self.config = MongodConfig(self._pim_context)

        self._temp_data_folder = TemporaryDirectory(prefix="pymongoim")
        self._using_tmp_folder = self._pim_context.mongod_data_folder is None

        self._client = pymongo.MongoClient(self.connection_string)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        pass

    def stop(self):
        logger.info("Sending kill signal to mongod.")
        self._proc.terminate()
        while self._proc.poll() is None:
            logger.debug("Waiting for MongoD shutdown.")
            time.sleep(1)
        self._clean_up()

    @property
    def data_folder(self):
        pass

    @property
    def connection_string(self):
        pass

    @property
    def is_locked(self):
        pass

    @property
    def is_healthy(self):
        pass

    def mongodump(self, database, collection):
        pass

    def logs(self):
        pass

    def _clean_up(self):
        if self._using_tmp_folder:
            self._temp_data_folder.cleanup()

    def _check_lock(self):
        pass


if __name__ == "__main__":
    # This part is used for integrity tests too.
    logging.basicConfig(level=logging.DEBUG)
    context = Context()
    with Mongod(context) as md:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass

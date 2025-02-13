"""Provides a class to manage output and input files for the pipeline"""

from logging import getLogger
from pathlib import Path
from typing import Dict, Any
from enum import Enum

_log = getLogger(__name__)


class FileManager:
    """Manages directories for input and output. The main purpose is to hold a series of
    paths that intermediate files. These paths can be stored using a key of any type, but
    the DirectoryType enumeration is provided to identify the normal intermediate results
    steps for the pipeline. """
    def __init__(self, root_path: Path) -> None:
        """ Constructs a FileManager linked to a single root path.

        :param root_path: the root path that all directories will be made relative to.
        :type root_path: pathlib.Path
        """
        self._root_path = root_path
        self._directories: Dict[Any, Path] = {}

    def get_directory(self, key: Any) -> Path:
        """Get a stored directory from the file manager.

        :param key: the identification key for the directory.
        :returns: `pathlib.Path` to the directory.
        :raises: `KeyError` if the key does not exist (handled by the underlying `Dict`)
        """
        return self._directories[key]
    
    def register_directory(self, key: Any, path: Path, exist_ok: bool = True, suppress_warning = False) -> Path:
        """Register a directory with the filemanager. If the path does not exist, create
        the directory. If `exist_ok` is `True` (default), will raise a warning if the 
        directory already exists but not an error.
        
        :param key: the identification key to store the directory under.
        :param path: the `pathlib.Path` to the directory to store.
        :param exist_ok: if `True` (default) will only raise a warning if the directory already
            exists.
        :raises: `RuntimeError` if `exist_ok` is set to `False` and the directory already
            exists.
        :returns: the `pathlib.Path` to the newly stored directory.
        """
        _log.debug('Registering directory {}'.format(path))
        if not path.exists():
            _log.debug('Directory not found, making directory')
            path.mkdir(parents=True, exist_ok=True)
        else:
            if exist_ok:
                if not suppress_warning:
                    _log.warning('Directory already exists, existing data may be overwritten!')
            else:
                _log.error('Directory already exists.')
                raise RuntimeError
        self._directories[key] = path
        return path


    def make_directory(self, key: Any, name: str, exist_ok: bool = True) -> Path:
        """Make a directory using a string as a name instead of registering a `pathlib.Path` directly.
        
        :param key: the identification key to store the directory under.
        :param name: the name of the directory to make.
        :param exist_ok: if `True` (default) will only raise a warning if the directory already
            exists.
        :raises: `RuntimeError` if `exist_ok` is set to `False` and the directory already
            exists.
        :returns: the `pathlib.Path` to the newly stored directory.
        """
        return self.register_directory(key, self._root_path / name, exist_ok)

    @property
    def root_path(self) -> Path:
        """The root path of the file manager."""
        return self._root_path
    
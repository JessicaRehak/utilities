from logging import getLogger
from pathlib import Path
import os

_log = getLogger(__name__)

def check_exists(path: Path, name: str = 'File') -> Path:
    """Check existance of a path and return it. The return is so that it can be used iomatically as:
    
    my_path = check_exists(Path('path/to/check'))

    :param path: path to check
    :type path: Path
    :param name: name of the file, only for loggin, defaults to 'File'
    :type name: str, optional
    :return: path that has been existance checked
    :rtype: Path
    """
    path = path.resolve()
    if not path.exists():
        _log.error("{} not found at {}, path does not exist".format(name, path))
        raise(FileNotFoundError)
    _log.debug("{} found at {}".format(name, path))
    return path

def move_to_directory(input_path: Path, output_directory: Path) -> None:
    """Move a specified path to a directory. The name after moving will be the same as in the origin.

    :param input_path: path of the object to move.
    :type input_path: Path
    :param output_directory: output directory to move the object to.
    :type output_directory: Path
    """
    _log.debug('Moving {} to {}'.format(input_path.name, output_directory))
    if not input_path.exists():
        _log.error('Input file {} does not exist'.format(input_path))
    elif not output_directory.exists():
        _log.error('Output directory {} does not exist'.format(output_directory))
    os.rename(input_path, output_directory / input_path.name)

def link(input_path: Path, output_path: Path) -> None:
    """Link a path to an output path. Will return without linking if a correct symlink already exists.

    :param input_path: path to link from.
    :type input_path: Path
    :param output_path: path to link to.
    :type output_path: Path
    :raises FileNotFoundError: Input file is not found.
    :raises FileExistsError: output_path already exists or, if a symlink, points to a different target.
    """
    _log.debug('Symlinking {} to {}'.format(input_path, output_path))
    if not input_path.exists():
        _log.error('Input file {} does not exist'.format(input_path))
        raise FileNotFoundError
    if output_path.exists():
        if output_path.is_symlink():
            _log.debug('Symlink already exists to {}'.format(output_path.readlink()))
            if output_path.readlink() == input_path:
                _log.debug('Correct symlink already exists, skipping.')
                return
            else:
                _log.error('Symlink already exists to a different file, please delete or resolve.')
            raise FileExistsError
        else:
            _log.error(f'File already exists at {output_path}')
    os.symlink(input_path, output_path)
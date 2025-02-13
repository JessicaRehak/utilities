from logging import getLogger
from pathlib import Path
import multiprocessing
import subprocess
from typing import List, Any

_log = getLogger(__name__)

def run_pool(args: List[List[str]], cwd: Path) -> str:
    _log.debug('Pooling {} calls'.format(len(args)))
    def run(args: List[str]):
        return run_command(args, cwd)
    p = multiprocessing.Pool()
    p.map(run, args)
    

def run_command(args: List[str | Any], cwd: Path, *, check_return_code: bool = True) -> str:
    """Runs a subprocess command. With the arguments provided in a list of strings or
    objects that can be converted to strings. Optionally checks the return code to raise
    an error. 

    :param args: A list of binary and arguments. See the documentation for `subprocess.SubprocessError` for specifics.
    :type args: List[str  |  Any]
    :param cwd: Location to run the command.
    :type cwd: Path
    :param check_return_code: If True, raises an error if the subprocess does not return 0, defaults to True
    :type check_return_code: bool, optional
    :raises subprocess.SubprocessError: If check_return_code is True and the subprocess does not return 0
    :return: the output of the command, decoded to utf-8, or the raw output if that fails.
    :rtype: str
    """
    if not all(isinstance(i, str) for i in args):
        args = [str(v) for v in args]
    _log.debug('Running command {} at {}'.format(' '.join(args), cwd))
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd) as proc:
        try:
            output = proc.stdout.read().decode("utf-8")
            error = proc.stderr.read().decode("utf-8")
        except UnicodeDecodeError:
            output = proc.stdout.read()
            error = proc.stderr.read()
        return_code = proc.wait()
        _log.debug('Process finished with code {}'.format(return_code))
        if check_return_code and return_code != 0:
            _log.error("Command error running {}: {}".format(args[0], error))
            raise subprocess.SubprocessError
    return output

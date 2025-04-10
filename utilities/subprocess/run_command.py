from logging import getLogger
from pathlib import Path
import multiprocessing
import subprocess
from typing import List, Any, Optional

_log = getLogger(__name__)

def run_pool(args: List[List[str]], cwd: Path) -> str:
    _log.debug('Pooling {} calls'.format(len(args)))
    def run(args: List[str]):
        return run_command(args, cwd)
    p = multiprocessing.Pool()
    p.map(run, args)
    

def run_command(args: List[str | Any], cwd: Path, *, check_return_code: bool = True, 
                print_output_to_debug: bool = False,
                run_in_shell: bool = False,
                input_file: Optional[Path] = None,
                capture_output: bool = False) -> int | tuple[int, bytes]:
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
    if input_file is not None:
        _log.debug('With input file: {}'.format(input_file))
        infile = open(input_file, 'r')
    else:
        infile = None
    try:
        process = subprocess.Popen(args, 
                                   stdout=subprocess.PIPE if print_output_to_debug or capture_output else None, 
                                   stderr=subprocess.PIPE, 
                                   cwd=cwd, 
                                   text=False, 
                                   shell=run_in_shell, stdin=infile)

        stdout, stderr = process.communicate()
        if print_output_to_debug and stdout is not None:
            for line in stdout.decode('utf-8', errors="replace").splitlines():
                _log.debug(line)
        return_code = process.returncode
        _log.debug('Process finished with code {}'.format(return_code))

        if check_return_code and return_code != 0:
            error_msg = stderr.decode("utf-8", errors="replace") if stderr else "<no error output>"
            _log.error("Command error running {}: {}".format(args[0], error_msg))
            raise subprocess.SubprocessError
        
        if capture_output:
            return return_code, stdout
        return return_code
    finally:
        if infile is not None:
            infile.close()
        

import sys
import subprocess
from run_tests import get_python_path

if __name__ == '__main__':
    python: str = get_python_path()
    caos: str = "from caos.cli import cli_entry_point; cli_entry_point()"
    execute_caos: subprocess.CompletedProcess = subprocess.run(
        [python, "-c", caos] + sys.argv
    )
    exit(execute_caos.returncode)
import os
import re
import sys


def supports_color() -> bool:
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    supported_platform = sys.platform != 'Pocket PC' and (sys.platform != 'win32' or 'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() # isatty is not always implemented, #6223.
    return supported_platform and is_a_tty


def escape_ansi(line) -> str:
    """
    Returns a string without ansi color codes
    """
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)




import os
import sys


def supports_color() -> bool:
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    supported_platform = sys.platform != 'Pocket PC' and (sys.platform != 'win32' or 'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() # isatty is not always implemented, #6223.
    return supported_platform and is_a_tty




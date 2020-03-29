"""
DO NOT TOUCH
    This script imports all the modules available that start with the word 'command'
"""

import pkgutil as _pkgutil
from typing import List

available_commands: List[str] = []
_search_path: List[str] = ['caos/cli_commands/']


_module_info: _pkgutil.ModuleInfo
for _module_info in _pkgutil.iter_modules(path=_search_path):
    module_name: str = _module_info.name

    if module_name.startswith("command"):
        available_commands.append(module_name)

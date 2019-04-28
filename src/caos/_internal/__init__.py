""" This module provides the logic for the different command line arguments of caos"""

import src.caos._internal.init as init
import src.caos._internal.prepare as prepare
import src.caos._internal.test as test
import src.caos._internal.run  as run
import src.caos._internal.templates as templates

__all__ = ["init", "prepare", "test", "run" , "templates"]



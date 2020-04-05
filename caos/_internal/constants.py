from enum import Enum

CAOS_YAML_FILE_NAME = "caos.yml"


class ValidDependencyVersionRegex(Enum):
    MAJOR_MINOR_PATCH = r"^(\^|\~)?(\d+\.)(\d+\.)(\d+)$"  # (^| ~) X.X.X
    MAJOR_MINOR = r"^(\^|\~)?(\d+\.)(\d+)$"  # (^| ~) X.X
    MAJOR = r"^(\^|\~)?(\d+)$"  # (^| ~) X
    LATEST = r"^(latest|LATEST)$"  # latest or LATEST
    WHL = r"^(.+)(\.whl|\.WHL)$"  # Anything.whl or Anything.WHL

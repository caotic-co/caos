class UnsupportedOS(Exception):
    pass


class OpenCaosFileException(Exception):
    pass


class InvalidCaosFileFormat(Exception):
    pass


class MissingKeyInYamlFile(Exception):
    pass


class WrongKeyTypeInYamlFile(Exception):
    pass


class InvalidDependencyVersionFormat(Exception):
    pass


class UnexpectedError(Exception):
    pass
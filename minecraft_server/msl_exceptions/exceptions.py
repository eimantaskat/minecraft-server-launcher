class InvalidResponseStatusError(Exception):
    def __init__(self, message):
        self.message = message


class DownloadUrlDoesNotExistError(Exception):
    def __init__(self, message):
        self.message = message


class FileDownloadError(Exception):
    def __init__(self, message):
        self.message = message

class IncorrectServerVersion(Exception):
    def __init__(self, message):
        self.message = message

class JarNotFound(Exception):
    def __init__(self, message):
        self.message = message
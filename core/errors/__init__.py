from disnake.ext.commands import CheckFailure


class NoOwnGuild(CheckFailure):
    '''An exception is raised when used outside of one's own guild.

    This inherits from :exc:`CheckFailure`
    '''

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or 'It cannot be used outside of your own guild.')

class CompileError(Exception):
    def __init__(self, original: Exception) -> None:
        super().__init__(original)

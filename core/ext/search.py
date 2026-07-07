import os
import pkgutil
from typing import Iterator


def search_extensions(path: str) -> Iterator[str]:
    """Walk through a directory and yield all modules.

    Parameters
    ----------
    path: :class:`str`
        The path to search for modules

    Yields
    ------
    :class:`str`
        The name of the found module. (usable in load_extension)
    """
    relpath = os.path.relpath(path)  # relative and normalized
    if ".." in relpath:
        msg = "Modules outside the cwd require a package to be specified"
        raise ValueError(msg)

    abspath = os.path.abspath(path)
    if not os.path.exists(relpath):
        msg = f"Provided path '{abspath}' does not exist"
        raise ValueError(msg)
    if not os.path.isdir(relpath):
        msg = f"Provided path '{abspath}' is not a directory"
        raise ValueError(msg)

    prefix = relpath.replace(os.sep, ".")
    if prefix in ("", "."):
        prefix = ""
    else:
        prefix += "."

    for _, name, ispkg in pkgutil.iter_modules([path]):
        if not ispkg: continue
        yield prefix + name
        yield from search_extensions(os.path.join(path, name))

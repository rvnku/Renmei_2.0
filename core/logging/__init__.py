import logging
from rich.logging import RichHandler


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)-15s %(message)s",
        handlers=[RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=False,
            tracebacks_extra_lines=0,
            tracebacks_width=120,
            markup=True,
            show_time=True,
            show_level=True,
            show_path=False,
        )]
    )
    logging.getLogger('disnake.gateway').setLevel(logging.WARNING)

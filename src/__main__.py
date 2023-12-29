import logging

import coloredlogs

coloredlogs.install(
    fmt="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.DEBUG,
)
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
#     datefmt="%Y/%m/%d %H:%M:%S",
# )

from .perfecter_sfinder import SolutionFinderJava
from .perfecter_sfinder.types import Drop, Hold, Kicks

a = SolutionFinderJava()
a.percent(
    """
XXXXXX____
XXXXXX____
XXXXXX____
XXXXXX____
XXXXXX____
XXXXXX____
XXXXXXXX__
XXXXXXXX__
""",
    "*p4",
    "v115@9gE8DeG8CeH8BeG8CeA8JeAgH",
)

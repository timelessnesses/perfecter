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

from .perfecter_sfinder import SolutionFinderJava as SolutionFinder

# import logging
logging.getLogger("Perfecter.src.perfecter_sfinder.SolutionFinderJava").setLevel(
    logging.NOTSET
)

SolutionFinder()
# print("hello!!!")

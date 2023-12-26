"""
Perfecter - SFinder lib
"""

import logging
import os
import pathlib
import subprocess
import sys


def init_log():
    formatting = logging.Formatter(
        "[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s"
    )

    log = logging.getLogger("Perfecter.src.perfecter_sfinder.SolutionFinderJava")
    log.setLevel(logging.DEBUG)

    try:
        os.mkdir("logs")
    except:
        pass
    with open(
        str(pathlib.Path(__file__).parent.resolve())
        + "/../../logs/perfecter_sfinder_sfj.log",
        "w",
    ) as fp:
        fp.write("")

    logf = logging.FileHandler(
        str(pathlib.Path(__file__).parent.resolve())
        + "/../../logs/perfecter_sfinder_sfj.log",
        "w",
    )
    logf.setFormatter(formatting)
    log.addHandler(logf)
    # yes = logging.StreamHandler(sys.stdout)
    # yes.setFormatter(formatting)
    # log.addHandler(yes)
    return log


log = init_log()
log.info("hi")


class SolutionFinderJava:
    """
    SolutionFinder - A class that wraps and parses solution-finder
    ONLY supporting Java version right now...
    """

    executable_path = (
        str(pathlib.Path(__file__).parent.resolve()) + "/../../bin/sfinder_JAVA"
    )
    execution_line = "java -jar {path} {args}"
    cwd = executable_path
    logger = log

    def __init__(self) -> None:
        self.logger.debug("SolutionFinderJava initialized")
        self.logger.debug(f"Execution Path: {self.executable_path}")
        self.logger.debug(
            f"Execution line: {self.execution_line.format(path=self.executable_path, args='bla bla bla')}"
        )
        self.run_command("-h")

    def run_command(self, args: list[str] | str) -> subprocess.CompletedProcess:
        # sanitized = self.sanitize() # sanitization :3
        return subprocess.run(
            [
                *self.execution_line.format(
                    path=self.executable_path + "/sfinder.jar",
                    args=args if isinstance(args, str) else " ".join(args),
                ).split(" ")
            ]
        )

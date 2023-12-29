"""
Perfecter - SFinder lib
"""

import copy
import logging
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import psutil

from .output_parser import PercentParser
from .types import Drop, Hold, Kicks


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
# log.info("hi")


class SolutionFinderJava:
    """
    SolutionFinder - A class that wraps and parses solution-finder
    ONLY supporting Java version right now...
    """

    executable_path = (
        str(pathlib.Path(__file__).parent.resolve()) + "/../../bin/sfinder_JAVA/"
    )
    jar_file = executable_path + "sfinder.jar"
    execution_line = ["java", "-jar", "{path}"]
    cwd = executable_path
    logger = log
    VERSION: str
    USABLE_THREADS = (
        psutil.cpu_count(logical=False) * 2
    ) // 2  # get half usable threads instead

    def __init__(self) -> None:
        self.logger.debug("SolutionFinderJava initialized")
        self.logger.debug(f"Execution Path: {self.executable_path}")
        # self.logger.debug(
        #     f"Execution line: {self.converted('-h')}"
        # )
        self.VERSION = (
            self.run_command("-v").stdout.decode("utf-8").replace("Version:", "")
        )
        self.logger.info(f"sfinder.jar version: {self.VERSION}")

    def run_command(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        """
        Do NOT call this function directly.
        This function's purpose is to run commands on the
        """
        # sanitized = self.sanitize() # sanitization :3
        return subprocess.run(
            self.converted(*args),
            capture_output=True,
            cwd=self.executable_path,
            # stdout=subprocess.PIPE
        )

    def converted(self, *args: str) -> list[str]:
        """
        Helper method for building command
        """
        copied = copy.copy(self.execution_line)
        copied[2] = copied[2].format(path=self.jar_file)
        copied.extend(args)
        return copied

    def percent(
        self,
        field: str,
        patterns: str,
        tetfu: str,
        clear_line: int = 4,
        drop: Drop = Drop.SOFT,
        failedcount: int = 100,
        hold: Hold = Hold.USE,
        kicks: Kicks = Kicks.SRS,
        page: int = 1,
        tree_depth: int = 3,
    ) -> PercentParser:
        path = self.write_field(field)
        output = self.run_command(
            "percent",
            "-c",
            str(clear_line),
            "-d",
            drop.value,
            "-fc",
            str(failedcount),
            "-fp",
            path.name,
            "-H",
            hold.value,
            "-K",
            kicks.value,
            "-P",
            str(page),
            "-t",
            tetfu,
            "-td",
            str(tree_depth),
            "-th",
            str(self.USABLE_THREADS),
            "-p",
            patterns,
        )
        path.close()
        return PercentParser.parser(output.stdout.decode())

    def write_field(self, field: str) -> "tempfile._TemporaryFileWrapper[str]":
        fp = tempfile.NamedTemporaryFile("w")
        fp.write(field)
        return fp

import abc
import typing_extensions
import typing
import dataclasses
from .types import Hold, Kicks, Drop
import re
import logging
class BaseParser(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def parser(cls, text: str) -> typing_extensions.Self:
        raise NotImplementedError()

@dataclasses.dataclass()
class Config:
    max_clear_lines: int
    using_hold: Hold
    kicks: Kicks
    drop: Drop
    searching_pattern: str

@dataclasses.dataclass()
class SystemInformation:
    threads: int
    version: str
    necessary_pieces: int

@dataclasses.dataclass()
class EnumeratingPieces:
    piece_pop_count: int
    duplicate_pattern_searching_size: int
    not_duplicated_pattern_searching_size: int

@dataclasses.dataclass()
class Search:
    average_time_ms: int
    counts: int

@dataclasses.dataclass()
class SuccessPatternTree:
    tree: dict[str, float | dict[str, float]]
    head_pieces: int

@dataclasses.dataclass()
class FailedPattern:
    patterns: list[list[str]]
    max: int

@dataclasses.dataclass()
class Output:
    success: float
    success_out_of: tuple[int,int]
    success_pattern_tree: SuccessPatternTree
    failed_pattern: FailedPattern

class PercentParser(BaseParser):
    """
    Parsed percent data
    """
    setup_field: list[str]
    config: Config
    system_info: SystemInformation
    enumerating_pieces: EnumeratingPieces
    search: Search
    output: Output
    original: str
    __logger = logging.getLogger("Perfecter.src.perfecter_sfinder.output_parser.PercentParser")

    @classmethod
    def parser(cls, text: str) -> typing_extensions.Self:
        thing = cls()

        setup_field_raw = text.split("# Setup Field\n")[1].split("# Initialize / User-defined\n")[0]
        config_raw = text.split("# Initialize / User-defined\n")[1].split("# Initialize / System\n")[0]
        system_info_raw = text.split("# Initialize / System\n")[1].split("# Enumerate pieces\n")[0]
        enumerating_pieces_raw = text.split("# Enumerate pieces\n")[1].split("# Search\n")[0]
        search_raw = text.split("# Search\n")[1].split("# Output\n")[0]
        output_raw = text.split("# Output\n")[1].replace("\n# Finalize\ndone\n","")

        # cls.__logger.debug(text)
        # cls.__logger.debug(setup_field_raw)
        # cls.__logger.debug(config_raw)
        # cls.__logger.debug(system_info_raw)
        # cls.__logger.debug(enumerating_pieces_raw)
        # cls.__logger.debug(search_raw)
        # cls.__logger.debug(output_raw)


        return thing
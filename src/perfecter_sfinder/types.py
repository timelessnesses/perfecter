import enum

class Drop(enum.Enum):
    HARD = "hard"
    SOFT = "soft"

class Hold(enum.Enum):
    USE = "use"
    AVOID = "avoid"

class Kicks(enum.Enum):
    NO_KICKS = "nokicks"
    NULLPOMINO180 = "nullpomino180"
    SRS = "srs"
    # maybe srs+ and srs-x?
import argparse
import enum
import logging
import os
import shutil
import subprocess
import zipfile

import coloredlogs
import requests

# coloredlogs.install()
coloredlogs.install(
    fmt="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

formatting = logging.Formatter("[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s")
logging.basicConfig(
    level=logging.NOTSET,
    format="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

log = logging.getLogger("Perfecter.Initialize")
log.setLevel(logging.NOTSET)

try:
    os.mkdir("logs")
except:
    pass
try:
    os.mkdir("bin")
except:
    pass

with open("logs/initializer.log", "w") as fp:
    fp.write("")

logf = logging.FileHandler("logs/initializer.log", "w")
logf.setFormatter(formatting)
log.addHandler(logf)


def build(selected: "SolutionFinderTypes") -> None:
    name = f"sfinder_{selected.name}"
    log.debug(f"Building Folder {name}")
    if selected == SolutionFinderTypes.CPP:
        # os.chdir(name + "/build")
        log.info("Building with CMake")
        subprocess.run(
            ["cmake", ".."],
            check=True,
            # shell=True,
            # capture_output=True,
            cwd=f"./{name}/build",
        )
        log.info("Done building with CMake")
        log.info("Continuing the work with GNU Make")
        subprocess.run(
            ["make", "main"],
            check=True,
            # shell=True,
            cwd=f"./{name}/build",
        )
        log.info("Done building everything!")
        log.info("Moving files")
        shutil.move(f"./{name}/build/bin/main", "./bin/sfinder_cpp")
        try:
            shutil.move(f"./{name}/build/bin/libsfinder.so", "./bin/libsfinder.so")
            log.debug("Moved linux shared library")
        except:
            log.debug("Failed to move linux shared library")
            pass
        try:
            shutil.move(f"./{name}/build/bin/libsfinder.dll", "./bin/libsfinder.dll")
            log.debug("Moved windows shared library")
        except:
            log.debug("Failed to move windows shared library")
            pass
        log.debug("Cleanup")
        shutil.rmtree(name)
    elif selected == SolutionFinderTypes.JAVA:
        log.debug("Finding assets that doesn't have GUI tag in it")
        for e in requests.get(
            "https://api.github.com/repos/knewjade/solution-finder/releases/latest"
        ).json()["assets"]:
            if "gui" in e["name"].lower():
                continue
            log.debug("Found one!")
            log.info("Downloading the file through wget")
            subprocess.run(["wget", e["browser_download_url"], "-O", "sfinder.zip"])
            log.info("Decompressing with zipfile")
            with zipfile.ZipFile("./sfinder.zip", "r") as fp:
                try:
                    shutil.rmtree("./bin/" + name)
                    log.debug("Removed previous binary folder")
                except:
                    log.debug(
                        "Failed to remove previous binary folder. (Maybe it doesn't exists)"
                    )
                    pass
                log.debug("Creating new folder")
                os.mkdir("./bin/" + name)
                log.debug("Extracting data")
                fp.extractall(f"./bin/{name}")
            log.debug("Cleanup")
            os.remove("./sfinder.zip")


class SolutionFinderTypes(enum.Enum):
    JAVA = "https://github.com/knewjade/solution-finder"
    CPP = "https://github.com/timelessnesses/sfinder-cpp"  # fork


parser = argparse.ArgumentParser(description="An initializer setting up for SFinder.")

parser.add_argument("-java", action="store_true")
parser.add_argument("-cpp", action="store_true")

parsed = parser.parse_args()

selected: SolutionFinderTypes = SolutionFinderTypes.JAVA  # defaulting this

if parsed.java:
    selected = SolutionFinderTypes.JAVA
elif parsed.cpp:
    selected = SolutionFinderTypes.CPP

log.info(f"Selected {selected}")
log.info(
    "Cloning repository through git..."
) if selected == SolutionFinderTypes.CPP else log.info("Downloading JAR file")

g = (
    subprocess.run(  # TODO: what the FUCK is going on
        [
            "git",
            "clone",
            selected.value,
            "--depth",
            "1",
            "--recurse-submodules",
            # "-j8"
            f"sfinder_{selected.name}",
        ],
        # shell=True,
        # # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        # capture_output=True,
        # stdout=subprocess.STDOUT
    )
    if selected != SolutionFinderTypes.JAVA
    else None
)

if g and g.returncode != 0:
    log.warn(
        "Non 0 exit code. Concerning. Probably existing file, recommended you to delete it to update to new version!"
    )

log.info("Completed")
log.info("Building the target")
build(selected)

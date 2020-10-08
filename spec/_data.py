import sys
from pathlib import Path

# inserting current dir where votm package exists
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from votm import __version__

# locations
BASE_DIR = Path(__file__).resolve().parents[1]
BASE_DIR_ABS = str(BASE_DIR)
PKG_DIR = BASE_DIR.joinpath("votm")
ASSETS_DIR = PKG_DIR.joinpath("assets")
LICENSE_FILE = BASE_DIR.joinpath("LICENSE")
# data
LICENSE_FILE = [
    (
        str(LICENSE_FILE.relative_to(BASE_DIR)),
        ".\\" + str(LICENSE_FILE.relative_to(BASE_DIR)),
        "DATA",
    )
]
DATA_FILES = {
    str(i.relative_to(ASSETS_DIR)): (
        str(i.relative_to(BASE_DIR)),
        ".\\" + str(i.relative_to(BASE_DIR)),
        "DATA",
    )
    for i in ASSETS_DIR.iterdir()
}
DATA_FILES[LICENSE_FILE[0][1].strip(".\\")] = LICENSE_FILE[0]
ICON_PATH = str(PKG_DIR.resolve().joinpath("assets/v_r.ico"))
DATA_FILES_ALL = list(DATA_FILES.values())
# cleanup
del LICENSE_FILE, ASSETS_DIR

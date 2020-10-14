import os
import pathlib
from platform import system

_resource_dir = "assets"
_data_dir = "votm-data"

PKG_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = PKG_DIR.parent
LICNESE_PATH = ROOT_DIR.joinpath("LICENSE")
ASSETS_PATH = PKG_DIR.joinpath(_resource_dir)
DATA_PATH = None
if system().lower() == "windows":
    DATA_PATH = pathlib.Path(os.getenv("ALLUSERSPROFILE")).joinpath(_data_dir)
else:
    DATA_PATH = pathlib.Path(os.path.expanduser("~")).joinpath(".{}".format(_data_dir))

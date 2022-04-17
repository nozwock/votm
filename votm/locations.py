import os
import pathlib
from appdirs import AppDirs

_resource_dir = "assets"
_appname = "votm"
_author_alias = "nozwock"

# if hasattr(sys, "frozen") -> if bundled/packaged
# sys.executable -> path for executable
# sys._MEIPASS -> path for bundled dir
# sys.prefix -> path for python installation. If bundled -> bundled dir location

PKG_DIR = pathlib.Path(__file__).resolve().parent
# ROOT_DIR = PKG_DIR.parent
# LICNESE_PATH = ROOT_DIR.joinpath("LICENSE")
ASSETS_PATH = PKG_DIR.joinpath(_resource_dir)
DATA_PATH = pathlib.Path(AppDirs(_appname, _author_alias).user_data_dir)

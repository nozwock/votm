import pathlib

PKG_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = PKG_DIR.parent
LICNESE_PATH = ROOT_DIR.joinpath("LICENSE")
ASSETS_PATH = PKG_DIR.joinpath("assets")

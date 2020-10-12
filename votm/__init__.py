from . import locations

__author__ = "Sagar Kumar"
__version__ = "1.1.1b0"
with open(locations.LICNESE_PATH, "r") as f:
    __license__ = f.read()

from . import core
from . import utils

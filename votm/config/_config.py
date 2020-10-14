import os
import toml
from pathlib import Path
from typing import Optional

from votm.utils.extras import hashTextSHA256
from votm.locations import DATA_PATH


BASE_CONFIG = {
    "config": {
        "security": {
            "passwd": "%s" % hashTextSHA256(""),
            "key": "%s" % hashTextSHA256(""),
        }
    }
}
CANDIDATE_CONFIG = {
    "config": {
        "candidate": {
            "['HeadBoy', 'HB']": [],
            "['ViceHeadBoy', 'VHB']": [],
            "['HeadGirl', 'HG']": [],
            "['ViceHeadGirl', 'VHG']": [],
        }
    }
}
CLASS_CONFIG = {
    "config": {
        "class": {
            "6": ["A", "B", "C", "D"],
            "7": ["A", "B", "C", "D"],
            "8": ["A", "B", "C", "D"],
            "9": ["A", "B", "C", "D"],
            "10": ["A", "B", "C", "D"],
            "11": ["A", "B", "C", "D"],
            "12": ["A", "B", "C", "D"],
        }
    }
}


class Config:
    CONFIG_FILE = "config.toml"
    CONFIG_PATH = Path(DATA_PATH).joinpath(CONFIG_FILE)
    _heads = {
        "security": BASE_CONFIG,
        "candidate": CANDIDATE_CONFIG,
        "class": CLASS_CONFIG,
    }

    def __init__(self):
        return

    def write_default(self, cfg_head: Optional[str] = None) -> bool:
        if not DATA_PATH.is_dir():
            DATA_PATH.mkdir()
        if not self._check_integrity():
            with open(self.CONFIG_PATH, "w") as fl:
                toml.dump(BASE_CONFIG, fl)
                toml.dump(CANDIDATE_CONFIG, fl)
                toml.dump(CLASS_CONFIG, fl)
                return 1

        if cfg_head is not None:
            if cfg_head not in list(self._heads.keys()):
                raise KeyError
            cfg_dict = self.load()
            with open(self.CONFIG_PATH, "w") as fl:
                for head in self._heads.items():
                    if cfg_head == head[0]:
                        cfg_dict["config"][head[0]] = head[1]["config"][head[0]]
                        toml.dump(cfg_dict, fl)
                        break
        return 0

    def write(self, cfg_head: str, provided_cfg: dict) -> None:
        cfg_dict = self.load()
        with open(self.CONFIG_PATH, "w") as fl:
            if cfg_head not in list(self._heads.keys()):
                raise KeyError
            if cfg_head == list(self._heads.keys())[2]:
                # * "class"
                cfg_dict["config"][cfg_head] = {
                    str(x): y for x, y in (i for i in provided_cfg.items())
                }
            else:
                cfg_dict["config"][cfg_head] = provided_cfg
            toml.dump(cfg_dict, fl)

    def load(self, cfg_head: Optional[str] = None) -> dict:
        with open(self.CONFIG_PATH, "r") as fl:
            self.cfg_dict = toml.load(fl)

        self.get_security = self.cfg_dict["config"]["security"]
        self.get_candidate = self.cfg_dict["config"]["candidate"]
        self.get_class = {
            int(x): y for x, y in (i for i in self.cfg_dict["config"]["class"].items())
        }

        if cfg_head is not None:
            _heads = list(self._heads.keys())
            if cfg_head not in _heads:
                raise KeyError
            if cfg_head == _heads[0]:
                return self.get_security
            elif cfg_head == _heads[1]:
                return self.get_candidate
            else:
                return self.get_class

        return self.cfg_dict

    def _check_integrity(self) -> bool:
        if not self.CONFIG_PATH.is_file():
            return False
        with open(self.CONFIG_PATH, "r") as fl:
            get = None
            try:
                get = toml.load(fl)
            except toml.TomlDecodeError:
                return False
            # trying to fetch data
            try:
                get = get["config"]
                _heads = list(self._heads.keys())
                for _ in _heads:
                    get[_]
            except KeyError:
                return False
            #!TODO: Use regex for further checks
            return True

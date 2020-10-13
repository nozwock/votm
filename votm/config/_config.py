import os
from ast import literal_eval
from platform import system

from votm.utils.extras import (
    hashTextSHA256,
    matchHashedTextSHA256,
    Base64encode,
    Base64decode,
)
from .env import ENV_KEY, SECRET_KEY


class Default_Config:
    """Contains Default configurations for the application."""

    BASE_CONFIG = "{'passwd' : '%s', 'key': '%s'}" % (
        hashTextSHA256(""),
        hashTextSHA256(""),
    )
    CANDIDATE_CONFIG = "{\"['HeadBoy', 'HB']\" : [], \"['ViceHeadBoy', 'VHB']\" : [], \"['HeadGirl', 'HG']\" : [], \"['ViceHeadGirl', 'VHG']\" : []}"
    CLASS_CONFIG = "{6 : ['A', 'B', 'C', 'D'], 7 : ['A', 'B', 'C', 'D'], 8 : ['A', 'B', 'C', 'D'], 9 : ['A', 'B', 'C', 'D'], 10 : ['A', 'B', 'C', 'D'], 11 : ['A', 'B', 'C', 'D'], 12 : ['A', 'B', 'C', 'D']}"


class Write_Default:
    """Writes Default config file which doesn't exist already, in the /ProgramData directory."""

    exist = 0
    loc = None
    if system().lower() == "windows":
        loc = os.path.join(os.getenv("ALLUSERSPROFILE"), "votm-data")
    else:
        loc = os.path.join(os.path.expanduser("~"), ".votm-data")
    #! temp: adding a pswrd.vcon for saving password
    #! later shift all to toml file format
    fles = ["cand.vcon", "clss.vcon", "pswrd.vcon"]

    def __init__(self):
        Write_Default.exist = 0
        if not os.path.exists(Write_Default.loc):
            os.mkdir(Write_Default.loc)
        eval_lst = [
            os.path.exists(os.path.join(Write_Default.loc, f)) == False
            for f in Write_Default.fles
        ]

        # try:
        #    self.reg.get(SECRET_KEY)
        # except FileNotFoundError:
        #    Write_Default.exist = 1
        #    self.reg.setx(SECRET_KEY, self.rand(16))

        if any(eval_lst):
            Write_Default.exist = 1
            j = 0
            for i in eval_lst:
                if i is True:
                    if j is 0:
                        self.wrt_cand()
                    elif j is 1:
                        self.wrt_clss()
                    else:
                        self.wrt_pswrd()
                j += 1

        # try:
        #    self.reg.get(ENV_KEY)
        # except FileNotFoundError:
        #    Write_Default.exist = 1
        #    self.reg.setx(
        #        ENV_KEY,
        #        self.crypt.encrypt(
        #            Default_Config.BASE_CONFIG, self.reg.get(SECRET_KEY)
        #        ),
        #    )
        #    self.reg.close()

    @staticmethod
    def rand(
        size=8,
        chars=__import__("string").ascii_letters + __import__("string").digits + "@#$&",
    ):
        return "".join(__import__("random").choice(chars) for _ in range(size))

    def wrt_cand(self):
        """Writes Candidate file."""
        with open(os.path.join(Write_Default.loc, Write_Default.fles[0]), "w") as f:
            f.write(Default_Config.CANDIDATE_CONFIG)

    def wrt_clss(self):
        """Writes Class&Sec file."""
        with open(os.path.join(Write_Default.loc, Write_Default.fles[1]), "w") as f:
            f.write(Default_Config.CLASS_CONFIG)

    def wrt_pswrd(self):
        with open(os.path.join(Write_Default.loc, Write_Default.fles[2]), "w") as f:
            f.write(Default_Config.BASE_CONFIG)


def write_config(fle: int, cfg):
    """Writes to config. files."""
    with open(os.path.join(Write_Default.loc, Write_Default.fles[fle]), "w") as f:
        f.write(str(cfg))
        f.flush()


class Access_Config:
    """Access config files located in the /roaming directory."""

    def __init__(self):
        loc = Write_Default.loc
        fles = Write_Default.fles
        with open(os.path.join(loc, fles[0]), "r") as f:
            cand_str = f.read()
        with open(os.path.join(loc, fles[1]), "r") as f:
            clss_str = f.read()
        with open(os.path.join(loc, fles[2]), "r") as f:
            bse_str = f.read()

        self.bse_config = literal_eval(bse_str)
        self.cand_config = literal_eval(cand_str)
        self.clss_config = literal_eval(clss_str)

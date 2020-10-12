import os
from platform import system

from votm.utils.extras import Reg, Crypt
from .env import ENV_KEY, SECRET_KEY


class Default_Config:
    """Contains Default configurations for the application."""

    BASE_CONFIG = "{'passwd' : '', 'key': ''}"
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
    fles = ["cand.vcon", "clss.vcon"]

    def __init__(self):
        Write_Default.exist = 0
        self.crypt = Crypt()
        self.reg = Reg()
        if not os.path.exists(Write_Default.loc):
            os.mkdir(Write_Default.loc)
        eval_lst = [
            os.path.exists(os.path.join(Write_Default.loc, f)) == False
            for f in Write_Default.fles
        ]

        try:
            self.reg.get(SECRET_KEY)
        except FileNotFoundError:
            Write_Default.exist = 1
            self.reg.setx(SECRET_KEY, self.rand(16))

        if any(eval_lst):
            Write_Default.exist = 1
            j = 0
            for i in eval_lst:
                if i is True:
                    if j is 0:
                        self.wrt_cand()
                    else:
                        self.wrt_clss()
                j += 1

        try:
            self.reg.get(ENV_KEY)
        except FileNotFoundError:
            Write_Default.exist = 1
            self.reg.setx(
                ENV_KEY,
                self.crypt.encrypt(
                    Default_Config.BASE_CONFIG, self.reg.get(SECRET_KEY)
                ),
            )
            self.reg.close()

    @staticmethod
    def rand(
        size=8,
        chars=__import__("string").ascii_letters + __import__("string").digits + "@#$&",
    ):
        return "".join(__import__("random").choice(chars) for _ in range(size))

    def wrt_cand(self):
        """Writes Candidate file."""
        with open(os.path.join(Write_Default.loc, Write_Default.fles[0]), "w") as f:
            f.write(
                self.reg.get(SECRET_KEY)
                + self.crypt.encrypt(
                    Default_Config.CANDIDATE_CONFIG, self.reg.get(SECRET_KEY)
                )
            )

    def wrt_clss(self):
        """Writes Class&Sec file."""
        with open(os.path.join(Write_Default.loc, Write_Default.fles[1]), "w") as f:
            f.write(
                self.reg.get(SECRET_KEY)
                + self.crypt.encrypt(
                    Default_Config.CLASS_CONFIG, self.reg.get(SECRET_KEY)
                )
            )


def write_config(fle: int, cfg: str):
    """Writes to config. files."""
    with open(os.path.join(Write_Default.loc, Write_Default.fles[fle]), "w") as f:
        cfg = Reg().get(SECRET_KEY) + Crypt().encrypt(str(cfg), Reg().get(SECRET_KEY))
        f.write(cfg)
        f.flush()


class Access_Config:
    """Access config files located in the /roaming directory."""

    def __init__(self):
        loc = Write_Default.loc
        fles = Write_Default.fles
        self.crypt = Crypt()
        self.reg = Reg()
        bse_str = self.reg.get(ENV_KEY)
        bse_str = self.crypt.decrypt(bse_str, self.reg.get(SECRET_KEY))
        with open(os.path.join(loc, fles[0]), "r") as f:
            cand_str = f.read()
            cand_str = self.crypt.decrypt(cand_str[16:], cand_str[:16])
        with open(os.path.join(loc, fles[1]), "r") as f:
            clss_str = f.read()
            clss_str = self.crypt.decrypt(clss_str[16:], clss_str[:16])

        self.bse_config = eval(bse_str)
        self.cand_config = eval(cand_str)
        self.clss_config = eval(clss_str)

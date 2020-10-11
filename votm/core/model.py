"""
Copyright (C) 2019 Sagar Kumar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or 
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from random import choice
from string import digits
from platform import system
from tkinter import messagebox as mg

from votm.utils.extras import Reg, Crypt
from ._config import SECRET_KEY, ENV_KEY


class Tokens:
    """Handles Tokens generation, saving and to get a specific token."""

    if system().lower() == "windows":
        LOC = os.path.join(os.getenv("ALLUSERSPROFILE"), "votm-data")
    else:
        LOC = os.path.join(os.path.expanduser("~"), ".votm-data")
    FL = "tkn.vcon"
    TPath = os.path.join(LOC, FL)

    def __init__(self, master, entries=None):
        self.master = master
        self.crypt = Crypt()
        self.reg = Reg()

        if entries != None:
            try:
                self.entries = int(entries)
                mg.showwarning(
                    "Voting Master",
                    "The previous Tokens are about to be overwriiten if exists.",
                    parent=master,
                )
            except:
                mg.showerror("Error", "Input is not valid.", parent=master)
                raise ValueError("Invalid Input")

    def gen(self):
        def key_gen(size=8, chars=digits):
            with open(Tokens.TPath, "r") as f:
                try:
                    self.tkn_read = eval(f.read())
                    self.tkn_read = self.crypt.decrypt(
                        str(self.tkn_read), self.reg.get(SECRET_KEY)
                    )
                except:
                    self.tkn_read = []

            key = "".join(choice(chars) for _ in range(size))
            if key not in self.tkn_read:
                return key
            else:
                return None

        try:
            with open(Tokens.TPath, "w") as f:
                tkn = []
                for _ in range(self.entries):
                    val = key_gen()
                    if val is not None:
                        tkn.append(val)
                tkn = self.crypt.encrypt(str(tkn), self.reg.get(SECRET_KEY))
                f.write(f"{tkn}")
            mg.showinfo(
                "Voting Master",
                f"{self.entries} Token(s) Generated.",
                parent=self.master,
            )
        except:
            pass

    def get(self, val: str):
        with open(Tokens.TPath, "r") as f:
            tkn_lst = eval(self.crypt.decrypt(str(f.read()), self.reg.get(SECRET_KEY)))
        try:
            ind = tkn_lst.index(val)
            del tkn_lst[ind]
            with open(Tokens.TPath, "w") as f:
                tkn_lst = self.crypt.encrypt(str(tkn_lst), self.reg.get(SECRET_KEY))
                f.write(str(tkn_lst))
            return True
        except:
            mg.showwarning(
                "Error", "The Key is either wrong or has been used.", parent=self.master
            )
            return False

    def check(self):
        try:
            with open(Tokens.TPath, "r") as f:
                tkn_lst = f.read()
                tkn_lst = eval(
                    self.crypt.decrypt(str(tkn_lst), self.reg.get(SECRET_KEY))
                )
            if len(tkn_lst) == 0:
                mg.showerror(
                    "Error", "No Tokens in the Token file.", parent=self.master
                )
                return False
        except:
            mg.showerror("Error", "Token file doesn't exists!", parent=self.master)
            return False

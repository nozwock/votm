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

import uuid
import hashlib
from collections import OrderedDict
from base64 import b64encode, b64decode

import os
from random import choice
from string import digits
from platform import system
from tkinter import messagebox as mg

from votm.locations import DATA_PATH


class Tokens:
    """Handles Tokens generation, saving and to get a specific token."""

    FL = "tkn.vcon"
    TPath = DATA_PATH.joinpath(FL)

    def __init__(self, master, entries=None):
        self.master = master

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
            tkn_lst = eval(f.read())
        try:
            ind = tkn_lst.index(val)
            del tkn_lst[ind]
            with open(Tokens.TPath, "w") as f:
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
                tkn_lst = eval(tkn_lst)
            if len(tkn_lst) == 0:
                mg.showerror(
                    "Error", "No Tokens in the Token file.", parent=self.master
                )
                return False
        except:
            mg.showerror("Error", "Token file doesn't exists!", parent=self.master)
            return False


def Base64encode(text: str) -> str:
    return b64encode(text.encode("ascii")).decode("ascii")


def Base64decode(ctext: str) -> str:
    return b64decode(ctext.encode("ascii")).decode("ascii")


def hashTextSHA256(text: str) -> str:
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + salt


def matchHashedTextSHA256(hashedText: str, providedText: str) -> bool:
    _hashedText, salt = hashedText[:-32], hashedText[-32:]
    return (
        _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()
    )


class Dicto:
    """A Class for creating ordered dictionaries."""

    def __init__(self, _dict):
        self.state = OrderedDict(_dict)
        self.dict = OrderedDict(_dict)

    def insert(self, pos, key, val):
        self.dict = OrderedDict()
        keys = list(dict(self.state).keys())
        if pos >= 0:
            flag = 0
            for i in range(len(dict(self.state))):
                try:
                    if keys[i] == keys[pos]:
                        pos = keys[i]
                        break
                except:
                    flag = 1
                    pos = keys[-1]
                    break
        else:
            flag = 1
            for i in range(-1, -len(dict(self.state)) - 1, -1):
                if keys[i] == keys[pos]:
                    pos = keys[i]
                    break
        for k, v in dict(self.state).items():
            if flag == 0:
                if k == pos:
                    self.dict[key] = val
                self.dict[k] = v
            else:
                self.dict[k] = v
                if k == pos:
                    self.dict[key] = val
        del self.state
        self.state = self.dict
        return self.dict

    def remove(self, key):
        self.dict = dict(self.state)
        try:
            del self.dict[key]
            del self.state
            self.state = self.dict
            return OrderedDict(self.dict)
        except:
            print("Error, No such key exists.")

    def get(self):
        return dict(self.state)

    def __repr__(self):
        return repr(dict(self.state))

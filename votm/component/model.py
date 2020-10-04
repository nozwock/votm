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
import sys
from random import choice
from string import digits
from platform import system
from tkinter import messagebox as mg
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.tools import Reg, Crypt
from utils.etc import SECRET_KEY, ENV_KEY


class Tokens:
    """Handles Tokens generation, saving and to get a specific token."""
    if system().lower()=='windows':
    	LOC = os.path.join(os.getenv('ALLUSERSPROFILE'),'votm-data')
    else:
   		LOC = os.path.join(os.path.expanduser('~'),'.votm-data')
    FL = 'tkn.vcon'
    TPath = os.path.join(LOC,FL)

    def __init__(self, master, entries=None):
        self.master = master
        self.crypt = Crypt()
        self.reg = Reg()

        if entries != None:
            try:
                self.entries = int(entries)
                mg.showwarning(
                    'Voting Master', 'The previous Tokens are about to be overwriiten if exists.', parent=master)
            except:
                mg.showerror('Error', 'Input is not valid.', parent=master)
                raise ValueError ('Invalid Input')

    def gen(self):
        def key_gen(size=8, chars=digits):
            with open(Tokens.TPath, 'r') as f:
                try:
                    self.tkn_read = eval(f.read())
                    self.tkn_read = self.crypt.decrypt(
                        str(self.tkn_read), self.reg.get(SECRET_KEY))
                except:
                    self.tkn_read = []

            key = ''.join(choice(chars) for _ in range(size))
            if key not in self.tkn_read:
                return key
            else:
                return None

        try:
            with open(Tokens.TPath, 'w') as f:
                tkn = []
                for _ in range(self.entries):
                    val = key_gen()
                    if val is not None:
                        tkn.append(val)
                tkn = self.crypt.encrypt(str(tkn), self.reg.get(SECRET_KEY))
                f.write(f'{tkn}')
            mg.showinfo(
                'Voting Master', f'{self.entries} Token(s) Generated.', parent=self.master)
        except:
            pass

    def get(self, val: str):
        with open(Tokens.TPath, 'r') as f:
            tkn_lst = eval(self.crypt.decrypt(str(f.read()), self.reg.get(SECRET_KEY)))
        try:
            ind = tkn_lst.index(val)
            del tkn_lst[ind]
            with open(Tokens.TPath, 'w') as f:
                tkn_lst = self.crypt.encrypt(str(tkn_lst), self.reg.get(SECRET_KEY))
                f.write(str(tkn_lst))
            return True
        except:
            mg.showwarning(
                'Error', 'The Key is either wrong or has been used.', parent=self.master)
            return False

    def check(self):
        try:
            with open(Tokens.TPath, 'r') as f:
                tkn_lst = f.read()
                tkn_lst = eval(self.crypt.decrypt(str(tkn_lst), self.reg.get(SECRET_KEY)))
            if len(tkn_lst) == 0:
                mg.showerror('Error', 'No Tokens in the Token file.',
                             parent=self.master)
                return False
        except:
            mg.showerror('Error', 'Token file doesn\'t exists!',
                         parent=self.master)
            return False


class Cand_Check:
    def __init__(self, key):
        self.key = key
        self.cand = [eval(i) for i in list(Access_Config().cand_config.keys())]
        self.ind = [i[0] for i in self.cand].index(self.key)

    def get(self):
        return str(self.cand[self.ind])


class Default_Config:
    """Contains Default configurations for the application."""
    base_config = "{'passwd' : '', 'key': ''}"
    candidate_config = "{\"['HeadBoy', 'HB']\" : [], \"['ViceHeadBoy', 'VHB']\" : [], \"['HeadGirl', 'HG']\" : [], \"['ViceHeadGirl', 'VHG']\" : []}"
    clss_config = "{6 : ['A', 'B', 'C', 'D'], 7 : ['A', 'B', 'C', 'D'], 8 : ['A', 'B', 'C', 'D'], 9 : ['A', 'B', 'C', 'D'], 10 : ['A', 'B', 'C', 'D'], 11 : ['A', 'B', 'C', 'D'], 12 : ['A', 'B', 'C', 'D']}"


class Write_Default:
    """Writes Default config file which doesn't exist already, in the /ProgramData directory."""
    exist = 0
    loc = None
    if system().lower()=='windows':
    	loc = os.path.join(os.getenv('ALLUSERSPROFILE'),'votm-data')
    else:
   		loc = os.path.join(os.path.expanduser('~'),'.votm-data')
    fles = ['cand.vcon', 'clss.vcon']

    def __init__(self):
        Write_Default.exist = 0
        self.crypt = Crypt()
        self.reg = Reg()
        if not os.path.exists(Write_Default.loc):
            os.mkdir(Write_Default.loc)
        eval_lst = [os.path.exists(os.path.join(Write_Default.loc,f))
                    == False for f in Write_Default.fles]

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
            self.reg.setx(ENV_KEY, self.crypt.encrypt(
                Default_Config.base_config, self.reg.get(SECRET_KEY)))
            self.reg.close()

    @staticmethod
    def rand(size=8, chars=__import__('string').ascii_letters + __import__('string').digits + "@#$&"):
        return ''.join(__import__('random').choice(chars) for _ in range(size))

    def wrt_cand(self):
        """Writes Candidate file."""
        with open(os.path.join(Write_Default.loc,Write_Default.fles[0]), 'w') as f:
            f.write(self.reg.get(SECRET_KEY)+self.crypt.encrypt(
                Default_Config.candidate_config, self.reg.get(SECRET_KEY)))

    def wrt_clss(self):
        """Writes Class&Sec file."""
        with open(os.path.join(Write_Default.loc,Write_Default.fles[1]), 'w') as f:
            f.write(self.reg.get(SECRET_KEY)+self.crypt.encrypt(
                Default_Config.clss_config, self.reg.get(SECRET_KEY)))


class Access_Config:
    """Access config files located in the /roaming directory."""

    def __init__(self):
        loc = Write_Default.loc
        fles = Write_Default.fles
        self.crypt = Crypt()
        self.reg = Reg()
        bse_str = self.reg.get(ENV_KEY)
        bse_str = self.crypt.decrypt(bse_str, self.reg.get(SECRET_KEY))
        with open(os.path.join(loc,fles[0]), 'r') as f:
            cand_str = f.read()
            cand_str = self.crypt.decrypt(cand_str[16:], cand_str[:16])
        with open(os.path.join(loc,fles[1]), 'r') as f:
            clss_str = f.read()
            clss_str = self.crypt.decrypt(clss_str[16:], clss_str[:16])

        self.bse_config = eval(bse_str)
        self.cand_config = eval(cand_str)
        self.clss_config = eval(clss_str)
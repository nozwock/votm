"""
A logical subset part of the main application.
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

"""
Change Salt at line 115.
"""

import sys, os
from random import choice
from string import digits
from Crypto.Cipher import AES
from collections import OrderedDict
from tkinter import messagebox as mg
from base64 import b64encode, b64decode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from votmapi.__main__ import SECRET_KEY
from winreg import (ConnectRegistry, OpenKey, SetValueEx, DeleteKeyEx,
                    QueryValueEx, CloseKey, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_EXPAND_SZ)


class Tokens:
    """Handles Tokens generation, saving and to get a specific token."""
    LOC = os.getenv('ALLUSERSPROFILE')
    FL = 'tkn.vcon'

    def __init__(self, master, entries=None):
        self.master = master
        self.crypt = Crypt()

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
            with open(rf'{Tokens.LOC}\{Tokens.FL}', 'r') as f:
                try:
                    self.tkn_read = eval(f.read())
                    self.tkn_read = self.crypt.decrypt(
                        str(self.tkn_read), SECRET_KEY)
                except:
                    self.tkn_read = []

            key = ''.join(choice(chars) for _ in range(size))
            if key not in self.tkn_read:
                return key
            else:
                return None

        try:
            with open(rf'{Tokens.LOC}\{Tokens.FL}', 'w') as f:
                tkn = []
                for _ in range(self.entries):
                    val = key_gen()
                    if val is not None:
                        tkn.append(val)
                tkn = self.crypt.encrypt(str(tkn), SECRET_KEY)
                f.write(f'{tkn}')
            mg.showinfo(
                'Voting Master', f'{self.entries} Token(s) Generated.', parent=self.master)
        except:
            pass

    def get(self, val: str):
        with open(rf'{Tokens.LOC}\{Tokens.FL}', 'r') as f:
            tkn_lst = eval(self.crypt.decrypt(str(f.read()), SECRET_KEY))
        try:
            ind = tkn_lst.index(val)
            del tkn_lst[ind]
            with open(rf'{Tokens.LOC}\{Tokens.FL}', 'w') as f:
                tkn_lst = self.crypt.encrypt(str(tkn_lst), SECRET_KEY)
                f.write(str(tkn_lst))
            return True
        except:
            mg.showwarning(
                'Error', 'The Key is either wrong or has been used.', parent=self.master)
            return False

    def check(self):
        try:
            with open(rf'{Tokens.LOC}\{Tokens.FL}', 'r') as f:
                tkn_lst = f.read()
                tkn_lst = eval(self.crypt.decrypt(str(tkn_lst), SECRET_KEY))
            if len(tkn_lst) == 0:
                mg.showerror('Error', 'No Tokens in the Token file.',
                             parent=self.master)
                return False
        except:
            mg.showerror('Error', 'Token file doesn\'t exists!',
                         parent=self.master)
            return False


class Crypt:
    def __init__(self, salt='<16-character-salt>'):
        self.salt = salt
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key, AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc)
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except:
            pass

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key, AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except:
            pass


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
            for i in range(-1, -len(dict(self.state))-1, -1):
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
            print('Error, No such key exists.')

    def get(self):
        return dict(self.state)

    def __repr__(self):
        return repr(dict(self.state))


class Reg:
    def __init__(self):
        self.path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        self.reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        self.key = OpenKey(self.reg, self.path, 0, KEY_ALL_ACCESS)

    def setx(self, _key, val):
        SetValueEx(self.key, _key, 0, REG_EXPAND_SZ, val)

    def delx(self, _key):
        DeleteKeyEx(self.key, _key)

    def get(self, _key):
        return QueryValueEx(self.key, _key)[0]

    def close(self):
        CloseKey(self.reg)
        CloseKey(self.key)
        del self

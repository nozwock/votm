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

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from collections import OrderedDict
from base64 import b64encode, b64decode

from winreg import (
    ConnectRegistry,
    OpenKey,
    SetValueEx,
    DeleteKeyEx,
    QueryValueEx,
    CloseKey,
    HKEY_LOCAL_MACHINE,
    KEY_ALL_ACCESS,
    REG_EXPAND_SZ,
)


#! CBC method with PKCS#7 padding
class Crypt:
    def __init__(self, salt=Random.new().read(AES.block_size)):
        self.salt = salt
        self.enc_dec_method = "latin-1"

    def encrypt(self, src, key, encode=True):
        src = src.encode()
        key = SHA256.new(key.encode()).digest()
        aes_obj = AES.new(key, AES.MODE_CBC, self.salt)
        padd = AES.block_size - len(src) % AES.block_size
        src += bytes([padd]) * padd
        hx_enc = self.salt + aes_obj.encrypt(src)
        return b64encode(hx_enc).decode(self.enc_dec_method) if encode else hx_enc

    def decrypt(self, src, key, decode=True):
        if decode:
            str_tmp = b64decode(src.encode(self.enc_dec_method))
        key = SHA256.new(key.encode()).digest()
        salt = str_tmp[: AES.block_size]
        aes_obj = AES.new(key, AES.MODE_CBC, salt)
        str_dec = aes_obj.decrypt(str_tmp[AES.block_size :])
        padd = str_dec[-1]
        if str_dec[-padd:] != bytes([padd]) * padd:
            pass
        return str_dec[:-padd].decode(self.enc_dec_method)


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


# For Windows ONLY
class Reg:
    def __init__(self):
        self.path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
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

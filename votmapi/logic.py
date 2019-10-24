"""A logical subset part of the main application."""

import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from datetime import date
from os import getenv, path, walk
from tkinter import messagebox as mg
from string import digits
from random import choice
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

__author__ = 'Sagar Kumar'
__version__ = '0.9.8'
SECRET_KEY = 'SykO@qd5ADyx7FpAzOiH2yqoeoQEg300'


class Sql_init:
    """Establishes connection with the requested database."""
    TBL_NM = 'votm_vte'
    NXT = 1

    def __init__(self, _key: int, dtb=None, yr=None, master=None):
        self.master = master
        Sql_init.NXT = 1
        self.yr = date.today().strftime('%Y')
        if dtb:
            self.db = rf'{Write_Default.loc}\votm_merged.db'
        elif yr:
            self.db = rf'{Write_Default.loc}\votm_{yr}.db'
        else:
            self.db = rf'{Write_Default.loc}\votm_{self.yr}.db'

        self.con = sql.connect(self.db, isolation_level=None)
        if _key:
            mg.showinfo('Connection Established',
                        'Connection to the Database has been successfully established.', parent=master)
        self.cur = self.con.cursor()

    def tbl(self):
        """Creates table if not exists already."""
        try:
            EXEC = 1
            __tbl_sy = f"""CREATE TABLE IF NOT EXISTS {Sql_init.TBL_NM}(
                STAFF INT DEFAULT(NULL),
                CLASS INT(2) DEFAULT(NULL),
                SEC VARCHAR(1) DEFAULT(NULL),
                STUDENT INT DEFAULT(NULL))"""
            self.cur.execute(__tbl_sy)
            cand_lst = [[x, Access_Config().cand_config[x]]
                        for x in list(Access_Config().cand_config.keys())]
            cand_lst[0][0], cand_lst[1][0], cand_lst[2][0], cand_lst[3][0] = 'HB', 'VHB', 'HG', 'VHG'
            tbl_cand, _ = Sql_init(0).cols(self.yr)
            tbl_cand = tbl_cand[4:len(tbl_cand)]
            if tbl_cand == []:
                pass
            else:
                chk_cand = []
                for i in range(len(cand_lst)):
                    for j in range(len(cand_lst[i][1])):
                        pst_cand = f'{cand_lst[i][0]}_{cand_lst[i][1][j]}'
                        chk_cand.append(pst_cand)
                if any([i not in tbl_cand for i in chk_cand]):
                    ch = mg.askyesnocancel(
                        '', 'The Candidates in the Settings and in the Database are different.\nDo you want to Recreate the Database with the New Candidates<Yes>, Or Continue with the Candidates in the Database<No>?', parent=self.master)
                    if ch is True:
                        __drp_sy = f'DROP TABLE {Sql_init.TBL_NM}'
                        self.cur.execute(__drp_sy)
                        self.con.close()
                        Sql_init(0).tbl()
                    elif ch is False:
                        EXEC = 0
                    else:
                        EXEC = 0
                        Sql_init.NXT = 0
            if EXEC:
                for i in range(len(cand_lst)):
                    for j in range(len(cand_lst[i][1])):
                        pst_cand = f'{cand_lst[i][0]}_{cand_lst[i][1][j]}'
                        __tbl_upd_sy = f'ALTER TABLE {Sql_init.TBL_NM} ADD {pst_cand} INT DEFAULT(NULL)'
                        self.cur.execute(__tbl_upd_sy)
        except:
            pass

    def tchr_vte(self, vte_lst: list):
        """Updates database with selected entries."""
        __tbl_chk_sy = f"SELECT STAFF FROM {Sql_init.TBL_NM} WHERE STAFF IS NOT NULL"
        self.cur.execute(__tbl_chk_sy)
        val = self.cur.fetchone()
        if val is not None:  # Exists i.e Update
            vte_lst = [f"{i} = {i} + 1" for i in vte_lst]
            vte_lst = (str(vte_lst).lstrip('[').rstrip(']')).replace("'", "")
            __tbl_upd_sy = f"""
            UPDATE {Sql_init.TBL_NM}
            SET STAFF = STAFF + 1, {vte_lst}
            WHERE STAFF IS NOT NULL
            """
            self.cur.execute(__tbl_upd_sy)
        else:  # does not exist i.e Create
            tbl_cand, _ = Sql_init(0).cols(self.yr)
            tbl_cand = tbl_cand[4:len(tbl_cand)]
            temp, _ = Sql_init(0).cols(self.yr)
            temp = temp[4:len(temp)]
            for i in range(len(temp)):
                if temp[i] in vte_lst:
                    temp[i] = 1
                else:
                    temp[i] = 0
            cand = str(tbl_cand).lstrip('[').rstrip(']')
            cand = cand.replace("'", "")
            '''
            This can be used too for above requirements->
            <str>.translate(str.marktrans({"'":None}))
            '''
            __tbl_ins_sy = f"""INSERT INTO {Sql_init.TBL_NM}(
                STAFF, {cand}
                )
            VALUES(
                1, {str(temp).lstrip('[').rstrip(']')}
            )
            """
            self.cur.execute(__tbl_ins_sy)

    def std_vte(self, *args: '(list, str, str)'):
        """Updates database with selected entries."""
        vte_lst, clss, sec = args
        __tbl_chk_sy = f"""SELECT CLASS, SEC FROM {Sql_init.TBL_NM}
        WHERE CLASS = {clss} AND SEC LIKE '{sec}'"""
        self.cur.execute(__tbl_chk_sy)
        val = self.cur.fetchone()
        if val is not None:  # UPDATE block
            vte_lst = [f"{i} = {i} + 1" for i in vte_lst]
            vte_lst = (str(vte_lst).lstrip('[').rstrip(']')).replace("'", "")
            __tbl_upd_sy = f"""
            UPDATE {Sql_init.TBL_NM}
            SET STUDENT = STUDENT + 1, {vte_lst}
            WHERE CLASS = {clss} AND SEC LIKE '{sec}'
            """
            self.cur.execute(__tbl_upd_sy)
        else:  # CREATE block
            tbl_cand, _ = Sql_init(0).cols(self.yr)
            tbl_cand = tbl_cand[4:len(tbl_cand)]
            temp, _ = Sql_init(0).cols(self.yr)
            temp = temp[4:len(temp)]
            for i in range(len(temp)):
                if temp[i] in vte_lst:
                    temp[i] = 1
                else:
                    temp[i] = 0
            cand = str(tbl_cand).lstrip('[').rstrip(']')
            cand = cand.replace("'", "")
            __tbl_ins_sy = f"""INSERT INTO {Sql_init.TBL_NM}(
                CLASS, SEC, STUDENT, {cand}
                )
            VALUES(
                {clss}, '{sec}', 1, {str(temp).lstrip('[').rstrip(']')}
            )
            """
            self.cur.execute(__tbl_ins_sy)

    def result(self, *args: '(String of fields to be shown)'):
        """Provides result in the form of list containing Records & Fields."""
        args = str(args).lstrip("('").rstrip("',)")
        if args.find('CLASS', 0, len(args)) == -1 and args.find('SEC', 0, len(args)) == -1 and args.find('STUDENT', 0, len(args)) == -1 and args.find('STAFF', 0, len(args)) != -1:
            __res_sel_sy = f"""
            SELECT {args} FROM {Sql_init.TBL_NM}
            WHERE STAFF IS NOT NULL
            ORDER BY CLASS
            """
        elif args.find('CLASS', 0, len(args)) == -1 and args.find('SEC', 0, len(args)) == -1 and args.find('STUDENT', 0, len(args)) != -1:
            if args.find('STAFF', 0, len(args)) == -1:
                args = str([f'SUM({i}) AS {i}' for i in [i for i in [
                           i.strip() for i in args.split(',')]]]).lstrip("['").rstrip("']").replace("'", "")
                __res_sel_sy = f"""
                SELECT {args} FROM {Sql_init.TBL_NM}
                WHERE STUDENT IS NOT NULL
                ORDER BY CLASS
                """
            else:
                args = str([f'SUM({i}) AS {i}' for i in [i for i in [i.strip() for i in args.split(
                    ',')] if i != 'STAFF']]).lstrip("['").rstrip("']").replace("'", "")
                __res_sel_sy = f"""
                SELECT STAFF, {args} FROM {Sql_init.TBL_NM}
                GROUP BY STAFF
                ORDER BY CLASS
                """
        elif args.find('SEC', 0, len(args)) == -1 and args.find('CLASS', 0, len(args)) != -1:
            if args.find('STAFF', 0, len(args)) == -1:
                args = str([f'SUM({i}) AS {i}' for i in [i for i in [i.strip() for i in args.split(
                    ',')] if i != 'CLASS' and i != 'STAFF']]).lstrip("['").rstrip("']").replace("'", "")
                __res_sel_sy = f"""
                SELECT CLASS, {args} FROM {Sql_init.TBL_NM}
                WHERE STUDENT IS NOT NULL
                GROUP BY CLASS
                ORDER BY CLASS
                """
            else:
                args = str([f'SUM({i}) AS {i}' for i in [i for i in [i.strip() for i in args.split(
                    ',')] if i != 'CLASS' and i != 'STAFF']]).lstrip("['").rstrip("']").replace("'", "")
                __res_sel_sy = f"""
                SELECT STAFF ,CLASS, {args} FROM {Sql_init.TBL_NM}
                GROUP BY CLASS
                ORDER BY CLASS
                """
        elif (args.find('CLASS', 0, len(args)) != -1 or args.find('SEC', 0, len(args)) != -1 or args.find('STUDENT', 0, len(args)) != -1) and args.find('STAFF', 0, len(args)) == -1:
            __res_sel_sy = f"""
            SELECT {args} FROM {Sql_init.TBL_NM}
            WHERE STUDENT IS NOT NULL
            ORDER BY CLASS
            """
        else:
            __res_sel_sy = f"""
            SELECT {args} FROM {Sql_init.TBL_NM}
            ORDER BY CLASS
            """
        self.cur.execute(__res_sel_sy)
        res = self.cur.fetchall()
        return res, [i[0] for i in self.cur.description]

    def cols(self, *args: str):
        """Return list of columns, and table description."""
        yr, = args
        self.con.close()
        db = rf'{Write_Default.loc}\votm_{yr}.db'
        con = sql.connect(db, isolation_level=None)
        cur = con.cursor()
        __dsc_sy = f'PRAGMA table_info({Sql_init.TBL_NM})'
        cur.execute(__dsc_sy)
        desc = cur.fetchall()
        cols = [tup[1] for tup in desc]
        con.close()
        return cols, desc

    def db_cands(self):
        """Returns candidates in the database."""
        self.cur.execute("PRAGMA table_info(votm_vte)")
        desc = self.cur.fetchall()
        cols = [tup[1] for tup in desc if tup[1] not in [
            'STAFF', 'CLASS', 'SEC', 'STUDENT']]
        cols = [i.split('_') for i in cols]
        dfl = {'HB': [], 'VHB': [], 'HG': [], 'VHG': []}
        for i in range(len(cols)):
            for j in range(1, len(cols[i])):
                dfl[cols[i][0]].append(cols[i][j])
        return dfl

    def gen_mrg_fle(self):
        """Creates Merge file with table details."""
        vals = []
        __vals_sy = f"""
        SELECT * FROM {Sql_init.TBL_NM}
        """
        self.cur.execute(__vals_sy)
        records = [tup for tup in self.cur.fetchall()]
        for _ in records:
            vals.append(_)
        return vals

    def mrg_dtb_res(self, *args: '(list of tables, list of (tables desc, records))'):
        """Creates "merged" named database consisting merged result."""
        tbl, vals, = args
        __fnl_sy = f"""CREATE TABLE {Sql_init.TBL_NM} \nAS """
        datype, _ = vals[0]
        lst = str([f'SUM({j}) AS {j}' for j in [i[0] for i in list(
            datype)] if j != 'CLASS' and j != 'SEC']).replace("'", '').rstrip(']').lstrip('[')
        __fnl_sy += f"""SELECT CLASS, SEC, {lst}\nFROM (\n"""
        for i in range(len(tbl)):
            datype, rcrds, = vals[i]
            datype = str(tuple([(str(i).replace(',', ' ')).rstrip(')').lstrip('(') for i in datype])).replace(
                '"', "").replace("'", '')
            if len(rcrds) > 1:
                rcrds = ('('+str(tuple([str(b).replace('None', 'NULL').replace(
                    "'", '"') for b in rcrds])).replace("'", '').rstrip(')').lstrip('(')+')')
            else:
                rcrds = ('('+str(tuple([str(b).replace('None', 'NULL').replace(
                    "'", '"') for b in rcrds])).replace("'", '').rstrip(',)').lstrip('(')+')')
            try:
                __tbl_sy = f"""
                CREATE TABLE {tbl[i]}{datype}
                """
                self.cur.execute(__tbl_sy)
                __ins_sy = f"""
                INSERT INTO {tbl[i]}
                VALUES {rcrds}
                """
                self.cur.execute(__ins_sy)
            except:
                pass
            finally:
                __fnl_sy += f"""SELECT * FROM {tbl[i]}\nUNION ALL\n"""

        __fnl_sy = __fnl_sy.rstrip('UNION ALL\n')
        __fnl_sy += '\n)\nGROUP BY CLASS, SEC'
        try:
            self.cur.execute(__fnl_sy)
        except:
            __drp_sy = f'DROP TABLE {Sql_init.TBL_NM}'
            self.cur.execute(__drp_sy)
            for i in tbl:
                __drp_sy = f"""
                DROP TABLE IF EXISTS {i}
                """
                self.cur.execute(__drp_sy)
            Sql_init(0, dtb=1).mrg_dtb_res(tbl, vals)
        finally:
            for i in tbl:
                __drp_sy = f"""
                DROP TABLE IF EXISTS {i}
                """
                self.cur.execute(__drp_sy)


class Tokens:
    """Handles Tokens generation, saving and to get a specific token."""
    LOC = getenv('ALLUSERSPROFILE')
    FL = 'tkn.md'

    def __init__(self, master, entries=None):
        self.master = master
        self.crypt = Crypt()

        if entries != None:
            try:
                self.entries = int(entries)
                mg.showwarning(
                    'Warning!', 'The previous Tokens are about to be overwriiten if exists.', parent=master)
            except:
                mg.showerror('Error', 'Incorrect Value.', parent=master)

    def gen(self):
        # def key_gen(size=8, chars=ascii_letters + digits):
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
                'Info', f'{self.entries} Token(s) Generated.', parent=self.master)
        except:
            raise

    def get(self, val: str):
        with open(rf'{Tokens.LOC}\{Tokens.FL}', 'r') as f:
            tkn_lst = eval(self.crypt.decrypt(str(f.read()), SECRET_KEY))
        try:
            print(tkn_lst)
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
    def __init__(self, salt='SlTKeYOpHygTYkP3'):
        self.salt = salt
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key, AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc)
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError(
                    'Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError(
                    'Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key, AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError(
                    'Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError(
                    'Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)


class Ent_Box(tk.Toplevel):
    """Constructs a toplevel frame whose master is Win,
    It provides a interface for authentication system."""

    def __init__(self, master, txt: str = 'Enter Password & Confirm to Continue.', icn: dir = None, chk: str = 'passwd'):
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.chk = chk
        self.protocol('WM_DELETE_WINDOW', self.s_cls)
        x = self.winfo_screenwidth()/2 - 175
        y = self.winfo_screenheight()/2 - 120
        '''
        For Center of Main Window->
        app.winfo_x() + 400 - 175
        app.winfo_y() + 225 - 70
        '''
        self.geometry('350x140+%d+%d' % (x, y))
        self.title('Confirm')
        self.resizable(0, 0)
        self.config(background='#F5F6F7')
        self.iconbitmap(icn)
        self.grab_set()
        self.lift()
        self.attributes('-topmost', True)
        dsc = tk.Label(self, text=txt, font=(
            'Segoe UI', 12), background='#FF3232', foreground='#EFEFEF')
        dsc.pack(side='top', fill='x', pady=(0, 20), ipady=6)
        spc_reg = self.register(self.spc_check)
        ent_bx = ttk.Entry(self, show='*', validate='key',
                           validatecommand=(spc_reg, '%S'))
        ent_bx.pack(side='top')
        ent_bx.focus_force()
        ent_bx.bind('<Return>', lambda event: self.ok_chk(ent_bx))
        btm_frm = tk.Frame(self, background='#F5F6F7')
        btm_frm.pack(side='bottom', pady=(0, 10))
        ok_btn = ttk.Button(btm_frm, text='Ok',
                            command=lambda: self.ok_chk(ent_bx))
        ok_btn.pack(side='left', padx=(0, 30))
        can_btn = ttk.Button(btm_frm, text='Cancel',
                             command=lambda: self.cncl())
        can_btn.pack(side='left')
        self.wait_window(self)

    @staticmethod
    def s_cls():
        """Prevents app from closing."""
        pass

    @staticmethod
    def spc_check(inp: str):
        """Restricts the use of whitespaces."""
        if inp != ' ':
            return True
        else:
            return False

    def ok_chk(self, ent: tk.Entry):
        """Validates the passwords, and exits if matched."""
        pswd = Access_Config().bse_config[self.chk]
        if ent.get().strip() == pswd.strip():
            self.destroy()
            self.flag = True
        else:
            ent.delete(0, tk.END)
            self.attributes('-topmost', 0)
            mg.showerror('Error', 'Incorrect Key.', parent=self)
            self.attributes('-topmost', 1)

    def cncl(self):
        self.destroy()
        self.flag = False

    def get(self) -> bool:
        return self.flag


class Yr_fle:
    """Creates list of names of database files existing."""
    yr = []
    fle = []

    def __init__(self):
        fle = []
        for _, _, f in walk(Write_Default.loc):
            for file in f:
                if '.db' in file:
                    if 'votm_' in file:
                        fle.append(file)
        yr = [i.replace('votm_', '').replace('.db', '') for i in fle]
        Yr_fle.yr = yr
        Yr_fle.fle = fle


class Default_Config:
    """Contains Default configurations for the application."""
    base_config = "{'passwd' : '', 'key': ''}"
    candidate_config = "{'HeadBoy' : [], 'ViceHeadBoy' : [], 'HeadGirl' : [], 'ViceHeadGirl' : []}"
    clss_config = "{6 : ['A', 'B', 'C', 'D'], 7 : ['A', 'B', 'C', 'D'], 8 : ['A', 'B', 'C', 'D'], 9 : ['A', 'B', 'C', 'D'], 10 : ['A', 'B', 'C', 'D'], 11 : ['A', 'B', 'C', 'D'], 12 : ['A', 'B', 'C', 'D']}"


class Write_Default:
    """Writes Default config file which doesn't exist already, in the /roaming directory."""
    exist = 0
    loc = getenv('ALLUSERSPROFILE')
    fles = ['base.md', 'cand.md',
            'clss.md']

    def __init__(self):
        Write_Default.exist = 0
        self.crypt = Crypt()
        eval_lst = [path.exists(rf'{Write_Default.loc}\{f}')
                    == False for f in Write_Default.fles]
        if any(eval_lst):
            Write_Default.exist = 1
            j = 0
            for i in eval_lst:
                if i is True:
                    if j is 0:
                        self.wrt_base()
                    elif j is 1:
                        self.wrt_cand()
                    else:
                        self.wrt_clss()
                j += 1

    def wrt_base(self):
        """Writes Base file."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[0]}', 'w') as f:
            f.write(self.crypt.encrypt(Default_Config.base_config, SECRET_KEY))

    def wrt_cand(self):
        """Writes Candidate file."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[1]}', 'w') as f:
            f.write(self.crypt.encrypt(
                Default_Config.candidate_config, SECRET_KEY))

    def wrt_clss(self):
        """Writes Class&Sec file."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[2]}', 'w') as f:
            f.write(self.crypt.encrypt(Default_Config.clss_config, SECRET_KEY))


class Access_Config:
    """Access config files located in the /roaming directory."""

    def __init__(self):
        loc = Write_Default.loc
        fles = Write_Default.fles
        self.crypt = Crypt()
        with open(rf'{loc}\{fles[0]}', 'r') as f:
            bse_str = f.read()
            bse_str = self.crypt.decrypt(bse_str, SECRET_KEY)
        with open(rf'{loc}\{fles[1]}', 'r') as f:
            cand_str = f.read()
            cand_str = self.crypt.decrypt(cand_str, SECRET_KEY)
        with open(rf'{loc}\{fles[2]}', 'r') as f:
            clss_str = f.read()
            clss_str = self.crypt.decrypt(clss_str, SECRET_KEY)

        self.bse_config = eval(bse_str)
        self.cand_config = eval(cand_str)
        self.clss_config = eval(clss_str)


# TEST RUN________________
if __name__ == '__main__':
    Write_Default()
    root = tk.Tk()
    root.withdraw()
    mg.showinfo(
        'VotmAPI', f'A logical subset part of the main application.\n\nVersion: {__version__}\nAuthor: {__author__}, 12\'A, 2019-20')
    Sql_init(1)
    mg.showinfo('Succes', 'Test run Successfull.')

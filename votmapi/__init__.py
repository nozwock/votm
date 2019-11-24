"""
Contains important definations of the program.
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

import sys
import os
import webbrowser
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import font
from datetime import date
from tkinter import messagebox as mg
from tkinter.scrolledtext import ScrolledText
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from votmapi.logic import Crypt, Reg
from votmapi.__main__ import SECRET_KEY, ENV_KEY, __version__, __author__, __license__


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
            cand_lst = [[eval(x)[-1], Access_Config().cand_config[x]]
                        for x in list(Access_Config().cand_config.keys())]
            tbl_cand = Sql_init(0).cols(self.yr)[0]
            tbl_cand = tbl_cand[4:len(tbl_cand)]
            if tbl_cand == []:
                pass
            else:
                chk_cand = []
                for i in range(len(cand_lst)):
                    for j in range(len(cand_lst[i][1])):
                        pst_cand = f'{cand_lst[i][0]}_{cand_lst[i][1][j]}'
                        chk_cand.append(pst_cand)
                if any([i not in tbl_cand for i in chk_cand]) or any([i not in chk_cand for i in tbl_cand]):
                    ch = mg.askyesnocancel(
                        'Voting Master', 'The Data in the Settings and in the Database are different.\nDo you want to Recreate the Database with the New Data<Yes>, Or Continue with the Data in the Database<No>?', parent=self.master)
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
        #dfl = {'HB': [], 'VHB': [], 'HG': [], 'VHG': []}
        dfl = {}
        _ = []
        for i in range(len(cols)):
            if cols[i][0] not in _:
                _.append(cols[i][0])
                dfl[cols[i][0]] = []

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

class Tr_View(tk.Frame):
    def __init__(self, master, cols: list, data, mode=None):
        super().__init__(master)
        self.pack(fill='both', expand=1)
        self.master = master
        self.cols = cols
        self.data = data

        ttk.Style(self.master).map('Treeview', foreground=self.fixed_map('foreground'), background=self.fixed_map('background'))
        ttk.Style(self.master).configure('Treeview', bd=0, highlightthickness=0, font=(None,12))
        ttk.Style(self.master).configure('Treeview.Heading', font=(None,12))
        ttk.Style(self.master).layout('Treeview', [('m.Treeview.treearea', {'sticky': 'nswe'})])

        top_f = tk.Frame(self)
        top_f.pack(side='top', fill='both', expand=1)
        view_f = tk.Frame(top_f, width=0, height=0)
        view_f.pack_propagate(0)
        view_f.pack(side='left', fill='both', expand=1)

        self.view = ttk.Treeview(view_f)
        self.view.pack(fill='both', expand=1)
        self.view.bind('<Button-1>', self.disable_col_resize)
        self.view.tag_configure('alt1', background='#F4F4F4')
        self.view.tag_configure('alt2', background='#EDEDED')

        if mode:
            if mode=='x':
                self.xbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.view.xview)
                self.xbar.pack(side='bottom', fill='x', padx=(0, 17))
                self.view.configure(xscrollcommand=self.xbar.set)
            elif mode=='y':
                self.ybar = tk.Scrollbar(top_f, orient=tk.VERTICAL, command=self.view.yview)
                self.ybar.pack(side='left', fill='y')
                self.view.configure(yscrollcommand=self.ybar.set)
            else:
                pass
        else:
            self.xbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.view.xview)
            self.ybar = tk.Scrollbar(top_f, orient=tk.VERTICAL, command=self.view.yview)
            self.xbar.pack(side='bottom', fill='x', padx=(0, 17))
            self.ybar.pack(side='left', fill='y')

            self.view.configure(xscrollcommand=self.xbar.set)
            self.view.configure(yscrollcommand=self.ybar.set)

        self.view['columns'] = self.cols
        self.view['show'] = 'headings'

        for _ in self.cols:
            exec(f'self.view.heading(\'{_}\', text=\'{_}\')')
            exec(f'self.view.column(\'{_}\', stretch=0)')

        for _ in self.view['columns']:
            self.view.column(_, anchor='center')

        self.data = eval(str(self.data).replace('None', "'-'"))

        for _ in range(len(self.data)):
            if _%2==0:
                self.view.insert('', 'end', values=self.data[_], tags='alt1')
            if _%2!=0:
                self.view.insert('', 'end', values=self.data[_], tags='alt2')

    @staticmethod
    def fixed_map(option):
        return [elm for elm in ttk.Style().map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

    def disable_col_resize(self, event):
        if self.view.identify_region(event.x, event.y) == 'separator':
            return 'break'


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
        self.focus_force()
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


class About(tk.Toplevel):
    """Dialog box containing information regarding the App."""

    def __init__(self, master, icn=None):
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        x = self.winfo_screenwidth()/2 - 198
        y = self.winfo_screenheight()/2 - 100
        self.geometry('376x200+%d+%d' % (x, y))
        self.title('About')
        self.iconbitmap(icn)
        self.resizable(0, 0)
        self.grab_set()
        self.lift()
        self.focus_force()
        logo_lt = tk.Frame(self)
        logo_lt.pack(side='left', fill='y')
        about_rt = tk.Frame(self)
        about_rt.pack(side='left', fill='both', expand=1,
                      pady=(10, 10), padx=(0, 10))
        about_tp = tk.Frame(about_rt, bd=2, relief='groove')
        about_tp.pack(side='top', fill='both', expand=1)

        DATAFILE = '..\\res\\logo.png'
        #Change above to 'res\\logo.png' while using with pyinstaller
        if not hasattr(sys, 'frozen'):
            DATAFILE = os.path.join(os.path.dirname(__file__), DATAFILE)
        else:
            DATAFILE = os.path.join(sys.prefix, DATAFILE)
        self.img = tk.PhotoImage(file=DATAFILE)

        lgc = tk.Label(logo_lt, image=self.img)
        lgc.pack(ipadx=14, pady=(10, 0))
        label = tk.Label(about_tp, text='VOTM - Voting Master',
                         font=('Segoe UI', 10, 'bold'))
        label.pack(side='top', anchor='nw')
        ver = tk.Label(about_tp, text=f'Version {__version__}')
        ver.pack(side='top', anchor='nw')
        auth = tk.Label(about_tp, text=f'Copyright (C) 2019 {__author__}')
        auth.pack(side='top', anchor='nw', pady=(10, 0))
        bug_ttl = tk.Label(
            about_tp, text='Report bugs or request enhancements at:')
        bug_ttl.pack(side='top', anchor='nw', pady=(10, 0))
        url = 'https://github.com/sgrkmr/votm/issues'
        bug_lnk = tk.Label(about_tp, text=url, fg='#6A00FF')
        bug_lnk.pack(side='top', anchor='nw')
        url_fnt = font.Font(bug_lnk, bug_lnk.cget('font'))
        url_fnt.configure(underline=1)
        bug_lnk.config(font=url_fnt)
        bug_lnk.bind('<ButtonRelease-1>',
                     lambda event: webbrowser.open_new(url))
        bug_lnk.bind('<Enter>', lambda e: bug_lnk.config(fg='#9E5EFF'))
        bug_lnk.bind('<Leave>', lambda e: bug_lnk.config(fg='#6A00FF'))

        btn_frm = tk.Frame(about_rt)
        btn_frm.pack(side='top', pady=(10, 0), fill='both', expand=1)

        lcnse = ttk.Button(btn_frm, text='License',
                           command=lambda: License(self, icn=icn))
        lcnse.pack(side='left')
        ok = ttk.Button(btn_frm, text='Ok', command=lambda: self.destroy())
        ok.pack(side='right')
        self.wait_window(self)


class License(tk.Toplevel):
    def __init__(self, master, icn=None):
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.focus_force()
        self.title('Votm License')
        self.iconbitmap(icn)
        self.resizable(0, 0)
        self.grab_set()
        self.lift()
        x = self.winfo_screenwidth()/2 - 280
        y = self.winfo_screenheight()/2 - 220
        self.geometry('560x440+%d+%d' % (x, y))

        lcn_frm = tk.Frame(self, relief='groove', bd=2)
        lcn_frm.pack(side='top', fill='both', expand=1,
                     pady=(10, 10), padx=(10, 10))
        self.lcn = ScrolledText(lcn_frm, font=('Segoe UI', 9), relief='flat')
        self.lcn.pack(fill='both', expand=1)
        self.lcn.insert(0.0, __license__)
        self.lcn.config(state='disabled')

        close_frm = tk.Frame(self)
        close_frm.pack(side='top', fill='both', expand=1,
                       padx=(0, 10), pady=(0, 10))
        close = ttk.Button(close_frm, text='Close',
                           command=lambda: self.destroy())
        close.pack(side='right')
        close.focus_set()
        self.wait_window(self)


class Yr_fle:
    """Creates a list of names of database files existing."""
    yr = []
    fle = []

    def __init__(self):
        fle = []
        Yr_fle.fle = fle
        for _, _, f in os.walk(Write_Default.loc):
            for file in f:
                if '.db' in file:
                    if 'votm_' in file:
                        fle.append(file)
        yr = [i.replace('votm_', '').replace('.db', '') for i in fle]
        Yr_fle.yr = yr
        Yr_fle.fle = fle


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
    """Writes Default config file which doesn't exist already, in the /roaming directory."""
    exist = 0
    loc = os.getenv('ALLUSERSPROFILE')
    fles = ['cand.vcon', 'clss.vcon']

    def __init__(self):
        Write_Default.exist = 0
        self.crypt = Crypt()
        self.reg = Reg()
        eval_lst = [os.path.exists(rf'{Write_Default.loc}\{f}')
                    == False for f in Write_Default.fles]
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
                Default_Config.base_config, SECRET_KEY))
            self.reg.close()

    def wrt_cand(self):
        """Writes Candidate file."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[0]}', 'w') as f:
            f.write(self.crypt.encrypt(
                Default_Config.candidate_config, SECRET_KEY))

    def wrt_clss(self):
        """Writes Class&Sec file."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[1]}', 'w') as f:
            f.write(self.crypt.encrypt(Default_Config.clss_config, SECRET_KEY))


class Access_Config:
    """Access config files located in the /roaming directory."""

    def __init__(self):
        loc = Write_Default.loc
        fles = Write_Default.fles
        self.crypt = Crypt()
        self.reg = Reg()
        bse_str = self.reg.get(ENV_KEY)
        self.reg.close()
        bse_str = self.crypt.decrypt(bse_str, SECRET_KEY)
        with open(rf'{loc}\{fles[0]}', 'r') as f:
            cand_str = f.read()
            cand_str = self.crypt.decrypt(cand_str, SECRET_KEY)
        with open(rf'{loc}\{fles[1]}', 'r') as f:
            clss_str = f.read()
            clss_str = self.crypt.decrypt(clss_str, SECRET_KEY)

        self.bse_config = eval(bse_str)
        self.cand_config = eval(cand_str)
        self.clss_config = eval(clss_str)


if __name__ == '__main__':
    def do(win):
        win.destroy()
        sys.exit(0)
    Write_Default()
    root = tk.Tk()
    root.attributes('-alpha', 0.0)
    ab = About(root)
    ab.protocol('WM_DELTE_WINDOW', do(root))
    root.mainloop()

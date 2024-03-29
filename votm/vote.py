"""
Voting will be done through this.
Copyright (C) 2019-2022 nozwock

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
import platform

isWindows = platform.system().lower() == "windows"
isLinux = platform.system().lower() == "linux"

# if isWindows:
#     import ctypes
#     import win32api
#     import win32event
#     from winerror import ERROR_ALREADY_EXISTS

from os import path
from datetime import date
import tkinter as tk
from tkinter import ttk

if isLinux:
    from ttkthemes import ThemedStyle

from tkinter import messagebox as mg

from .locations import ASSETS_PATH
from .config import Config
from .core.db import Sql_init
from .core.ui import Ent_Box, About
from .utils.extras import Tokens
from .common import getImg, _checkInstance
from . import __author__, __version__


class Win(tk.Tk):
    """Main Window container."""

    SM_BG_HEX = "#F0F0F0"

    def __init__(self):
        global ICON_IMG
        super().__init__()
        out = Config().write_default()

        if isWindows:
            ttk.Style().theme_use("vista")
        elif isLinux:
            ThemedStyle().theme_use("breeze")

        ICON_IMG = getImg("app.gif", imgDATA)

        self.config(
            background=Win.SM_BG_HEX,
            relief="groove",
            highlightbackground="#000000",
            highlightcolor="#000000",
            highlightthickness=1,
        )

        x = self.winfo_screenwidth() / 2 - 400
        y = self.winfo_screenheight() / 2 - 240
        self.geometry("800x480+%d+%d" % (x, y))
        self.resizable(0, 0)
        self.iconphoto(True, ICON_IMG)
        self.title("VOTM - vote")

        ttk.Style().configure("TButton", focuscolor=self.cget("background"))

        # top_bar = tk.Frame(self, bg="#6A00FF", height=5)
        # top_bar.pack(fill="x")
        # top_bar.pack_propagate(0)
        # top_bar.bind("<Button-1>", self.get_pos)
        # top_bar.bind(
        #    "<B1-Motion>",
        #    lambda event: self.geometry(
        #        f"+{event.x_root+self.xwin}+{event.y_root+self.ywin}"
        #    ),
        # )
        # min_btn = tk.Label(
        #    top_bar, text="█", bg="#6A00FF", fg="#9E5EFF", font="Consolas 25"
        # )
        # min_btn.pack(side="right")
        # min_btn.bind("<Enter>", lambda event: min_btn.config(foreground="#C39EFF"))
        # min_btn.bind("<Leave>", lambda event: min_btn.config(foreground="#9E5EFF"))
        # min_btn.bind(
        #    "<ButtonRelease-1>", lambda event: (self.master.iconify(), self.withdraw())
        # )
        # self.master.bind("<FocusIn>", lambda event: self.lift())
        # self.master.bind(
        #    "<Map>",
        #    lambda event: (self.master.deiconify(), self.deiconify(), self.lift()),
        # )
        # self.master.bind(
        #    "<Unmap>", lambda event: (self.master.iconify(), self.withdraw())
        # )

        self.navbar()
        self.frame_n = None
        self.replace_frame(Home)
        self.protocol("WM_DELETE_WINDOW", self.s_cls)
        self.lift()

        if out == 1:
            mg.showerror(
                "Error",
                (
                    "error: either config file missing or is corrupted\n"
                    "falling back to default config..."
                ),
                parent=self,
            )

        if any(
            [
                (Config().load("candidate")[i]) == []
                for i in list(Config().load("candidate").keys())
            ]
        ):
            mg.showerror(
                "Error",
                "No Candidate found!, Add Candidate in Manage App.",
                parent=self,
            )
            self.destroy()
            sys.exit(0)
        else:
            pass

    @staticmethod
    def s_cls():
        """Prevents app from closing."""
        pass

    def replace_frame(self, cont: tk.Frame):
        """Cycle b/w frames."""
        frame = cont(self)

        if cont == Home:
            self.home.config(
                text="Category", background="#EFEFEF", foreground="#0077CC"
            )
            self.vote.config(text="Vote", background="#0077CC", foreground="#EFEFEF")
            self.clss.config(text="Class", background="#0077CC", foreground="#EFEFEF")
            self.done.config(text="Done", background="#0077CC", foreground="#EFEFEF")
        elif cont == Class:
            self.clss.config(text="Class", background="#EFEFEF", foreground="#0077CC")
            self.home.config(
                text="Category", background="#0077CC", foreground="#EFEFEF"
            )
            self.vote.config(text="Vote", background="#0077CC", foreground="#EFEFEF")
            self.done.config(text="Done", background="#0077CC", foreground="#EFEFEF")
        elif cont == Vote:
            self.vote.config(text="Vote", background="#EFEFEF", foreground="#0077CC")
            self.home.config(
                text="Category", background="#0077CC", foreground="#EFEFEF"
            )
            self.clss.config(text="Class", background="#0077CC", foreground="#EFEFEF")
            self.done.config(text="Done", background="#0077CC", foreground="#EFEFEF")
        else:
            self.done.config(text="Done", background="#EFEFEF", foreground="#0077CC")
            self.home.config(
                text="Category", background="#0077CC", foreground="#EFEFEF"
            )
            self.clss.config(text="Class", background="#0077CC", foreground="#EFEFEF")
            self.vote.config(text="Vote", background="#0077CC", foreground="#EFEFEF")

        if self.frame_n is not None:
            self.frame_n.pack_forget()

        self.frame_n = frame
        self.frame_n.pack(side="right", expand=True, fill="both")

    def ext(self):
        if Ent_Box(self, icn=ICON_IMG).get():
            self.destroy()
            sys.exit(0)

    @staticmethod
    def session() -> str:
        """Return current session."""
        yr = date.today().strftime("%Y")  #! Return Year only
        ssn = str(yr) + " - " + f"{int(yr) + 1}"
        return ssn

    # ? NAVBAR______________________________
    def navbar(self):
        """Left sided navbar for main window."""
        fl = tk.Frame(self, background="#0077CC", width=223)
        fl.pack(side="left", expand=0, fill="y")
        fl.pack_propagate(0)
        # ? NAVBAR's internal items______________________________
        flt = tk.Frame(fl)
        flt.pack(side="top", fill="both", expand=0)
        # flt.pack_propagate(0)
        self.lg_img = getImg("bg.png", imgDATA)
        flt.config(height=self.lg_img.height())
        lg_canv = tk.Canvas(flt, borderwidth=0, highlightthickness=0)
        lg_canv.place(x=0, y=0, relheight=1, relwidth=1, anchor="nw")
        lg_canv.create_image(0, 0, image=self.lg_img, anchor="nw")
        lg_canv.create_text(
            108,
            45,
            text="» " + self.session(),
            fill="#EFEFEF",
            font=("Segoe UI", 18, "bold"),
        )
        lg_canv.bind("<Button-1>", self.get_pos)
        lg_canv.bind(
            "<B1-Motion>",
            lambda event: self.geometry(
                f"+{event.x_root+self.xwin}+{event.y_root+self.ywin}"
            ),
        )

        flb = tk.Frame(fl, background="#0077CC")
        flb.pack(side="bottom", fill="x", expand=1, anchor="s")
        btxlb = tk.Button(
            flb,
            text="X",
            highlightthickness=0,
            background="#FF3232",
            activebackground="#FF4C4C",
            relief="flat",
            borderwidth=1,
            foreground="#EFEFEF",
            height=2,
            command=self.ext,
            font=("Segoe UI", 10, "bold"),
        )
        btxlb.pack(side="left", fill="x", expand=1, anchor="s")
        bthlb = tk.Button(
            flb,
            text="?",
            highlightthickness=0,
            background="#303030",
            activebackground="#6D6D6D",
            relief="flat",
            borderwidth=1,
            foreground="#EFEFEF",
            height=2,
            command=lambda: About(self, icn=ICON_IMG),
            font=("Segoe UI", 10, "bold"),
        )
        bthlb.pack(side="left", fill="x", expand=1, anchor="s")
        # ? NAVBAR's Content______________________________
        #!Todo: Just have 1 corresponding Label at a time instead of all 4 on NAVBAR, maybe?
        self.home = tk.Label(
            fl,
            text="Category",
            foreground="#FFFFFF",
            background="#0077CC",
            font=("Segoe UI", 16, "bold"),
        )
        self.home.pack(side="top", ipady=20, fill="x")
        self.clss = tk.Label(
            fl,
            text="Class",
            foreground="#FFFFFF",
            background="#0077CC",
            font=("Segoe UI", 16, "bold"),
        )
        self.clss.pack(side="top", ipady=20, fill="x")
        self.vote = tk.Label(
            fl,
            text="Vote",
            foreground="#FFFFFF",
            background="#0077CC",
            font=("Segoe UI", 16, "bold"),
        )
        self.vote.pack(side="top", ipady=20, fill="x")
        self.done = tk.Label(
            fl,
            text="Done",
            foreground="#FFFFFF",
            background="#0077CC",
            font=("Segoe UI", 16, "bold"),
        )
        self.done.pack(side="top", ipady=20, fill="x")

    def get_pos(self, event):
        self.xwin = self.winfo_x() - event.x_root
        self.ywin = self.winfo_y() - event.y_root


class Home(tk.Frame):
    """Constructs a frame for selection of type of voting, Staff or Students."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure("TLabelframe.Label", font=("Segoe UI", 17))
        ttk.Style().configure("1.TButton", font=("Segoe UI", 15))
        self.config(background=Win.SM_BG_HEX)

        btnfrm = ttk.LabelFrame(self, text="Choose", padding=10)
        btnfrm.pack(pady=160)
        btnt = ttk.Button(
            btnfrm,
            text="Staff",
            style="1.TButton",
            command=lambda: self.tch_sel(btnt, btns),
        )
        btnt.pack(pady=(0, 8))
        btns = ttk.Button(
            btnfrm,
            text="Students",
            style="1.TButton",
            command=lambda: self.std_sel(btns, btnt),
        )
        btns.pack()

    def tch_sel(self, *args: ttk.Button):
        """Takes to Vote frame if Staff selected."""
        global sel
        (
            btn1,
            btn2,
        ) = args
        sel = 0  #! for Staff, direct to Vote
        btn1.config(state="disabled")
        btn2.config(state="disabled")
        if Tokens(self).check() is False:
            app.destroy()
            sys.exit(0)
        Sql_init(1, master=self).tbl()
        if (
            Ent_Box(
                self, "Enter SuperKey & Confirm to Continue.", ICON_IMG, "key"
            ).get()
            and Sql_init.NXT == 1
        ):
            app.replace_frame(Vote)
        else:
            btn1.config(state="enabled")
            btn2.config(state="enabled")

    def std_sel(self, *args: ttk.Button):
        """Takes to Class frame if Students selected."""
        global sel
        (
            btn1,
            btn2,
        ) = args
        sel = 1  #! for students, move to Class frame
        btn1.config(state="disabled")
        btn2.config(state="disabled")
        if Tokens(self).check() is False:
            app.destroy()
            sys.exit(0)
        Sql_init(1, master=self).tbl()
        if (
            Ent_Box(
                self, "Enter SuperKey & Confirm to Continue.", ICON_IMG, "key"
            ).get()
            and Sql_init.NXT == 1
        ):
            app.replace_frame(Class)
        else:
            btn1.config(state="enabled")
            btn2.config(state="enabled")


class Class(tk.Frame):
    """Constructs a Class frame to choose a class & section for the students."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure("1.TButton", font=("Segoe UI", 12))
        self.config(background=Win.SM_BG_HEX)
        clss_lst = [str(i) for i in list(Config().load("class").keys())]

        btnfrm_class = ttk.LabelFrame(self, text="Class", padding=10)
        btnfrm_class.pack(side="top", pady=(150, 0))
        btn_class = ttk.Combobox(btnfrm_class, values=clss_lst, state="readonly")
        btn_class.set("Select")
        btn_class.pack()

        btnfrm_sec = ttk.LabelFrame(self, text="Section", padding=10)
        btnfrm_sec.pack(pady=(20, 0))
        btn_sec = ttk.Combobox(btnfrm_sec, state="readonly")
        btn_sec.set("Select")
        btn_sec.pack()

        btnnxt = ttk.Button(
            self,
            text="Next",
            style="1.TButton",
            command=lambda: self.mv_Vote(btn_class.get(), btn_sec.get()),
            state="disabled",
        )
        btnnxt.pack(side="bottom", pady=(0, 10))

        btn_class.bind(
            "<<ComboboxSelected>>",
            lambda event: (
                btn_sec.config(values=Config().load("class")[int(btn_class.get())])
            ),
        )
        btn_sec.bind(
            "<<ComboboxSelected>>", lambda event: btnnxt.config(state="enabled")
        )

    @staticmethod
    def mv_Vote(*args: str):
        """Moves to Vote frame from Class frame."""
        global ch_clss, ch_sec
        ch_clss, ch_sec = args
        app.replace_frame(Vote)


class Vote(tk.Frame):
    """Constructs a Vote frame for voting."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure("TLabelframe.Label", font=("Segoe UI", 13))
        ttk.Style().configure("1.TButton", font=("Segoe UI", 15))
        self.config(background=Win.SM_BG_HEX)

        cnd = Sql_init(0).db_cands()
        self.n_val = len(cnd)
        lcl_cnd = [eval(i) for i in list(Config().load("candidate").keys())]
        cn = 1
        self.args = []

        if self.n_val > 4:
            ttk.Style().configure("TNotebook", tabposition="s")
            ttk.Style().configure(
                "TNotebook.Tab",
                font=("Segoe UI", 14, "bold"),
                foreground="#8C8C8C",
                focuscolor=ttk.Style().configure(".")["background"],
                width=20,
            )
            self.tab = ttk.Notebook(self, padding=-3)
            p1 = tk.Frame(self.tab, background=Win.SM_BG_HEX)
            p2 = tk.Frame(self.tab, background=Win.SM_BG_HEX)
            self.tab.add(p1, text=f"{' '*20}1")
            self.tab.add(p2, text=f"{' '*20}2")
            self.tab.pack(side="right", expand=1, fill="both")
            self.tab.bind("<<NotebookTabChanged>>", lambda event: self.updt(event))
            for i in range(1, 3):
                exec(
                    f"cls_txt{i} = tk.Label(p{i}, text='', font=('Segoue UI', 12, 'bold'), bg='#C39EFF', fg='#FFFFFF')"
                )
                exec(f"cls_txt{i}.pack(side='top', anchor='n', fill='x', pady=(2,0))")
                if sel == 1:
                    txt = f"{ch_clss}' {ch_sec}"
                    exec(f"cls_txt{i}.config(text=txt)")
                else:
                    exec(f"cls_txt{i}.config(text='Staff')")
                exec(f"tkn_frm{i} = ttk.LabelFrame(p{i}, text='Token', padding=10)")
                exec(f"tkn_frm{i}.pack(pady=(50, 0))")
                exec(f"self.uppr{i} = tk.Frame(p{i}, background=Win.SM_BG_HEX)")
                exec(f"self.lwr{i} = tk.Frame(p{i}, background=Win.SM_BG_HEX)")
                exec(f"self.uppr{i}.pack(pady=(40, 20))")
                exec(f"self.lwr{i}.pack()")
            tkn_reg = self.register(self.tkn_check)
            for i in range(1, 3):
                exec(
                    f"self.tkn_ent{i} = ttk.Entry(tkn_frm{i}, validate='key',validatecommand=(tkn_reg, '%P'))"
                )
                exec(f"self.tkn_ent{i}.pack()")
            pg = 1

            for j in range(len(cnd)):
                text = str(list(cnd.keys())[j])
                for _ in range(len(lcl_cnd)):
                    if text == lcl_cnd[_][-1]:
                        text = lcl_cnd[_][0]
                        break
                if cn <= 2 and pg <= 4:
                    pos = self.uppr1
                elif cn > 2 and pg <= 4:
                    pos = self.lwr1
                elif cn <= 6 and pg > 4:
                    pos = self.uppr2
                else:
                    pos = self.lwr2
                if cn % 2 == 0:
                    padx = (0, 0)
                else:
                    padx = (0, 10)
                exec(
                    f"{str(list(cnd.keys())[j].lower())}_frm = ttk.LabelFrame(pos, text='{text}', padding=10)"
                )
                exec(
                    f"{str(list(cnd.keys())[j].lower())}_frm.pack(side='left', padx=padx)"
                )
                cn += 1
                pg += 1

            for i in range(len(cnd)):
                exec(
                    f"self.{str(list(cnd.keys())[i].lower())}_box = ttk.Combobox({str(list(cnd.keys())[i].lower())}_frm, values={cnd[list(cnd.keys())[i]]}, state='readonly')"
                )
                exec(f"self.{str(list(cnd.keys())[i].lower())}_box.set('Select')")
                exec(f"self.{str(list(cnd.keys())[i].lower())}_box.pack()")

            for i in range(1, 3):
                exec(
                    f"self.btnvt{i} = ttk.Button(p{i}, text='Vote', style='1.TButton', state='disabled',command= self.exec_do{i})"
                )
                exec(f"self.btnvt{i}.pack(side='bottom', pady=(0, 10))")

            for i in range(len(cnd)):
                exec(
                    f"self.{str(list(cnd.keys())[i].lower())}_box.bind('<<ComboboxSelected>>', self.exec_do_chk)"
                )
        else:
            cls_txt = tk.Label(
                self,
                text="",
                font=("Segoue UI", 12, "bold"),
                bg="#C39EFF",
                fg="#FFFFFF",
            )
            cls_txt.pack(side="top", anchor="n", fill="x")
            if sel == 1:
                cls_txt.config(text=f"{ch_clss}' {ch_sec}")
            else:
                cls_txt.config(text="Staff")

            tkn_frm = ttk.LabelFrame(self, text="Token", padding=10)
            tkn_frm.pack(pady=(50, 0))

            uppr = tk.Frame(self, background=Win.SM_BG_HEX)
            uppr.pack(pady=(40, 20))
            lwr = tk.Frame(self, background=Win.SM_BG_HEX)
            lwr.pack()

            tkn_reg = self.register(self.tkn_check)
            self.tkn_ent = ttk.Entry(
                tkn_frm, validate="key", validatecommand=(tkn_reg, "%P")
            )
            self.tkn_ent.pack()

            for j in range(len(cnd)):
                text = str(list(cnd.keys())[j])
                for _ in range(len(lcl_cnd)):
                    if text == lcl_cnd[_][-1]:
                        text = lcl_cnd[_][0]
                        break
                if cn <= 2:
                    pos = uppr
                else:
                    pos = lwr
                if cn % 2 == 0:
                    padx = (0, 0)
                else:
                    padx = (0, 10)
                exec(
                    f"{str(list(cnd.keys())[j].lower())}_frm = ttk.LabelFrame(pos, text='{text}', padding=10)"
                )
                exec(
                    f"{str(list(cnd.keys())[j].lower())}_frm.pack(side='left', padx=padx)"
                )
                cn += 1

            for i in range(len(cnd)):
                exec(
                    f"self.{str(list(cnd.keys())[i].lower())}_box = ttk.Combobox({str(list(cnd.keys())[i].lower())}_frm, values={cnd[list(cnd.keys())[i]]}, state='readonly')"
                )
                exec(f"self.{str(list(cnd.keys())[i].lower())}_box.set('Select')")
                exec(f"self.{str(list(cnd.keys())[i].lower())}_box.pack()")

            self.btnvt = ttk.Button(
                self,
                text="Vote",
                style="1.TButton",
                state="disabled",
                command=lambda: self.mv_Done(self.btnvt, self.tkn_ent, self.crt_args()),
            )
            self.btnvt.pack(side="bottom", pady=(0, 10))

            for i in range(len(cnd)):
                exec(
                    f"self.{str(list(cnd.keys())[i].lower())}_box.bind('<<ComboboxSelected>>', self.exec_do_al_chk)"
                )

    def exec_do1(self):
        self.mv_Done(self.btnvt1, self.tkn_ent1, self.crt_args())

    def exec_do2(self):
        self.mv_Done(self.btnvt2, self.tkn_ent2, self.crt_args())

    def exec_do_chk(self, event):
        self.chk_vote(self.btnvt1, self.btnvt2)

    def exec_do_al_chk(self, event):
        self.chk_vote(self.btnvt)

    def updt(self, event):
        slave = event.widget.winfo_children()[event.widget.index("current")]
        if str(slave).split("!")[-1] == "frame":
            self.tkn_ent1.delete(0, "end")
            self.tkn_ent1.insert(0, self.tkn_ent2.get())
        else:
            self.tkn_ent2.delete(0, "end")
            self.tkn_ent2.insert(0, self.tkn_ent1.get())

    def crt_args(self):
        cnd = Sql_init(0).db_cands()
        del self.args
        self.args = []
        for i in range(len(cnd)):
            exec(f"self.args.append(self.{str(list(cnd.keys())[i].lower())}_box.get())")
        return self.args

    def tkn_check(self, inp: str) -> bool:
        """Restricts all but numbers and that too upto 5 digits only."""
        if (inp.isdigit() or inp == "") and len(inp) <= 8:
            return True
        else:
            return False

    def chk_vote(self, _btn=None, btn2=None, event=None):
        """Makes sure Vote button stays disabled untill a candidate has been selected in each menu."""
        if _btn:
            btn = _btn
        else:
            btn = self.btnvt
        n = 0
        m = 0
        for j in [
            Sql_init(0).db_cands()[x] for x in list(Sql_init(0).db_cands().keys())
        ]:
            if self.crt_args()[m] in j:
                n += 1
            m += 1
        if n == self.n_val:
            btn.config(state="enabled")
            if btn2:
                btn2.config(state="enabled")

    def mv_Done(self, btnvt: ttk.Button, tkn, *args: str):
        """Move to Done frame while saving votes in database through the logic module."""
        (args,) = args
        global vte_lst  #! Votes of 1 turn
        if mg.askokcancel("Confirm", "Are you sure?", parent=self):
            if Tokens(self).get(tkn.get()):
                vte_lst = list(args)
                x = [eval(i) for i in list(Config().load("candidate").keys())]
                for i in range(len(vte_lst)):
                    vte_lst[i] = f"{x[i][-1]}_{vte_lst[i]}"
                if sel == 0:  #! Staff
                    btnvt.config(state="disabled")
                    Sql_init(0).tchr_vte(vte_lst)
                    app.replace_frame(Done_0)
                else:  #! Students
                    btnvt.config(state="disabled")
                    Sql_init(0).std_vte(vte_lst, ch_clss, ch_sec)
                    app.replace_frame(Done_1)


class Done(tk.Frame):
    """Constructs a Done frame providing options for Next or to end session."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure("1.TButton", font=("Segoe UI", 15))
        self.config(background=Win.SM_BG_HEX)

        cls_txt = tk.Label(
            self, text="", font=("Segoue UI", 12, "bold"), bg="#C39EFF", fg="#FFFFFF"
        )
        cls_txt.pack(side="top", anchor="n", fill="x")
        if sel == 1:
            cls_txt.config(text=f"{ch_clss}' {ch_sec}")
        else:
            cls_txt.config(text="Staff")

        botmos = tk.Frame(self, background=Win.SM_BG_HEX)
        botmos.pack(fill="x", pady=(170, 100))
        self.lowos = tk.Frame(self, background=Win.SM_BG_HEX)
        self.lowos.pack(side="bottom", pady=(0, 30))
        klb = tk.Label(
            botmos,
            text="Done",
            font=("Segoe UI", 35, "bold"),
            background="#29B539",
            foreground="#FFFFFF",
        )
        klb.pack(fill="x")

    def bck_vote_next(self):
        """Moves to Vote frame again."""
        app.replace_frame(Vote)

    @staticmethod
    def bck_chng_clss_save():
        """Moves to Class frame from calling on in the Close/Continue Dialog box which requires passsword."""
        if Ent_Box(app, icn=ICON_IMG).get():
            app.replace_frame(Class)


class Done_0(Done):
    """Inheritates from Done frame and is to be used while Staff voting."""

    def __init__(self, parent: Win):
        Done.__init__(self, parent)
        bcktovote = ttk.Button(
            self.lowos, text="Next", style="1.TButton", command=self.bck_vote_next
        )
        bcktovote.pack(side="left")


class Done_1(Done):
    """Inheritates from Done frame, also have a additional Change class button
    and is to be used while Students voting."""

    def __init__(self, parent: Win):
        Done.__init__(self, parent)
        bcktovote = ttk.Button(
            self.lowos, text="Next", style="1.TButton", command=self.bck_vote_next
        )
        bcktovote.pack(side="left", padx=(0, 40))
        bcktoclss = ttk.Button(
            self.lowos,
            text="Change Class",
            style="1.TButton",
            command=self.bck_chng_clss_save,
        )
        bcktoclss.pack(side="left")


def main():
    global app, imgDATA
    imgDATA = {i: [ASSETS_PATH.joinpath(i), None] for i in ["app.gif", "bg.png"]}
    # Disabling UAC req(permanently) and Single instance check (win; temp?)
    # _checkInstance()

    app = Win()
    app.mainloop()


if __name__ == "__main__":
    main()

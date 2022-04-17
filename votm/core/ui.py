"""
Copyright (C) 2022 nozwock

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
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import font
from datetime import date
from tkinter import messagebox as mg
from tkinter.scrolledtext import ScrolledText

from votm.config import Config
from votm.utils.extras import matchHashedTextSHA256
from votm import __version__, __author__
from votm._license import __license__


class Tr_View(tk.Frame):
    def __init__(self, master, cols: list, data, mode=None):
        super().__init__(master)
        self.pack(fill="both", expand=1)
        self.master = master
        self.cols = cols
        self.data = data

        ttk.Style(self.master).map(
            "Treeview",
            foreground=self.fixed_map("foreground"),
            background=self.fixed_map("background"),
        )
        ttk.Style(self.master).configure(
            "Treeview", bd=0, highlightthickness=0, font=(None, 12)
        )
        ttk.Style(self.master).configure("Treeview.Heading", font=(None, 12))
        ttk.Style(self.master).layout(
            "Treeview", [("m.Treeview.treearea", {"sticky": "nswe"})]
        )

        top_f = tk.Frame(self)
        top_f.pack(side="top", fill="both", expand=1)
        view_f = tk.Frame(top_f, width=0, height=0)
        view_f.pack_propagate(0)
        view_f.pack(side="left", fill="both", expand=1)

        self.view = ttk.Treeview(view_f)
        self.view.pack(fill="both", expand=1)
        self.view.bind("<Button-1>", self.disable_col_resize)
        self.view.tag_configure("alt1", background="#F4F4F4")
        self.view.tag_configure("alt2", background="#EDEDED")

        if mode:
            if mode == "x":
                self.xbar = tk.Scrollbar(
                    self, orient=tk.HORIZONTAL, command=self.view.xview
                )
                self.xbar.pack(side="bottom", fill="x", padx=(0, 17))
                self.view.configure(xscrollcommand=self.xbar.set)
            elif mode == "y":
                self.ybar = tk.Scrollbar(
                    top_f, orient=tk.VERTICAL, command=self.view.yview
                )
                self.ybar.pack(side="left", fill="y")
                self.view.configure(yscrollcommand=self.ybar.set)
            else:
                pass
        else:
            self.xbar = tk.Scrollbar(
                self, orient=tk.HORIZONTAL, command=self.view.xview
            )
            self.ybar = tk.Scrollbar(top_f, orient=tk.VERTICAL, command=self.view.yview)
            self.xbar.pack(side="bottom", fill="x", padx=(0, 17))
            self.ybar.pack(side="left", fill="y")

            self.view.configure(xscrollcommand=self.xbar.set)
            self.view.configure(yscrollcommand=self.ybar.set)

        self.view["columns"] = self.cols
        self.view["show"] = "headings"

        for _ in self.cols:
            exec(f"self.view.heading('{_}', text='{_}')")
            exec(f"self.view.column('{_}', stretch=0)")

        for _ in self.view["columns"]:
            self.view.column(_, anchor="center")

        self.data = eval(str(self.data).replace("None", "'-'"))

        for _ in range(len(self.data)):
            if _ % 2 == 0:
                self.view.insert("", "end", values=self.data[_], tags="alt1")
            if _ % 2 != 0:
                self.view.insert("", "end", values=self.data[_], tags="alt2")

    @staticmethod
    def fixed_map(option):
        return [
            elm
            for elm in ttk.Style().map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")
        ]

    def disable_col_resize(self, event):
        if self.view.identify_region(event.x, event.y) == "separator":
            return "break"


class Ent_Box(tk.Toplevel):
    """Constructs a toplevel frame whose master is Win,
    It provides a interface for authentication system."""

    def __init__(
        self,
        master,
        txt: str = "Enter Password & Confirm to Continue.",
        icn: dir = None,
        chk: str = "passwd",
    ):
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.chk = chk
        self.protocol("WM_DELETE_WINDOW", self.s_cls)
        x = self.winfo_screenwidth() / 2 - 175
        y = self.winfo_screenheight() / 2 - 120
        """
        *For Center of Main Window->
        !app.winfo_x() + 400 - 175
        !app.winfo_y() + 225 - 70
        """
        self.geometry("350x140+%d+%d" % (x, y))
        self.title("Confirm")
        self.resizable(0, 0)
        self.config(background="#F5F6F7")
        self.iconphoto(True, icn)
        # self.iconbitmap(icn)
        self.grab_set()
        self.lift()
        self.focus_force()
        dsc = tk.Label(
            self,
            text=txt,
            font=("Segoe UI", 12),
            background="#FF3232",
            foreground="#EFEFEF",
        )
        dsc.pack(side="top", fill="x", pady=(0, 20), ipady=6)
        spc_reg = self.register(self.spc_check)
        ent_bx = ttk.Entry(
            self, show="*", validate="key", validatecommand=(spc_reg, "%S")
        )
        ent_bx.pack(side="top")
        ent_bx.focus_force()
        ent_bx.bind("<Return>", lambda event: self.ok_chk(ent_bx))
        btm_frm = tk.Frame(self, background="#F5F6F7")
        btm_frm.pack(side="bottom", pady=(0, 10))
        ok_btn = ttk.Button(btm_frm, text="Ok", command=lambda: self.ok_chk(ent_bx))
        ok_btn.pack(side="left", padx=(0, 30))
        can_btn = ttk.Button(btm_frm, text="Cancel", command=lambda: self.cncl())
        can_btn.pack(side="left")
        self.wait_window(self)

    @staticmethod
    def s_cls():
        """Prevents app from closing."""
        pass

    @staticmethod
    def spc_check(inp: str):
        """Restricts the use of whitespaces."""
        if inp != " ":
            return True
        else:
            return False

    def ok_chk(self, ent: tk.Entry):
        """Validates the passwords, and exits if matched."""
        if matchHashedTextSHA256(
            Config().load("security")[self.chk].strip(), ent.get().strip()
        ):
            self.destroy()
            self.flag = True
        else:
            ent.delete(0, tk.END)
            self.attributes("-topmost", 0)
            mg.showerror("Error", "Incorrect Key.", parent=self)
            self.attributes("-topmost", 1)

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
        x = self.winfo_screenwidth() / 2 - 198
        y = self.winfo_screenheight() / 2 - 100
        self.geometry("376x200+%d+%d" % (x, y))
        self.title("About")
        self.iconphoto(True, icn)
        # self.iconbitmap(icn)
        self.resizable(0, 0)
        self.grab_set()
        self.lift()
        self.focus_force()
        logo_lt = tk.Frame(self)
        logo_lt.pack(side="left", fill="y")
        about_rt = tk.Frame(self)
        about_rt.pack(side="left", fill="both", expand=1, pady=(10, 10), padx=(0, 10))
        about_tp = tk.Frame(about_rt, bd=2, relief="groove")
        about_tp.pack(side="top", fill="both", expand=1)

        DATAFILE = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "logo.png",
        )
        if not hasattr(sys, "frozen"):
            DATAFILE = os.path.join(os.path.dirname(__file__), DATAFILE)
        else:
            DATAFILE = os.path.join(sys.prefix, DATAFILE)
        self.img = tk.PhotoImage(file=DATAFILE)

        lgc = tk.Label(logo_lt, image=self.img)
        lgc.pack(ipadx=14, pady=(10, 0))
        label = tk.Label(
            about_tp, text="VOTM - Voting Master", font=("Segoe UI", 10, "bold")
        )
        label.pack(side="top", anchor="nw")
        ver = tk.Label(about_tp, text=f"Version {__version__}")
        ver.pack(side="top", anchor="nw")
        auth = tk.Label(about_tp, text=f"Copyright (C) 2019 {__author__}")
        auth.pack(side="top", anchor="nw", pady=(10, 0))
        bug_ttl = tk.Label(about_tp, text="Report bugs or request enhancements at:")
        bug_ttl.pack(side="top", anchor="nw", pady=(10, 0))
        url = "https://github.com/nozwock/votm/issues"
        bug_lnk = tk.Label(about_tp, text=url, fg="#6A00FF")
        bug_lnk.pack(side="top", anchor="nw")
        url_fnt = font.Font(bug_lnk, bug_lnk.cget("font"))
        url_fnt.configure(underline=1)
        bug_lnk.config(font=url_fnt)
        bug_lnk.bind("<ButtonRelease-1>", lambda event: webbrowser.open_new(url))
        bug_lnk.bind("<Enter>", lambda e: bug_lnk.config(fg="#9E5EFF"))
        bug_lnk.bind("<Leave>", lambda e: bug_lnk.config(fg="#6A00FF"))

        btn_frm = tk.Frame(about_rt)
        btn_frm.pack(side="top", pady=(10, 0), fill="both", expand=1)

        lcnse = ttk.Button(
            btn_frm, text="License", command=lambda: License(self, icn=icn)
        )
        lcnse.pack(side="left")
        ok = ttk.Button(btn_frm, text="Ok", command=lambda: self.destroy())
        ok.pack(side="right")
        self.wait_window(self)


class License(tk.Toplevel):
    def __init__(self, master, icn=None):
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.focus_force()
        self.title("Votm License")
        self.iconphoto(True, icn)
        # self.iconbitmap(icn)
        self.resizable(0, 0)
        self.grab_set()
        self.lift()
        x = self.winfo_screenwidth() / 2 - 280
        y = self.winfo_screenheight() / 2 - 220
        self.geometry("560x440+%d+%d" % (x, y))

        lcn_frm = tk.Frame(self, relief="groove", bd=2)
        lcn_frm.pack(side="top", fill="both", expand=1, pady=(10, 10), padx=(10, 10))
        self.lcn = ScrolledText(lcn_frm, font=("Segoe UI", 9), relief="flat")
        self.lcn.pack(fill="both", expand=1)
        self.lcn.insert(0.0, __license__)
        self.lcn.config(state="disabled")

        close_frm = tk.Frame(self)
        close_frm.pack(side="top", fill="both", expand=1, padx=(0, 10), pady=(0, 10))
        close = ttk.Button(close_frm, text="Close", command=lambda: self.destroy())
        close.pack(side="right")
        close.focus_set()
        self.wait_window(self)


if __name__ == "__main__":
    # ? Testing
    def do(win):
        win.destroy()
        sys.exit(0)

    Config().write_default()
    root = tk.Tk()
    root.attributes("-alpha", 0.0)
    ab = About(root)
    ab.protocol("WM_DELTE_WINDOW", do(root))
    root.mainloop()

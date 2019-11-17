"""
For changing configurations which will be used at the time of voting
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
import ctypes
import win32api
import xlsxwriter
import win32event
from shutil import copyfile
from os import path, remove
from datetime import date
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox as mg
from tabulate import tabulate
from winerror import ERROR_ALREADY_EXISTS
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename, askopenfilenames, askdirectory
from votmapi.logic import Dicto, Reg, Tokens, Crypt
from votmapi.__main__ import SECRET_KEY, ENV_KEY, __author__, __version__
from votmapi import (Default_Config, Write_Default, Access_Config, Sql_init, Yr_fle,
                     Cand_Check, Ent_Box, About)


class Root(tk.Tk):
    """Root Dummy Window."""
    DATAFILE = []

    def __init__(self):
        super().__init__()
        ttk.Style().theme_use('vista')
        self.title('Voting Master-Edit')
        self.attributes('-alpha', 0.0)
        self.ins_dat(['res\\v_r.ico', 'res\\ttle.png', 'res\\edtw.png', 'res\\rslw.png',
                      'res\\sttw.png', 'res\\edtb.png', 'res\\rslb.png', 'res\\sttb.png'])
        if not ctypes.windll.shell32.IsUserAnAdmin():
            self.withdraw()
            self.attributes('-topmost', 1)
            self.title('Error')
            mg.showwarning(
                'Error', 'This App requires Administrator Privileges to function properly.\nPlease Retry with Run as Administrator.', parent=self)
            self.destroy()
            sys.exit()
        self.iconbitmap(Root.DATAFILE[0])

    @classmethod
    def ins_dat(cls, iter_fle):
        """Instantiates Data files."""
        cls.DATAFILE.extend(iter_fle)
        for DATA in range(len(cls.DATAFILE)):
            if not hasattr(sys, 'frozen'):
                cls.DATAFILE[DATA] = path.join(
                    path.dirname(__file__), cls.DATAFILE[DATA])
            else:
                cls.DATAFILE[DATA] = path.join(
                    sys.prefix, cls.DATAFILE[DATA])


class Win(tk.Toplevel):
    """Main Window container."""
    SM_BG_HEX = '#F0F0F0'

    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(1)
        Write_Default()

        self.config(bg=Win.SM_BG_HEX, relief='groove',
                    highlightbackground='#000000', highlightcolor='#000000', highlightthickness=1)
        x = self.winfo_screenwidth()/2 - 400
        y = self.winfo_screenheight()/2 - 240
        self.geometry('800x480+%d+%d' % (x, y))
        self.resizable(0, 0)
        self.iconbitmap(Root.DATAFILE[0])
        ttk.Style().configure('TButton', focuscolor=self.cget('bg'))
        ttk.Style().configure('TCheckbutton', focuscolor=self.cget('bg'))
        ttk.Style().configure('TRadiobutton', focuscolor=self.cget('bg'))

        top_bar = tk.Frame(self, bg='#6A00FF', height=5)
        top_bar.pack(fill='x')
        top_bar.pack_propagate(0)
        top_bar.bind('<Button-1>', self.get_pos)
        top_bar.bind('<B1-Motion>', lambda event: self.geometry(
            f'+{event.x_root+self.xwin}+{event.y_root+self.ywin}'))
        min_btn = tk.Label(top_bar, text='█', bg='#6A00FF',
                           fg='#9E5EFF', font='Consolas 25')
        min_btn.pack(side='right')
        min_btn.bind(
            '<Enter>', lambda event: min_btn.config(foreground='#C39EFF'))
        min_btn.bind(
            '<Leave>', lambda event: min_btn.config(foreground='#9E5EFF'))
        min_btn.bind('<ButtonRelease-1>',
                     lambda event: (self.master.iconify(), self.withdraw()))
        self.bind('<Alt-F4>', lambda event: (self.master.destroy(), sys.exit()))
        self.master.bind('<FocusIn>', lambda event: self.lift())
        self.master.bind('<Map>', lambda event: (
            self.master.deiconify(), self.deiconify(), self.lift()))
        self.master.bind('<Unmap>', lambda event: (
            self.master.iconify(), self.withdraw()))

        self.navbar()
        self.frame_n = None
        self.replace_frame(Edit)

        if Ent_Box(self, icn=Root.DATAFILE[0]).get():
            pass
        else:
            self.master.destroy()
            sys.exit()

        if Write_Default.exist is 1:
            mg.showinfo('Voting Master',
                        'Some default configuration files has been saved.', parent=self)

    def replace_frame(self, cont: tk.Frame):
        """Cycle b/w frames."""
        frame = cont(self)
        self.cont = cont

        if cont == Edit:
            self.edit.config(image=self.edtb_img,
                             fg='#0077CC', bg='#EFEFEF')
            self.settings.config(image=self.stt_img,
                                 fg='#EFEFEF', bg='#0077CC')
            self.result.config(image=self.rsl_img,
                               fg='#EFEFEF', bg='#0077CC')
        elif cont == Result:
            self.result.config(image=self.rslb_img,
                               fg='#0077CC', bg='#EFEFEF')
            self.edit.config(image=self.edt_img,
                             fg='#EFEFEF', bg='#0077CC')
            self.settings.config(image=self.stt_img,
                                 fg='#EFEFEF', bg='#0077CC')
        elif cont == Settings:
            self.settings.config(image=self.sttb_img,
                                 fg='#0077CC', bg='#EFEFEF')
            self.edit.config(image=self.edt_img,
                             fg='#EFEFEF', bg='#0077CC')
            self.result.config(image=self.rsl_img,
                               fg='#EFEFEF', bg='#0077CC')

        if self.frame_n is not None:
            self.frame_n.pack_forget()

        self.frame_n = frame
        self.frame_n.pack(side='right', expand=True, fill='both')

    def navbar(self):
        """Left sided navbar for main window."""
        fl = tk.Frame(self, bg='#0077CC', width=223)
        fl.pack(side='left', expand=0, fill='y')
        fl.pack_propagate(0)
        # items_____________________________
        flt = tk.Frame(fl)
        flt.pack(side='top', fill='both', expand=1)
        flt.pack_propagate(0)
        self.lg_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[1]))
        lg_canv = tk.Canvas(flt, bd=0, highlightthickness=0)
        lg_canv.place(x=0, y=0, relheight=1, relwidth=1, anchor='nw')
        lg_canv.create_image(0, 0, image=self.lg_img, anchor='nw')

        flb = tk.Frame(fl, bg='#0077CC')
        flb.pack(side='bottom', fill='x', expand=1, anchor='s', pady=(1, 0))

        btxlb = tk.Button(flb, text='X', highlightthickness=0, bg='#FF3232', activebackground='#FF4C4C', takefocus=0,
                          relief='flat', bd=1, fg='#EFEFEF', height=2, command=lambda: self.desexit(), font=('Segoe UI', 10, 'bold'))
        btxlb.pack(side='left', fill='x', expand=1, anchor='s')

        bthlb = tk.Button(flb, text='?', highlightthickness=0, bg='#303030', activebackground='#6D6D6D', takefocus=0,
                          relief='flat', bd=1, fg='#EFEFEF', height=2, command=lambda: About(self, Root.DATAFILE[0]), font=('Segoe UI', 10, 'bold'))
        bthlb.pack(side='left', fill='x', expand=1, anchor='s')
        # contents_____________________________
        self.edt_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[2]))
        self.edtb_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[5]))
        self.edit = tk.Button(fl, text='  Edit      ', image=self.edt_img, compound='left', highlightthickness=0, activeforeground='#FFFFFF',
                              activebackground='#2888CC', relief='flat', bd=1, fg='#FFFFFF', bg='#0077CC',
                              font=('Segoe UI', 15, 'bold'), command=lambda: app.replace_frame(Edit), takefocus=0)
        self.edit.pack(side='top', ipady=20, fill='x')

        self.rsl_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[3]))
        self.rslb_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[6]))
        self.result = tk.Button(fl, text='  Result   ', image=self.rsl_img, compound='left', highlightthickness=0, activeforeground='#FFFFFF',
                                activebackground='#2888CC', relief='flat', bd=1, fg='#FFFFFF', bg='#0077CC',
                                font=('Segoe UI', 15, 'bold'), command=lambda: app.replace_frame(Result), takefocus=0)
        self.result.pack(side='top', ipady=20, fill='x')

        self.stt_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[4]))
        self.sttb_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[7]))
        self.settings = tk.Button(fl, text='  Settings', image=self.stt_img, compound='left', highlightthickness=0, activeforeground='#FFFFFF',
                                  activebackground='#2888CC', relief='flat', bd=1, fg='#FFFFFF', bg='#0077CC',
                                  font=('Segoe UI', 15, 'bold'), command=lambda: app.replace_frame(Settings), takefocus=0)
        self.settings.pack(side='top', ipady=20, fill='x')

        self.edit.bind(
            '<Button-1>', lambda event: (self.edit.config(image=self.edt_img), self.edit_bind()))
        self.edit.bind('<ButtonRelease-1>',
                       lambda event: (self.edit.unbind('<Enter>'), self.edit.unbind('<Leave>')))
        self.result.bind(
            '<Button-1>', lambda event: (self.result.config(image=self.rsl_img), self.result_bind()))
        self.result.bind('<ButtonRelease-1>',
                         lambda event: (self.result.unbind('<Enter>'), self.result.unbind('<Leave>')))
        self.settings.bind(
            '<Button-1>', lambda event: (self.settings.config(image=self.stt_img), self.settings_bind()))
        self.settings.bind('<ButtonRelease-1>',
                           lambda event: (self.settings.unbind('<Enter>'), self.settings.unbind('<Leave>')))

        lg_canv.bind('<Button-1>', self.get_pos)
        lg_canv.bind('<B1-Motion>', lambda event: self.geometry(
            f'+{event.x_root+self.xwin}+{event.y_root+self.ywin}'))

    def desexit(self):
        try:
            self.master.destroy()
            sys.exit()
        except:
            pass

    def edit_bind(self):
        self.edit.bind(
            '<Enter>', lambda e: self.edit.config(image=self.edt_img))
        if self.cont == Edit:
            self.edit.bind(
                '<Leave>', lambda e: self.edit.config(image=self.edtb_img))

    def result_bind(self):
        self.result.bind(
            '<Enter>', lambda e: self.result.config(image=self.rsl_img))
        if self.cont == Result:
            self.result.bind(
                '<Leave>', lambda e: self.result.config(image=self.rslb_img))

    def settings_bind(self):
        self.settings.bind(
            '<Enter>', lambda e: self.settings.config(image=self.stt_img))
        if self.cont == Settings:
            self.settings.bind(
                '<Leave>', lambda e: self.settings.config(image=self.sttb_img))

    def get_pos(self, event):
        self.xwin = self.winfo_x() - event.x_root
        self.ywin = self.winfo_y() - event.y_root


class Edit(tk.Frame):
    """Constructs a frame for changing candidate, class, etc. related data."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        self.config(bg=Win.SM_BG_HEX)
        ttk.Style().configure('TLabelframe.Label', font=('Segoe UI', 14))
        ttk.Style().configure('TLabelframe', bg=Win.SM_BG_HEX)
        ttk.Style().configure('m.TButton', font=('Segoe UI', 8),
                              highlightthickness=0, bd=0)
        ttk.Style().configure('TNotebook.Tab', font=('Segoe UI', 14),
                              focuscolor=ttk.Style().configure('.')['background'])

        self.tab = ttk.Notebook(self)
        cand = Candidates(self.tab)
        #cand.bind('<Visibility>', lambda e: cand.update())
        self.tab.add(cand, text=' Candidates ')
        pst = Posts(self.tab)
        self.tab.add(pst, text=' Posts ')
        clss = Classes(self.tab)
        self.tab.add(clss, text=' Classes ')
        sec = Sections(self.tab)
        self.tab.add(sec, text=' Sections ')
        self.tab.pack(side='right', expand=1, fill='both')
        self.tab.bind('<ButtonRelease-1>', lambda event: self.updt(event))

    @staticmethod
    def wrt(fle: int, cfg: str):
        """Writes Default config. files."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[fle]}', 'w') as f:
            cfg = Crypt().encrypt(str(cfg), SECRET_KEY)
            f.write(cfg)
            f.flush()

    @staticmethod
    def cur(cand: ttk.Combobox):
        """Selects 1st value in a combobox."""
        try:
            cand.current(0)
        except:
            pass

    def updt(self, event):
        slave = event.widget.winfo_children()[event.widget.index('current')]
        tabs = self.tab.tabs()

        tab_ins = [Candidates, Posts, Classes, Sections]

        for i in range(len(tab_ins)):
            if isinstance(slave, tab_ins[i]):
                c_ind = self.tab.index(tabs[i])
                self.tab.forget(tabs[i])
                del slave
                slave = tab_ins[i](self.tab)
                if c_ind < 3:
                    self.tab.insert(
                        c_ind, slave, text=' '+str(tab_ins[i]).split('.')[-1].strip("'>")+' ')
                else:
                    self.tab.add(slave, text=f'{tab_ins[i]}'.split(
                        '.')[-1].strip("'>"))
                self.tab.select(slave)
                break


class Candidates(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=Win.SM_BG_HEX)

        post = [eval(i)[0] for i in list(Access_Config().cand_config.keys())]
        cand_vw_ed = ttk.LabelFrame(self, text='View/Edit', padding=10)
        cand_vw_ed.pack(pady=(48, 10))
        cand_vw_ed_top = tk.Frame(cand_vw_ed, bg=Win.SM_BG_HEX)
        cand_vw_ed_top.pack(side='top', pady=(0, 10))
        cand_vw_ed_btm = tk.Frame(cand_vw_ed, bg=Win.SM_BG_HEX)
        cand_vw_ed_btm.pack(side='bottom')
        self.cand_vw_ed_pst = ttk.Combobox(
            cand_vw_ed_top, values=post, state='readonly', style='TCombobox')
        self.cand_vw_ed_pst.set('Post')
        self.cand_vw_ed_pst.pack(side='left', padx=(0, 10))
        self.cand_vw_ed_cand = ttk.Combobox(cand_vw_ed_top, state='readonly')
        self.cand_vw_ed_cand.set('Candidate')
        self.cand_vw_ed_cand.pack(side='left')
        str_reg = self.register(self.str_check)
        self.cand_vw_ed_ent = ttk.Entry(cand_vw_ed_btm, validate='key',
                                        validatecommand=(str_reg, '%S'))
        self.cand_vw_ed_ent.pack(side='left', padx=(0, 45))
        self.cand_vw_ed_ent.insert(1, 'Candidate')
        self.cand_vw_ed_ent.config(state='disabled')
        cand_vw_ed_btn = ttk.Button(cand_vw_ed_btm, text='Edit', style='m.TButton', command=lambda: self.wrt_edt(
            self.cand_vw_ed_pst, self.cand_vw_ed_cand, self.cand_vw_ed_ent), takefocus=0)
        cand_vw_ed_btn.pack(side='left', padx=(0, 25))

        cand_add = ttk.LabelFrame(self, text='Add', padding=10)
        cand_add.pack(pady=(0, 10))
        cand_add_pst = ttk.Combobox(cand_add, values=post, state='readonly')
        cand_add_pst.set('Post')
        cand_add_pst.pack(side='left', padx=(0, 10))
        cand_add_ent = ttk.Entry(cand_add, validate='key',
                                 validatecommand=(str_reg, '%S'))
        cand_add_ent.pack(side='left', padx=(0, 10))
        cand_add_ent.insert(1, 'Candidate')
        cand_add_ent.config(state='disabled')
        cand_add_btn = ttk.Button(cand_add, text='Add', style='m.TButton', command=lambda: (
            self.wrt_add(cand_add_pst, cand_add_ent), cand_add_ent.delete(0, tk.END)), takefocus=0)
        cand_add_btn.pack(side='left')

        cand_del = ttk.LabelFrame(self, text='Delete', padding=10)
        cand_del.pack(pady=(0, 20))
        self.cand_del_pst = ttk.Combobox(
            cand_del, values=post, state='readonly')
        self.cand_del_pst.set('Post')
        self.cand_del_pst.pack(side='left', padx=(0, 10))
        self.cand_del_cand = ttk.Combobox(cand_del, state='readonly')
        self.cand_del_cand.set('Candidate')
        self.cand_del_cand.pack(side='left', padx=(0, 10))
        cand_del_btn = ttk.Button(cand_del, text='Delete', style='m.TButton',
                                  command=lambda: self.cand_del(self.cand_del_pst, self.cand_del_cand), takefocus=0)
        cand_del_btn.pack(side='left')

        cand_clr = ttk.Button(self, text='Clear', padding=10,
                              style='m.TButton', command=lambda: self.clr(), takefocus=0)
        cand_clr.pack()
        self.cand_vw_ed_pst.bind('<<ComboboxSelected>>', lambda event: (self.cand_vw_ed_cand.config(values=Access_Config().cand_config[Cand_Check(self.cand_vw_ed_pst.get(
        )).get()]), self.cand_vw_ed_cand.set(''), Edit.cur(self.cand_vw_ed_cand), self.cand_vw_ed_ent.config(state='enabled'), self.cand_vw_ed_ent.delete(0, tk.END), self.cand_vw_ed_ent.insert(0, self.cand_vw_ed_cand.get())))
        self.cand_vw_ed_cand.bind('<<ComboboxSelected>>', lambda event: (
            self.cand_vw_ed_ent.delete(0, tk.END), self.cand_vw_ed_ent.insert(0, self.cand_vw_ed_cand.get())))
        cand_add_pst.bind('<<ComboboxSelected>>',
                          lambda event: (cand_add_ent.config(state='enabled'), cand_add_ent.delete(0, tk.END)))
        self.cand_del_pst.bind('<<ComboboxSelected>>', lambda event: (self.cand_del_cand.config(
            values=Access_Config().cand_config[Cand_Check(self.cand_del_pst.get()).get()]), self.cand_del_cand.set(''), Edit.cur(self.cand_del_cand)))

    @staticmethod
    def str_check(inp: str) -> bool:
        """Checks if the input is an alphabet or not."""
        if inp.isalpha():
            return True
        else:
            return False

    def clr(self):
        if mg.askokcancel('Confirm', 'Are you sure?', parent=self):
            Edit.wrt(0, Default_Config.candidate_config)
            app.replace_frame(Edit)
            mg.showinfo('Voting Master',
                        'Cleared, And set to default.', parent=self)

    def wrt_edt(self, key: ttk.Combobox, pos: ttk.Combobox, val: tk.Entry):
        """Writes changes to the Candidate file."""
        cfg = Access_Config().cand_config
        if val.get().strip() != '':
            try:
                cfg[Cand_Check(key.get()).get()][cfg[Cand_Check(key.get()).get()].index(
                    pos.get())] = val.get().strip()
                Edit.wrt(0, cfg)
                txt_val = pos.get()
                pos.set(val.get())
                pos.config(values=Access_Config(
                ).cand_config[Cand_Check(key.get()).get()])
                if self.cand_vw_ed_pst.get() == self.cand_del_pst.get():
                    self.cand_del_cand.config(values=Access_Config(
                    ).cand_config[Cand_Check(key.get()).get()])
                    if txt_val == self.cand_del_cand.get():
                        self.cand_del_cand.current(0)
            except:
                mg.showerror('Error', 'No Canidate was selected.', parent=self)
        else:
            mg.showerror('Error', 'Enter a value first.', parent=self)

    def wrt_add(self, key: ttk.Combobox, val: tk.Entry):
        """Adds value to the candidate file."""
        cfg = Access_Config().cand_config
        if val.get().strip() != '':
            try:
                cfg[Cand_Check(key.get()).get()].append(val.get().strip())
                Edit.wrt(0, cfg)
                self.cand_del_cand.config(values=Access_Config(
                ).cand_config[Cand_Check(key.get()).get()])
                self.cand_vw_ed_cand.config(values=Access_Config(
                ).cand_config[Cand_Check(key.get()).get()])
            except:
                mg.showerror('Error', 'Select a Post first.', parent=self)
        else:
            mg.showerror('Error', 'Enter a value first.', parent=self)

    def cand_del(self, key: ttk.Combobox, val: ttk.Combobox):
        """Deletes value from candidate file."""
        cfg = Access_Config().cand_config
        try:
            cfg[Cand_Check(key.get()).get()].remove(val.get())
            Edit.wrt(0, cfg)
            val.set('')
            val.config(values=Access_Config(
            ).cand_config[Cand_Check(key.get()).get()])
            val.current(0)
            if self.cand_vw_ed_pst.get() == self.cand_del_pst.get():
                self.cand_vw_ed_cand.config(values=Access_Config(
                ).cand_config[Cand_Check(key.get()).get()])
                self.cand_vw_ed_cand.current(0)
                self.cand_vw_ed_ent.delete(0, 'end')
                self.cand_vw_ed_ent.insert(0, self.cand_vw_ed_cand.get())
        except (ValueError, KeyError):
            val.set('')
            mg.showerror('Error', 'Candidate doesn\'t exist.', parent=self)
        except tk.TclError:
            pass


class Posts(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=Win.SM_BG_HEX)

        self.flpost = [
            f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]
        tag_reg = self.register(self.tag_check)
        pst_reg = self.register(self.pst_check)
        self.lbl_ent = 'Full-Post'
        self.lbl_tag = 'Post Tag'
        self.lbl_pst = 'Post'

        top_frm = tk.Frame(self, bg=Win.SM_BG_HEX)
        top_frm.pack(pady=(40, 10))

        pst_edt = ttk.LabelFrame(top_frm, text='Edit', padding=10)
        pst_edt.pack(side='left', padx=(0, 10))
        pst_edt_top = tk.Frame(pst_edt, bg=Win.SM_BG_HEX)
        pst_edt_top.pack(side='top', pady=(0, 10))
        pst_edt_btm = tk.Frame(pst_edt, bg=Win.SM_BG_HEX)
        pst_edt_btm.pack(side='bottom')
        self.pst_edt_pst = ttk.Combobox(
            pst_edt_top, values=self.flpost, state='readonly', style='TCombobox')
        self.pst_edt_pst.set(self.lbl_pst)
        self.pst_edt_pst.pack(side='left', padx=(0, 10))
        self.pst_edt_ent = ttk.Entry(pst_edt_btm)
        self.pst_edt_ent.pack(side='left', padx=(0, 10))
        self.pst_edt_ent.insert(1, self.lbl_ent)
        self.pst_edt_ent.config(state='disabled')
        self.pst_edt_tag = ttk.Entry(pst_edt_btm, width=8)
        self.pst_edt_tag.pack(side='left')
        self.pst_edt_tag.insert(1, self.lbl_tag)
        self.pst_edt_tag.config(state='disabled')
        pst_edt_btn = ttk.Button(
            pst_edt_top, text='Edit', style='m.TButton', takefocus=0, command=lambda: self.post_edt(self.pst_edt_pst, self.pst_edt_ent, self.pst_edt_tag))
        pst_edt_btn.pack(side='left')
        self.pst_edt_pst.bind('<<ComboboxSelected>>', lambda event: (self.pst_edt_ent.config(state='enabled'), self.pst_edt_tag.config(state='enabled'), self.pst_edt_ent.config(validate='key', validatecommand=(pst_reg, '%P')), self.pst_edt_tag.config(validate='key', validatecommand=(tag_reg, '%P')), self.pst_edt_pst.config(values=[
            f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]), self.pst_edt_ent.delete(0, 'end'), self.pst_edt_tag.delete(0, 'end'), self.pst_edt_ent.insert(0, self.pst_edt_pst.get().split(';')[0].strip()), self.pst_edt_tag.insert(0, self.pst_edt_pst.get().split(';')[-1].strip())))
        ######################################
        pst_add = ttk.LabelFrame(self, text='Add', padding=10)
        pst_add.pack(pady=(0, 10))
        self.pst_add_ent = ttk.Entry(pst_add)
        self.pst_add_ent.pack(side='left', padx=(0, 10))
        self.pst_add_ent.insert(1, self.lbl_ent)
        self.pst_add_tag = ttk.Entry(pst_add, width=8)
        self.pst_add_tag.pack(side='left', padx=(0, 10))
        self.pst_add_tag.insert(1, self.lbl_tag)
        pst_add_btn = ttk.Button(
            pst_add, text='Add', style='m.TButton', takefocus=0, command=lambda: (self.post_add(self.pst_add_ent, self.pst_add_tag), self.pst_add_ent.delete(0, 'end'), self.pst_add_tag.delete(0, 'end')))
        pst_add_btn.pack(side='left')
        self.pst_add_ent.bind('<Enter>', lambda e: (self.pst_add_ent.delete(0, 'end'), self.pst_add_ent.config(
            validate='key', validatecommand=(pst_reg, '%P')), self.pst_add_ent.unbind('<Enter>')))
        self.pst_add_tag.bind('<Enter>', lambda e: (self.pst_add_tag.delete(0, 'end'), self.pst_add_tag.config(
            validate='key', validatecommand=(tag_reg, '%P')), self.pst_add_tag.unbind('<Enter>')))
        ######################################
        btm_frm = tk.Frame(self, bg=Win.SM_BG_HEX)
        btm_frm.pack(pady=(0, 20))
        left_btm = tk.Frame(btm_frm, bg=Win.SM_BG_HEX)
        left_btm.pack(side='left', fill='y', expand=1, padx=(0, 10))

        pst_del = ttk.LabelFrame(left_btm, text='Delete', padding=10)
        pst_del.pack(side='top')
        self.pst_del_pst = ttk.Combobox(
            pst_del, values=self.flpost, state='readonly')
        self.pst_del_pst.set(self.lbl_pst)
        self.pst_del_pst.pack(side='left', padx=(0, 10))
        pst_del_btn = ttk.Button(
            pst_del, text='Delete', style='m.TButton', takefocus=0, command=lambda: self.post_del(self.pst_del_pst))
        pst_del_btn.pack(side='left')

        self.pst_del_pst.bind('<<ComboboxSelected>>', lambda e: self.pst_del_pst.config(values=[
            f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]))

        pst_clr = ttk.Button(left_btm, text='Default', padding=10,
                             style='m.TButton', command=lambda: self.clr(), takefocus=0)
        pst_clr.pack(side='top', fill='y', expand=1, pady=(20, 20))
        ########################################
        self.cfg = Dicto(Access_Config().cand_config)
        keys = list(self.cfg.get().keys())

        ordr_frm = ttk.LabelFrame(btm_frm, text='Rearrange', padding=10)
        ordr_frm.pack(side='left')
        self.pst_list = [f'{eval(i)[0]}; {eval(i)[-1]}' for i in keys]
        self.pst_var = tk.StringVar(value=self.pst_list)
        self.ordr_posts = tk.Listbox(
            ordr_frm, height=5, listvariable=self.pst_var, relief='groove', bd=2, highlightthickness=0)
        self.ordr_posts.pack(side='top')
        up_dn_frm = tk.Frame(ordr_frm)
        up_dn_frm.pack(side='top', fill='x', expand=1)
        up_btn = tk.Button(up_dn_frm, text='Up', relief='groove', highlightthickness=0, bg=Win.SM_BG_HEX, command=lambda: self.move_up(),
                           activebackground=Win.SM_BG_HEX, takefocus=0)
        up_btn.pack(side='left', fill='x', expand=1)
        dn_btn = tk.Button(up_dn_frm, text='Down', relief='groove', highlightthickness=0, bg=Win.SM_BG_HEX, command=lambda: self.move_down(),
                           activebackground=Win.SM_BG_HEX, takefocus=0)
        dn_btn.pack(side='left', fill='x', expand=1)

    def tag_check(self, inp):
        if ((inp.isalpha() or inp is '') and len(inp) <= 3) or inp in [i.split(';')[-1].strip() for i in self.flpost]:
            return True
        else:
            return False

    def pst_check(self, inp):
        if ((inp.isalpha() or inp is '') and len(inp) <= 15) or inp in [i.split(';')[0].strip() for i in self.flpost]:
            return True
        else:
            return False

    def clr(self):
        if mg.askokcancel('Confirm', 'Are you sure?', parent=self):
            Edit.wrt(0, Default_Config.candidate_config)
            app.replace_frame(Edit)
            mg.showinfo('Voting Master',
                        'Cleared, And set to default.', parent=self)

    def move_up(self, *args):
        try:
            self.idxs = self.ordr_posts.curselection()
            if not self.idxs:
                return
            for pos in self.idxs:
                if pos == 0:
                    continue
                val = self.ordr_posts.get(pos)
                self.ordr_posts.delete(pos)
                self.ordr_posts.insert(pos-1, val)
                self.pst_list.pop(pos)
                self.pst_list.insert(pos-1, val)
                self.ordr_posts.selection_set(pos-1)
                key = str([val.split(';')[0].strip(),
                           val.split(';')[-1].strip()])
                item = self.cfg.get()[key]
                self.cfg.remove(key)
                self.cfg.insert(pos-1, key, item)

                Edit.wrt(0, self.cfg)
                self.flpost = [
                    f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]
                self.pst_edt_pst.config(values=self.flpost)
                self.pst_edt_pst.current(0)
                self.pst_del_pst.config(values=self.flpost)
                self.pst_del_pst.current(0)
        except:
            raise

    def move_down(self, *args):
        try:
            self.idxs = self.ordr_posts.curselection()
            if not self.idxs:
                return
            for pos in self.idxs:
                if pos == len(self.pst_list)-1:
                    continue
                val = self.ordr_posts.get(pos)
                self.ordr_posts.delete(pos)
                self.ordr_posts.insert(pos+1, val)
                self.pst_list.pop(pos)
                self.pst_list.insert(pos+1, val)
                self.ordr_posts.selection_set(pos+1)
                key = str([val.split(';')[0].strip(),
                           val.split(';')[-1].strip()])
                item = self.cfg.get()[key]
                self.cfg.remove(key)
                self.cfg.insert(pos+1, key, item)
                Edit.wrt(0, self.cfg)
                self.flpost = [
                    f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]
                self.pst_edt_pst.config(values=self.flpost)
                self.pst_edt_pst.current(0)
                self.pst_del_pst.config(values=self.flpost)
                self.pst_del_pst.current(0)
        except:
            raise

    def post_edt(self, key, ent, tag):
        if ent.get() != '' and tag.get() != '':
            cfg = Dicto(Access_Config().cand_config)
            _tag = [eval(i)[-1]
                    for i in list(cfg.get().keys()) if eval(i)[-1] != key.get().split(';')[-1].strip()]
            if tag.get() not in _tag:
                cmb = key
                _key = f'{[ent.get(), tag.get().upper()]}'
                key = str([key.get().split(';')[0].strip(),
                           key.get().split(';')[-1].strip()])
                con = cfg.get().get(key)
                ind = list(cfg.get().keys()).index(key)
                cfg.remove(key)
                #del cfg.get()[key]
                cfg.insert(ind, _key, con)
                #cfg.get()[_key] = con
                self.cfg = Dicto(cfg.get())
                self.pst_list = [
                    f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(self.cfg.get().keys())]
                self.ordr_posts.delete(ind)
                self.ordr_posts.insert(
                    ind, [f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(self.cfg.get().keys())][ind])
                Edit.wrt(0, cfg.get())
                val = [
                    f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]
                self.pst_del_pst.config(values=val)
                self.pst_del_pst.current(0)
                cmb.config(values=val)
                cmb.current(ind)
                mg.showinfo('Voting Master',
                            'Post has been edited.', parent=self)
            else:
                mg.showwarning(
                    'Error', 'This Tag already exists.', parent=self)

    def post_add(self, ent, tag):
        if ent.get() not in ['', self.lbl_ent] and tag.get() not in ['', self.lbl_tag]:
            cfg = Access_Config().cand_config
            _tag = [eval(i)[-1] for i in list(cfg.keys())]
            if tag.get() not in _tag:
                key = f'{[ent.get(), tag.get().upper()]}'
                cfg[key] = []
                if len(cfg) <= 8:
                    self.cfg = Dicto(cfg)
                    self.pst_list = [
                        f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(self.cfg.get().keys())]
                    self.ordr_posts.insert(
                        'end', [f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(self.cfg.get().keys())][-1])
                    Edit.wrt(0, cfg)
                    val = [
                        f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]
                    self.pst_del_pst.config(values=val)
                    self.pst_del_pst.current(0)
                    self.pst_edt_pst.config(values=val)
                    self.pst_edt_pst.current(0)
                    self.pst_edt_ent.config(state='enabled')
                    self.pst_edt_tag.config(state='enabled')
                    self.pst_edt_ent.delete(0, 'end')
                    self.pst_edt_tag.delete(0, 'end')
                    self.pst_edt_ent.insert(
                        0, self.pst_edt_pst.get().split(';')[0].strip())
                    self.pst_edt_tag.insert(
                        0, self.pst_edt_pst.get().split(';')[-1].strip())
                    mg.showinfo('Voting Master',
                                'Post has been added.', parent=self)
                else:
                    mg.showerror(
                        'Error', 'No. of Max posts is 8!', parent=self)
            else:
                mg.showwarning(
                    'Error', 'This Tag already exists.', parent=self)
        else:
            mg.showerror('Error', 'Incorrect Entry.', parent=self)

    def post_del(self, ent):
        if ent.get() != self.lbl_pst:
            cfg = Dicto(Access_Config().cand_config)
            key = str([ent.get().split(';')[0].strip(),
                       ent.get().split(';')[-1].strip()])
            if len(cfg.get()) > 1:
                ind = list(cfg.get().keys()).index(key)
                cfg.remove(key)
                self.cfg = Dicto(cfg.get())
                self.pst_list = list(self.cfg.get().keys())
                self.ordr_posts.delete(ind)
                Edit.wrt(0, cfg)
                val = [
                    f'{eval(i)[0]}; {eval(i)[-1]}' for i in list(Access_Config().cand_config.keys())]
                ent.config(values=val)
                self.pst_edt_pst.config(values=val)
                self.pst_edt_pst.current(0)
                ent.current(0)
                self.pst_edt_ent.delete(0, 'end')
                self.pst_edt_tag.delete(0, 'end')
                self.pst_edt_ent.insert(
                    0, self.pst_edt_pst.get().split(';')[0].strip())
                self.pst_edt_tag.insert(
                    0, self.pst_edt_pst.get().split(';')[-1].strip())
                mg.showinfo('Voting Master',
                            'Post has been deleted.', parent=self)
            else:
                mg.showwarning(
                    'Error', 'Can\'t delete, Atleast 1 Post should exist.', parent=self)


class Classes(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=Win.SM_BG_HEX)
        clss_lst = list(Access_Config().clss_config.keys())

        clss_add = ttk.LabelFrame(self, text='Add', padding=10)
        clss_add.pack(pady=(100, 40))
        clss_reg = self.register(self.clss_check)
        self.clss_add_cls = ttk.Entry(clss_add)
        self.clss_add_cls.insert(0, 'Class')
        self.clss_add_cls.pack(side='left', padx=(0, 10))
        clss_add_btn = ttk.Button(clss_add, text='Add', style='m.TButton', command=lambda: (
            self.add_clss(), self.clss_add_cls.delete(0, tk.END)), takefocus=0)
        clss_add_btn.pack(side='left')

        clss_del = ttk.LabelFrame(self, text='Delete', padding=10)
        clss_del.pack(pady=(0, 40))
        self.clss_del_clss = ttk.Combobox(
            clss_del, values=clss_lst, state='readonly')
        self.clss_del_clss.set('Class')
        self.clss_del_clss.pack(side='left', padx=(0, 10))
        clss_del_btn = ttk.Button(
            clss_del, text='Delete', style='m.TButton', takefocus=0, command=lambda: self.del_clss())
        clss_del_btn.pack(side='left')

        clss_def = ttk.Button(self, text='Default', padding=10,
                              style='m.TButton', command=lambda: self.set_dft(), takefocus=0)
        clss_def.pack()

        self.clss_add_cls.bind('<Enter>', lambda e: (self.clss_add_cls.delete(0, 'end'), self.clss_add_cls.config(
            validate='key', validatecommand=(clss_reg, '%P')), self.clss_add_cls.unbind('<Enter>')))

    def clss_check(self, inp):
        try:
            if list(inp)[0] != '0':
                if len(inp) == 1:
                    if ((inp.isdigit() or inp is '') and len(inp) <= 2):
                        return True
                    else:
                        return False
                elif list(inp)[0] == '1' and len(inp) == 2 or inp is '':
                    if list(inp)[-1] in ['1', '2', '0']:
                        if ((inp.isdigit() or inp is '') and len(inp) <= 2):
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except:
            return True

    def set_dft(self):
        if mg.askokcancel('Confirm', 'Are you sure?', parent=self):
            Edit.wrt(1, Default_Config.clss_config)
            app.replace_frame(Edit)
            mg.showinfo('Voting Master', 'Set to Default.', parent=self)

    def add_clss(self):
        cfg = Dicto(Access_Config().clss_config)
        val = self.clss_add_cls.get()
        clss = list(cfg.get().keys())
        if val != '':
            if int(val) not in clss:
                clss.append(int(val))
                clss.sort()
                ind = clss.index(int(val))
                cfg.insert(ind, int(val), ['A', 'B', 'C', 'D'])
                Edit.wrt(1, str(cfg.get()))
                self.clss_del_clss.config(values=list(
                    Access_Config().clss_config.keys()))
                mg.showinfo('Voting Master',
                            'Class has been added.', parent=self)
            else:
                mg.showerror('Error', 'Class already exists.', parent=self)

    def del_clss(self):
        cfg = Access_Config().clss_config
        val = self.clss_del_clss.get()
        if val != 'Class':
            if len(cfg) > 4:
                del cfg[int(val)]
                Edit.wrt(1, str(cfg))
                self.clss_del_clss.config(values=list(
                    Access_Config().clss_config.keys()))
                self.clss_del_clss.current(0)
                mg.showinfo('Voting Master',
                            'Class has been Deleted.', parent=self)
            else:
                mg.showwarning(
                    'Voting Master', 'Too Many Classes has been deleted.', parent=self)
        else:
            mg.showerror(
                'Error', 'Invalid, Select a Class first.', parent=self)


class Sections(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=Win.SM_BG_HEX)
        clss_lst = list(Access_Config().clss_config.keys())

        clss_vw = ttk.LabelFrame(self, text='View', padding=10)
        clss_vw.pack(pady=(30, 10))
        self.clss_vw_clss = ttk.Combobox(
            clss_vw, values=clss_lst, state='readonly')
        self.clss_vw_clss.set('Class')
        self.clss_vw_clss.pack(pady=(0, 10))
        self.clss_vw_sec = ScrolledText(clss_vw, wrap=tk.WORD, font=(
            'Segue UI', 8), width=30, height=5, relief='flat', bg=Win.SM_BG_HEX)
        self.clss_vw_sec.insert(0.0, 'Sections Here')
        self.clss_vw_sec.pack()
        self.clss_vw_sec.config(state='disabled')

        clss_add = ttk.LabelFrame(self, text='Add', padding=10)
        clss_add.pack(pady=(0, 10))
        clss_add_clss = ttk.Combobox(
            clss_add, values=clss_lst, state='readonly')
        clss_add_clss.set('Class')
        clss_add_clss.pack(side='left', padx=(0, 10))
        one_reg = self.register(self.one_check)
        self.clss_add_sec = ttk.Entry(clss_add)
        self.clss_add_sec.insert(0, 'Section')
        self.clss_add_sec.config(state='disabled')
        self.clss_add_sec.pack(side='left', padx=(0, 10))
        clss_add_btn = ttk.Button(clss_add, text='Add', style='m.TButton', command=lambda: (
            self.clss_add(clss_add_clss, self.clss_add_sec), self.clss_add_sec.delete(0, tk.END)), takefocus=0)
        clss_add_btn.pack(side='left')

        clss_del = ttk.LabelFrame(self, text='Delete', padding=10)
        clss_del.pack(pady=(0, 10))
        self.clss_del_clss = ttk.Combobox(
            clss_del, values=clss_lst, state='readonly')
        self.clss_del_clss.set('Class')
        self.clss_del_clss.pack(side='left', padx=(0, 10))
        self.clss_del_sec = ttk.Combobox(clss_del, state='readonly')
        self.clss_del_sec.set('Section')
        self.clss_del_sec.pack(side='left', padx=(0, 10))
        clss_del_btn = ttk.Button(clss_del, text='Delete', style='m.TButton',
                                  command=lambda: self.clss_del(self.clss_del_clss, self.clss_del_sec), takefocus=0)
        clss_del_btn.pack(side='left')

        clss_def = ttk.Button(self, text='Default', padding=10,
                              style='m.TButton', command=lambda: self.set_dft(), takefocus=0)
        clss_def.pack()
        self.clss_vw_clss.bind('<<ComboboxSelected>>', lambda event: (self.clss_vw_sec.config(state='normal'), self.clss_vw_sec.delete(
            0.0, tk.END), self.clss_vw_sec.insert(0.0, Access_Config().clss_config[int(self.clss_vw_clss.get())]), self.clss_vw_sec.config(state='disabled')))
        clss_add_clss.bind('<<ComboboxSelected>>',
                           lambda event: (self.clss_add_sec.config(state='enabled', validate='key', validatecommand=(one_reg, '%P')), self.clss_add_sec.delete(0, tk.END)))
        self.clss_del_clss.bind('<<ComboboxSelected>>', lambda event: (self.clss_del_sec.config(values=Access_Config(
        ).clss_config[int(self.clss_del_clss.get())]), self.clss_del_sec.set(''), Edit.cur(self.clss_del_sec)))

    def one_check(self, inp: str) -> bool:
        """Check to allow only 1 alphabet."""
        if (len(inp+self.clss_add_sec.get()) <= 1 and (inp.isalpha()) or inp is ''):
            return True
        else:
            return False

    def set_dft(self):
        if mg.askokcancel('Confirm', 'Are you sure?', parent=self):
            Edit.wrt(1, Default_Config.clss_config)
            app.replace_frame(Edit)
            mg.showinfo('Voting Master', 'Set to Default.', parent=self)

    def clss_del(self, key: ttk.Combobox, val: ttk.Combobox):
        """Deletes value from class file."""
        cfg = Access_Config().clss_config
        try:
            cfg[int(key.get())].remove(val.get())
            Edit.wrt(1, cfg)
            val.set('')
            val.config(values=Access_Config().clss_config[int(key.get())])
            val.current(0)
            if key.get() == self.clss_vw_clss.get():
                self.clss_vw_sec.config(state='normal')
                self.clss_vw_sec.delete(0.0, 'end')
                self.clss_vw_sec.insert(0.0, Access_Config(
                ).clss_config[int(self.clss_vw_clss.get())])
                self.clss_vw_sec.config(state='disabled')
        except (ValueError, KeyError):
            val.set('')
            mg.showerror('Error', 'Section doesn\'t exist.', parent=self)
        except tk.TclError:
            pass

    def clss_add(self, key: ttk.Combobox, val: tk.Entry):
        """Adds value to the class file."""
        cfg = Access_Config().clss_config
        if val.get().strip() != '':
            if val.get() not in cfg[int(key.get())]:
                try:
                    cfg[int(key.get())].append(val.get().upper())
                    cfg[int(key.get())].sort()
                    Edit.wrt(1, cfg)
                    if key.get() == self.clss_vw_clss.get():
                        self.clss_vw_sec.config(state='normal')
                        self.clss_vw_sec.delete(0.0, 'end')
                        self.clss_vw_sec.insert(0.0, Access_Config(
                        ).clss_config[int(self.clss_vw_clss.get())])
                        self.clss_vw_sec.config(state='disabled')
                    if key.get() == self.clss_del_sec.get():
                        self.clss_del_sec.config(values=Access_Config(
                        ).clss_config[int(self.clss_del_clss.get())])
                        self.clss_del_sec.current(0)
                except:
                    mg.showerror('Error', 'Select a Class first.', parent=self)
            else:
                mg.showerror('Error', 'Section already exists.', parent=self)
        else:
            mg.showerror('Error', 'Enter a value first.', parent=self)


class Result(tk.Frame):
    """Constructs a frame for fetching result & merging tables from the database."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure('TLabelframe.Label', font=('Segoe UI', 14))
        ttk.Style().configure('m.TButton', font=('Segoe UI', 10))
        self.config(bg=Win.SM_BG_HEX)
        # Merge Frame______________________
        self.mrg_lblfrm = ttk.Labelframe(self, text='Merge', padding=10)
        self.shw_lblfrm = ttk.Labelframe(self, text='Show', padding=10)
        self.mrg_lblfrm.pack(pady=(60, 10))
        self.shw_lblfrm.pack()

        mrg_left = tk.Frame(self.mrg_lblfrm, bg=Win.SM_BG_HEX)
        mrg_left.pack(side='left', padx=(0, 10))
        mrg_right = tk.Frame(self.mrg_lblfrm, bg=Win.SM_BG_HEX)
        mrg_right.pack(side='right')
        self.mrg_drctr = tk.Listbox(
            mrg_left, height=5, relief='groove', bd=2, highlightthickness=0)
        self.mrg_drctr.pack(side='top')
        mrg_clr = tk.Button(mrg_left, text='Remove', relief='groove', highlightthickness=0, bg=Win.SM_BG_HEX,
                            activebackground=Win.SM_BG_HEX, command=lambda: self.rmv_item(), takefocus=0)
        mrg_clr.pack(side='top', fill='x')
        mrg_brws = ttk.Button(mrg_right, text='Browse',
                              command=lambda: self.opn_mrg_fles(), takefocus=0)
        mrg_brws.pack(side='top', pady=(10, 10), fill='x')
        mrg_shw = ttk.Button(mrg_right, text='Merge',
                             command=lambda: self.do_mrg(), takefocus=0)
        mrg_shw.pack(side='top', pady=(0, 10), fill='x')
        mrg_conv_exl = ttk.Button(
            mrg_right, text='Export Merge File', command=lambda: self.crt_mrg_fle(), takefocus=0)
        mrg_conv_exl.pack(side='top', pady=(0, 10))
        # Show Frame______________________
        self.shw_db = ttk.Combobox(
            self.shw_lblfrm, state='readonly', values=Yr_fle().yr)
        self.shw_db.set('Database')
        self.shw_lblfrm_top = tk.Frame(self.shw_lblfrm, bg=Win.SM_BG_HEX)
        self.shw_lblfrm_sup = tk.Frame(self.shw_lblfrm, bg=Win.SM_BG_HEX)
        self.shw_shw = ttk.Button(
            self.shw_lblfrm, text='Show', state='disabled', command=lambda: self.shw_res(), takefocus=0)
        self.shw_db.pack(side='top', pady=(0, 10))
        self.shw_lblfrm_top.pack(side='top', pady=(0, 10))
        self.shw_lblfrm_sup.pack(side='top', pady=(0, 10))
        self.shw_shw.pack(side='bottom')

        self.shw_opt_var = tk.IntVar()
        self.shw_chk_var_tchr = tk.IntVar()
        self.shw_chk_var_std = tk.IntVar()
        self.shw_chk_var_clss = tk.IntVar()
        self.shw_chk_var_sec = tk.IntVar()
        shw_opt_cstm = ttk.Radiobutton(
            self.shw_lblfrm_top, text='Custom', state='disabled', variable=self.shw_opt_var, value=0, command=lambda: self.opt_call(shw_chk_clss))
        shw_opt_all = ttk.Radiobutton(self.shw_lblfrm_top, text='Select All', state='disabled',
                                      variable=self.shw_opt_var, value=1, command=lambda: self.opt_call(shw_chk_clss))
        shw_chk_tchr = ttk.Checkbutton(self.shw_lblfrm_sup, text='Staff', state='disabled', takefocus=0, variable=self.shw_chk_var_tchr, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_std = ttk.Checkbutton(self.shw_lblfrm_sup, text='Student', state='disabled', takefocus=0, variable=self.shw_chk_var_std, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_clss = ttk.Checkbutton(self.shw_lblfrm_sup, text='Class', state='disabled', takefocus=0, variable=self.shw_chk_var_clss, command=lambda: (
            self.chk_clss_sec(self.shw_chk_var_clss, shw_chk_clss, self.shw_chk_var_sec), self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_sec = ttk.Checkbutton(self.shw_lblfrm_sup, text='Section', state='disabled', takefocus=0, variable=self.shw_chk_var_sec, command=lambda: (
            self.chk_clss_sec(self.shw_chk_var_clss, shw_chk_clss, self.shw_chk_var_sec), self.chk_btn(), self.shw_opt_var.set(0)))
        shw_opt_cstm.pack(side='left')
        shw_opt_all.pack(side='left')
        shw_chk_tchr.pack(side='left')
        shw_chk_std.pack(side='left')
        shw_chk_clss.pack(side='left')
        shw_chk_sec.pack(side='left')

        self.shw_db.bind("<<ComboboxSelected>>", lambda event: (self.do_enb(
            shw_opt_cstm, shw_opt_all, shw_chk_tchr, shw_chk_std, shw_chk_clss, shw_chk_sec), self.do_upd(), self.chk_btn()))

    def exec_do(self):
        self.chk_btn()
        self.shw_opt_var.set(0)

    def do_enb(self, *args):
        for i in args:
            i.config(state='enabled')
        self.shw_db.unbind("<<ComboboxSelected>>")
        self.shw_db.bind("<<ComboboxSelected>>", lambda event: (
            self.do_upd(), self.chk_btn()))

    def do_upd(self):
        self.mrg_lblfrm.pack(pady=(40, 10))
        if self.shw_db.get() != 'merged':
            cnd = Sql_init(0, yr=self.shw_db.get()).db_cands()
        else:
            cnd = Sql_init(0, dtb=1).db_cands()
        lcl_cnd = [eval(i) for i in list(Access_Config().cand_config.keys())]
        cn = 1

        try:
            _list = self.main.winfo_children()
            for item in _list:
                if item.winfo_children():
                    _list.extend(item.winfo_children())
            for item in _list:
                item.pack_forget()
            self.main.pack_forget()
        except:
            pass

        self.args = []
        self.main = tk.Frame(self.shw_lblfrm, bg=Win.SM_BG_HEX)
        self.main.pack()
        self.shw_lblfrm_btw = tk.Frame(self.main, bg=Win.SM_BG_HEX)
        self.shw_lblfrm_btm = tk.Frame(self.main, bg=Win.SM_BG_HEX)
        self.shw_lblfrm_btw.pack(side='top', pady=(0, 10))
        self.shw_lblfrm_btm.pack(side='top', pady=(0, 10))
        for j in range(len(cnd)):
            text = str(list(cnd.keys())[j])
            for _ in range(len(lcl_cnd)):
                if text == lcl_cnd[_][-1]:
                    text = lcl_cnd[_][0]
                    break
            if cn <= 4:
                pos = self.shw_lblfrm_btw
                self.shw_lblfrm_btw.pack(side='top', pady=(0, 10))
                self.shw_lblfrm_btm.pack_forget()
            else:
                pos = self.shw_lblfrm_btm
                self.shw_lblfrm_btw.pack(side='top', pady=(0, 10))
                self.shw_lblfrm_btm.pack(side='top', pady=(0, 10))
            exec(f'self.shw_chk_var_{str(list(cnd.keys())[j])} = tk.IntVar()')
            exec(
                f'shw_chk_{str(list(cnd.keys())[j])} = ttk.Checkbutton(pos, text=\'{text}\', takefocus=0, variable=self.shw_chk_var_{str(list(cnd.keys())[j])}, command=self.exec_do)')
            exec(f'shw_chk_{str(list(cnd.keys())[j])}.pack(side=\'left\')')
            cn += 1

    def crt_args(self):
        if self.shw_db.get() != 'merged':
            cnd = Sql_init(0, yr=self.shw_db.get()).db_cands()
        else:
            cnd = Sql_init(0, dtb=1).db_cands()
        del self.args
        self.args = []
        try:
            del kwargs
        except:
            pass
        kwargs = []
        for i in range(len(cnd)):
            exec(
                f'self.args.append(self.shw_chk_var_{str(list(cnd.keys())[i])}.get())')
            exec(
                f'kwargs.append(self.shw_chk_var_{str(list(cnd.keys())[i])})')
        return self.args, kwargs

    def crt_mrg_fle(self):
        """Creates a merge file through a dialog box."""
        try:
            _, cols = Sql_init(0).cols(date.today().strftime('%Y'))
            fle = Sql_init(0).gen_mrg_fle()
            _ = [list(tup) for tup in list(cols)]
            cols = []
            for i in range(len(_)):
                apnd_val = [x.replace('NULL', 'DEFAULT(NULL)') or x for x in _[
                    i] if not isinstance(x, int)]
                cols.append(apnd_val)
            fdir = path.dirname(__file__)
            fname = asksaveasfilename(
                parent=self, initialdir=fdir, filetypes=(('Merge Files', '*.mrg'),))
            if fname != '':
                dir_fle = f'{fname}'
                if not dir_fle.endswith('.mrg'):
                    dir_fle += '.mrg'
                with open(dir_fle, 'w') as f:
                    f.write('((\n')
                    for i in cols:
                        f.write(f'{str(tuple(i))},\n')
                    f.write('),\n(\n')
                    f.flush()
                    for i in fle:
                        f.write(f'{str(i)},\n')
                        f.flush()
                    f.write('))')
                with open(dir_fle, 'r') as f:
                    rd = Crypt().encrypt(str(f.read()), SECRET_KEY)
                with open(dir_fle, 'w') as f:
                    f.write(rd)
                    mg.showinfo(
                        'Voting Master', 'Merge file has been generated.', parent=self)

        except:
            mg.showerror(
                'Error', 'No Data exists to create Merge file from.', parent=self)

    def opn_mrg_fles(self):
        """Opens a merge file through a dialog box."""
        fdir = path.dirname(__file__)
        self.fname = askopenfilenames(
            parent=self, initialdir=fdir, filetypes=(('Merge Files', '*.mrg'),))
        for item in range(len(self.fname)):
            if self.fname[item] not in self.mrg_drctr.get(0, tk.END):
                self.mrg_drctr.insert(tk.END, self.fname[item])

    def rmv_item(self):
        """Removes selected merge file directory from the listbox."""
        try:
            ind = self.mrg_drctr.curselection()[0]
            del list(self.fname)[ind]
            self.mrg_drctr.delete(ind)
        except:
            pass

    def do_mrg(self):
        """Performs merging in the logic module, from the data proccessed in main."""
        mrg = self.mrg_drctr.get(0, tk.END)
        if mrg != ():
            if mg.askokcancel('Confirm', 'Are you sure?', parent=self):
                mrg_tbl_n = [(sr.replace('.mrg', '').split('/'))[-1]
                             for sr in mrg]  # File Names
                mrg_tbl_data = []
                for dirc in mrg:
                    with open(dirc, 'r') as f:
                        mrg_tbl_data.append(
                            eval(Crypt().decrypt(str(f.read()), SECRET_KEY)))
                Sql_init(0, dtb=1).mrg_dtb_res(mrg_tbl_n, mrg_tbl_data)
                mg.showinfo('Voting Master', 'Merging is Done.', parent=self)
        else:
            mg.showwarning('Voting Master',
                           'No Merge file is selected!', parent=self)

    def shw_res(self):
        """Creates a string from a list of columns to be shown and it is passed to the Result window."""
        try:
            if self.shw_db.get() != 'merged':
                pst_cand = Sql_init(0).cols(self.shw_db.get())[0][4:]
            else:
                pst_cand = Sql_init(0, dtb=1).cols(self.shw_db.get())[0][4:]
            shrt = [i[:3].strip('_') for i in pst_cand]
            count = []
            for i in shrt:
                if i not in count:
                    count.append(i)
            vals = ['STAFF', 'STUDENT', 'CLASS', 'SEC']
            for i in range(len(count)):
                exec(
                    f"{shrt[i].lower()}=(str([i for i in pst_cand if i.startswith('{shrt[i]}')]).lstrip('[').rstrip(']')).replace(\"'\", \"\")")
                exec(f'vals.append({shrt[i].lower()})')

            args = []
            for i in range(len(self.var_val_lst)):
                if self.var_val_lst[i] == 1:
                    args.append(vals[i])
            args = (str(args).lstrip('[').rstrip(']')).replace("'", "")

            _ = Sql_init(0, yr=self.shw_db.get()).result(args)[0]
            assert (_ != [])
            # Abobe just to check for exception

            Result_Show_Sep(self.shw_db.get(), args).mainloop()
        except:
            mg.showerror(
                'Error', 'No Result found!', parent=self)

    def chk_clss_sec(self, val: tk.IntVar, obj: tk.Checkbutton, self_val: tk.IntVar):
        """Makes sure that "class" button can't be turned off while "section" button is on."""
        if self_val.get() == 1:
            val.set(1)
            obj.bind('<Button-1>', lambda event: 'break')
        else:
            obj.bind('<Button-1>', lambda event: self.freeze)

    @staticmethod
    def freeze():
        pass

    def chk_btn(self):
        """Keeps the "show" button disabled unless (a checkbutton & year/database) is selected."""
        self.var_val_lst = [self.shw_chk_var_tchr.get(), self.shw_chk_var_std.get(
        ), self.shw_chk_var_clss.get(), self.shw_chk_var_sec.get()]
        self.var_val_lst.extend(self.crt_args()[0])
        if self.shw_db.get() in Yr_fle.yr:
            if any(self.var_val_lst) == 0:
                self.shw_shw.config(state='disabled')
            else:
                self.shw_shw.config(state='enabled')

    def opt_call(self, clss: ttk.Combobox):
        """Tickmarks all for select all and change to custom for any changes."""
        var_lst = [self.shw_chk_var_tchr, self.shw_chk_var_std,
                   self.shw_chk_var_clss, self.shw_chk_var_sec]
        var_lst.extend(self.crt_args()[-1])
        if self.shw_opt_var.get() == 1:
            for v in var_lst:
                v.set(1)
            clss.bind('<Button-1>', lambda event: 'break')
        self.chk_btn()


class Settings(tk.Frame):
    """Constructs a frame for to delete database and to change password."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)

        ttk.Style().configure('TLabelframe.Label', font=('Segoe UI', 14))
        ttk.Style().configure('m.TButton', font=('Segoe UI', 10))
        self.config(bg=Win.SM_BG_HEX)

        frm_top = tk.Frame(self, bg=Win.SM_BG_HEX)
        frm_top.pack(side='top', pady=(60, 0))
        frm_btm = tk.Frame(self, bg=Win.SM_BG_HEX)
        frm_btm.pack(side='top', pady=(40, 0))

        lbl_hed_dtb = ttk.LabelFrame(
            frm_top, text='Delete Database', padding=10)
        lbl_hed_dtb.pack(side='left', padx=(0, 40))

        # Import/Export_______________________________
        lbl_hed_imp_exp = ttk.LabelFrame(
            frm_btm, text='Import/Export', padding=10)
        lbl_hed_imp_exp.pack(side='left', padx=(0, 20), fill='both')
        imp_btn = ttk.Button(
            lbl_hed_imp_exp, text='Import Settings', command=lambda: self.imp_set())
        exp_btn = ttk.Button(
            lbl_hed_imp_exp, text='Export Settings', command=lambda: self.exp_set())
        imp_btn.pack(pady=(0, 20), fill='both', expand=1)
        exp_btn.pack(fill='both', expand=1)

        lbl_hed_bse = ttk.LabelFrame(frm_btm, text='Advanced', padding=10)
        lbl_hed_bse.pack(side='left')
        # Database Settings_______________________________
        dtb_yr = ttk.Combobox(
            lbl_hed_dtb, values=Yr_fle().yr, state='readonly')
        dtb_yr.set('Database')
        dtb_yr.pack(side='top', pady=(0, 10))
        del_yr = ttk.Button(lbl_hed_dtb, text='Delete', command=lambda: self.dtb_del(
            dtb_yr.get(), dtb_yr, del_yr), state='disabled', takefocus=0)
        del_yr.pack(side='bottom')
        # Tokens Settings_______________________________
        lbfrm_tkn = ttk.LabelFrame(frm_top, text='Tokens', padding=10)
        lbfrm_tkn.pack(side='left')
        lbfrm_tkn_top = tk.Frame(lbfrm_tkn, bg=Win.SM_BG_HEX)
        lbfrm_tkn_top.pack(side='top', pady=(0, 10), fill='x')
        lbfrm_tkn_btm = tk.Frame(lbfrm_tkn, bg=Win.SM_BG_HEX)
        lbfrm_tkn_btm.pack(side='top')

        tkn_reg = self.register(self.tkn_check)
        ent_tkn = ttk.Entry(lbfrm_tkn_top, width=5,
                            validate='key', validatecommand=(tkn_reg, '%P'))
        ent_tkn.pack(side='left', padx=(0, 10))

        gen_tkn = ttk.Button(lbfrm_tkn_top, text='Generate Tokens',
                             command=lambda: self.tkn_gen(ent_tkn))
        gen_tkn.pack(side='left', fill='x', expand=1)

        vw_tkn = ttk.Button(lbfrm_tkn_btm, text='View Tokens',
                            command=lambda: Token_Show())
        vw_tkn.pack(side='left', padx=(0, 10))

        del_tkn = ttk.Button(
            lbfrm_tkn_btm, text='Delete Tokens', command=lambda: self.tkn_del())
        del_tkn.pack(side='left')
        # Base Settings_______________________________
        lbfrm_bse_passwd = ttk.LabelFrame(
            lbl_hed_bse, text='Password', padding=10)
        lbfrm_bse_passwd.pack(side='top')
        spc_reg = self.register(self.spc_check)
        bse_passwd = ttk.Entry(lbfrm_bse_passwd, validate='key',
                               validatecommand=(spc_reg, '%S'))
        bse_passwd.pack(side='left', padx=(0, 10))
        bse_passwd.insert(0, Access_Config().bse_config['passwd'])

        lbfrm_key_passwd = ttk.LabelFrame(
            lbl_hed_bse, text='SuperKey', padding=10)
        lbfrm_key_passwd.pack(side='top')
        key_passwd = ttk.Entry(lbfrm_key_passwd, validate='key',
                               validatecommand=(spc_reg, '%S'), show='*')
        key_passwd.pack(side='left', padx=(0, 10))
        key_passwd.insert(0, Access_Config().bse_config['key'])

        btn_bse_sub = ttk.Button(lbfrm_bse_passwd, text='Submit', style='m.TButton',
                                 command=lambda: self.chng_pswd(bse_passwd), takefocus=0)
        btn_bse_sub.pack(side='left')
        btn_key_sub = ttk.Button(
            lbfrm_key_passwd, text='Submit', style='m.TButton', command=lambda: self.chng_key(key_passwd), takefocus=0)
        btn_key_sub.pack(side='left')
        dtb_yr.bind('<<ComboboxSelected>>',
                    lambda event: del_yr.config(state='enabled'))
        # _______________________________

    @staticmethod
    def spc_check(inp: str) -> bool:
        """Restricts the use of whitespaces."""
        if inp != ' ':
            return True
        else:
            return False

    @staticmethod
    def tkn_check(inp: str) -> bool:
        """Restricts all but numbers and that too upto 5 digits only."""
        if (inp.isdigit() or inp is '') and len(inp) <= 5:
            return True
        else:
            return False

    def tkn_gen(self, ent: ttk.Entry):
        if Ent_Box(self, 'Enter SuperKey & Confirm to Continue.', Root.DATAFILE[0], 'key').get():
            Tokens(app, ent.get()).gen()

    def exp_set(self):
        fdir = path.dirname(__file__)
        dest = askdirectory(parent=self, initialdir=fdir)
        if dest != '':
            try:
                src = rf'{Write_Default.loc}/'
                fles = Write_Default.fles
                for i in fles:
                    fsrc = src+i
                    copyfile(fsrc, dest+f'/{i}')
                mg.showinfo(
                    'Voting Master', f'Settings Exported successfuly to-\n{dest}', parent=self)
            except:
                mg.showerror(
                    'Error', 'Can\'t export! File doesn\'t exist', parent=self)

    def imp_set(self):
        fdir = path.dirname(__file__)
        fnmes = askopenfilenames(
            parent=self, initialdir=fdir, filetypes=(('Settings Files', '*.md'),))
        if fnmes != '':
            try:
                dest = rf'{Write_Default.loc}/'
                fsrc = [i for i in fnmes if i.split(
                    '/')[-1] in Write_Default.fles]
                for i in fsrc:
                    copyfile(i, dest+(i.split('/')[-1]))
                repr_dir = ''.join(fsrc[0].split('/')[:-1])+'/'
                if fsrc != []:
                    mg.showinfo(
                        'Voting Master', f'Settings Imported successfuly from-\n{repr_dir}', parent=self)
            except:
                pass

    def dtb_del(self, *args: '(str, ttk.Combobox, ttk.Button)'):
        """Deletes the selected database."""
        sel_yr, bx_up, btn, = args
        fle = Yr_fle.fle
        yr = Yr_fle.yr
        if mg.askokcancel('Voting Master', 'You are about to delete a database!', parent=self):
            bx_up.set('Database')
            btn.config(state='disabled')
            ind = yr.index(sel_yr)
            fl_dl = fle[ind]
            remove(rf'{Write_Default.loc}\{fl_dl}')
            bx_up.config(values=Yr_fle().yr)

    def tkn_del(self):
        if mg.askokcancel('Voting Master', 'You are about to delete the Token file!', parent=self):
            remove(rf'{Tokens.LOC}\{Tokens.FL}')

    def chng_pswd(self, pswd: tk.Entry):
        """Changes the password in base config file."""
        cfg = Access_Config().bse_config
        if cfg['passwd'] != pswd.get().strip():
            try:
                cfg['passwd'] = pswd.get().strip()
                self.reg = Reg()
                self.reg.setx(ENV_KEY, Crypt().encrypt(str(cfg), SECRET_KEY))
                self.reg.close()
                pswd.delete(0, tk.END)
                pswd.insert(0, Access_Config().bse_config['passwd'])
                mg.showinfo('Voting Master',
                            'Password has been Changed!', parent=self)
            except:
                pass
        else:
            if pswd.get().strip() == '':
                pswd.delete(0, tk.END)
            mg.showerror(
                'Error', 'Same Password found,\nType in a different password.', parent=self)

    def chng_key(self, pswd: tk.Entry):
        """Changes the key in base config file."""
        cfg = Access_Config().bse_config
        if Ent_Box(app, 'Enter Previous SuperKey to Continue.', Root.DATAFILE[0], 'key').get():
            if cfg['key'] != pswd.get().strip():
                try:
                    cfg['key'] = pswd.get().strip()
                    self.reg = Reg()
                    self.reg.setx(ENV_KEY, Crypt().encrypt(
                        str(cfg), SECRET_KEY))
                    self.reg.close()
                    pswd.delete(0, tk.END)
                    pswd.insert(0, Access_Config().bse_config['key'])
                    mg.showinfo('Voting Master',
                                'Key has been Changed!', parent=self)
                except:
                    pass
            else:
                if pswd.get().strip() == '':
                    pswd.delete(0, tk.END)
                mg.showerror(
                    'Error', 'Same Key found,\nType in a different Key.', parent=self)


class Result_Show_Sep(tk.Tk):
    """Constructs a Result window to the show the fetched data and to save it."""

    def __init__(self, __yr: str, *__args: '(String of fields to be shown)', key=1):
        super().__init__()
        __args = str(__args).lstrip("('").rstrip("',)")
        x = self.winfo_screenwidth()/2 - 400
        y = self.winfo_screenheight()/2 - 300 - 40
        self.title('Result')
        self.geometry('800x600+%d+%d' % (x, y))
        self.iconbitmap(Root.DATAFILE[0])
        self.minsize(800, 600)

        menu_bar = tk.Menu(self)
        self.configure(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save as Text',
                              command=lambda: self.save())
        if key == 1:
            file_menu.add_command(label='Export to Excel',
                                  command=lambda: self._exp_exl(res, col))
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.destroy)

        if key == 1:
            __hedbar = tk.Frame(self)
            __hedbar.pack(side='top', fill='x')
            __lblres = tk.Label(__hedbar, text='Result', font=('Segoe UI', 24, 'bold'),
                                fg='#FFFFFF', bg='#0077CC', relief='solid', bd=1)
            __lblres.pack(fill='x', ipady=10)
        self.flval = 0
        self.r_navbar()
        h_scrlbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        h_scrlbar.pack(side='bottom', fill='x')

        self.res_tbl = ScrolledText(self, font=(
            'Consolas', 14), wrap=tk.NONE, xscrollcommand=h_scrlbar.set)
        self.res_tbl.pack(fill='both', expand=1)
        h_scrlbar.config(command=self.res_tbl.xview)
        if key == 1:
            if __yr != 'merged':
                res, col = Sql_init(0, yr=__yr).result(__args)
            else:
                res, col = Sql_init(0, dtb=1).result(__args)
            _pr = tabulate(res, col, tablefmt='fancy_grid',
                           missingval='-', numalign='center', stralign='center')
            _total = self._total(
                ['STAFF', 'STUDENT', 'CLASS', 'SEC'], res, col)
            if self._ttl != []:
                _pr += '\n'+tabulate([['TOTAL']], tablefmt='fancy_grid')
            _pr += '\n'+tabulate(_total, headers='firstrow',
                                 tablefmt='fancy_grid', numalign='center', stralign='center')
            self.res_tbl.insert(0.0, _pr)
            self.res_tbl.config(state='disabled')

    def _total(self, expt: list, *args: '(list, list)'):
        """To get total of result."""
        res, col = args
        ind = [i for i in range(len(list(col))) if col[i] not in expt]
        self._ttl = []
        for i in ind:
            _ = 0
            for j in range(len([list(i) for i in res])):
                try:
                    _ += [list(i) for i in res][j][i]
                except:
                    continue
            self._ttl.append(_)
        col = [col[i] for i in range(len(col)) if i in ind]
        return col, self._ttl if self._ttl != [] else ''

    def save(self):
        """Saves the fetched data through a dialog box."""
        fdir = path.dirname(__file__)
        fname = asksaveasfilename(
            parent=self, initialdir=fdir, filetypes=(('Text Documents', '*.txt'),))
        if fname != '':
            dir_fle = f'{fname}'
            if not dir_fle.endswith('.txt'):
                dir_fle += '.txt'
            with open(f'{dir_fle}', 'w', encoding='utf-8') as f:
                f.write(self.res_tbl.get(1.0, tk.END))
            mg.showinfo('Voting Master', 'File has been Saved.', parent=self)

    def _exp_exl(self, *args: '(list, list)'):
        """Exports the fetched data in a XLSX format."""
        val, col, = args
        fdir = path.dirname(__file__)
        fname = asksaveasfilename(
            parent=self, initialdir=fdir, filetypes=(('XLSX File', '*.xlsx'),))
        if fname != '':
            dir_fle = f'{fname}'
            if not dir_fle.endswith('.xlsx'):
                dir_fle += '.xlsx'
            wrkbk = xlsxwriter.Workbook(f'{dir_fle}')
            wrksht = wrkbk.add_worksheet()
            wrksht.set_column(0, len(col), max([len(i) for i in col])+1)
            head_format = wrkbk.add_format({
                'bold': True,
                'align': 'centre',
                'pattern': 1,
                'bg_color': '#0077CC',
                'font_color': '#FFFFFF',
                'text_wrap': False,
                'border': 1
            })
            val_format = wrkbk.add_format({
                'bold': False,
                'align': 'centre',
                'text_wrap': False,
                'border': 1
            })
            row = 0
            # Writing coloumns
            for i in range(len(col)):
                wrksht.write(row, i, col[i], head_format)
            row += 1
            # Writing Values
            for i in range(len(val)):
                for j in range(len(val[i])):
                    if val[i][j] is None:
                        wrksht.write(row, j, '-', val_format)
                    else:
                        wrksht.write(row, j, val[i][j], val_format)
                row += 1
            row += 1+1
            # Writing Total
            ind = [i for i in range(len(col)) if col[i]
                   not in ['CLASS', 'SEC']]
            ttl = self._total(['CLASS', 'SEC'], val, col)
            _ = 0
            wrksht.write(row-1, 0, 'Total:', head_format)
            for i in range(len(col)):
                if i in ind:
                    wrksht.write(row, i, ttl[1][_], val_format)
                    _ += 1
                else:
                    wrksht.write(row, i, '-', val_format)
            wrkbk.close()
            mg.showinfo('Voting Master', 'File has been Saved.', parent=self)

    def flscrn(self):
        """Toggles b/w Fullscreen mode."""
        if self.flval == 0:
            self.flval = 1
            self.attributes('-fullscreen', True)
        else:
            self.flval = 0
            self.attributes('-fullscreen', False)

    def r_navbar(self):
        """Bottom sided navbar for Result Window"""
        navbar = tk.Frame(self)
        navbar.pack(side='bottom', expand=0, fill='x')

        navx = tk.Button(navbar, text='X', highlightthickness=0, bg='#FF3232', activebackground='#FF4C4C', takefocus=0,
                         relief='groove', bd=1, fg='#EFEFEF', height=2, command=self.destroy, font=('Segoe UI', 10, 'bold'))
        navx.pack(side='left', fill='x', expand=1, anchor='s')

        navhlp = tk.Button(navbar, text='≡', highlightthickness=0, bg='#303030', activebackground='#6D6D6D', takefocus=0,
                           relief='groove', bd=1, fg='#EFEFEF', height=2, command=lambda: self.flscrn(), font=('Segoe UI', 10, 'bold'))
        navhlp.pack(side='left', fill='x', expand=1, anchor='s')


class Token_Show(Result_Show_Sep):
    def __init__(self):
        super().__init__(None, None, key=0)
        self.title('Tokens')
        try:
            with open(rf'{Tokens.LOC}\{Tokens.FL}', 'r') as f:
                tkns = ''
                try:
                    tkn_lst = eval(Crypt().decrypt(str(f.read()), SECRET_KEY))
                    line = len(tkn_lst)//7
                    if (len(tkn_lst)/7)-line > 0:
                        line += 1
                    n = 0
                    for _ in range(line):
                        n += 7
                        tkn_tab = tabulate([tkn_lst[n-7:n]],
                                           tablefmt='fancy_grid', numalign='center', stralign='center')
                        tkns += tkn_tab+'\n'
                except:
                    pass
            self.res_tbl.insert(0.0, tkns)
            self.res_tbl.config(state='disabled')
        except FileNotFoundError:
            self.withdraw()
            mg.showerror('Error', 'Token file doesn\'t exists.', parent=self)
            self.destroy()


if __name__ == '__main__':
    mutex = win32event.CreateMutex(None, False, 'name')
    last_error = win32api.GetLastError()
    if last_error == ERROR_ALREADY_EXISTS:
        Root.ins_dat(['res\\v_r.ico'])
        msg = tk.Tk()
        msg.attributes('-topmost', 1)
        msg.withdraw()
        msg.title('Error')
        msg.iconbitmap(Root.DATAFILE[0])
        mg.showwarning('Error', 'App instance already running.', parent=msg)
        msg.destroy()
        sys.exit()
    root = Root()
    root.lower()
    root.iconify()

    app = Win(root)
    app.mainloop()

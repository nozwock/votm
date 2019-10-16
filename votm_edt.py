# -*- coding: utf-8 -*-

import sys
from os import path, remove
from datetime import date
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinter import messagebox as mg
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename, askopenfilenames
from votmapi.logic import Default_Config, Write_Default, Access_Config, Sql_init, Yr_fle, Ent_Box, Tokens, __author__, __version__
from tabulate import tabulate
import xlsxwriter


class Root(ThemedTk):
    """Root Dummy Window."""
    DATAFILE = []

    def __init__(self):
        super().__init__(theme='arc')
        self.title('Voting Master-Edit')
        self.attributes('-alpha', 0.0)
        self.ins_dat(['res\\v_r.ico', 'res\\ttle.png', 'res\\edtw.png', 'res\\rslw.png',
                      'res\\sttw.png', 'res\\edtb.png', 'res\\rslb.png', 'res\\sttb.png'])
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
    SM_BG_HEX = '#F5F6F7'

    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(1)

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
                     lambda event: (self.withdraw()))
        self.master.bind('<Map>', lambda event: (
            self.master.deiconify(), self.deiconify()))

        self.navbar()
        self.frame_n = None
        self.replace_frame(Edit)

        if Ent_Box(self, icn=Root.DATAFILE[0]).get():
            pass
        else:
            self.master.destroy()
            exit()

        Write_Default()
        if Write_Default.exist is 1:
            mg.showinfo('One-Time Process',
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

    def about(self) -> str:
        """Dialog box of about."""
        mg.showinfo(
            'About', f'Version: {__version__}\nAuthor: {__author__}, 12\'A, 2019-20\nArmy Public School\nMathura Cantt\nPrinciple - Mrs. Gayatri Kulshreshtha\nTeacher - Mr. Amit Bansal, PGT - Comp.Sc', parent=self)

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
                          relief='flat', bd=1, fg='#EFEFEF', height=2, command=self.master.destroy, font=('Segoe UI', 10, 'bold'))
        btxlb.pack(side='left', fill='x', expand=1, anchor='s')

        bthlb = tk.Button(flb, text='?', highlightthickness=0, bg='#303030', activebackground='#6D6D6D', takefocus=0,
                          relief='flat', bd=1, fg='#EFEFEF', height=2, command=self.about, font=('Segoe UI', 10, 'bold'))
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

        tab = ttk.Notebook(self)
        cand = tk.Frame(tab, bg=Win.SM_BG_HEX)
        tab.add(cand, text='Candidancy')
        clss = tk.Frame(tab, bg=Win.SM_BG_HEX)
        tab.add(clss, text='Class & Sec')
        tab.pack(side='right', expand=True, fill='both')
        # Cand Frame__________________________
        post = list(Access_Config().cand_config.keys())
        cand_vw_ed = ttk.LabelFrame(cand, text='View/Edit', padding=10)
        cand_vw_ed.pack(pady=(48, 10))
        cand_vw_ed_top = tk.Frame(cand_vw_ed, bg=Win.SM_BG_HEX)
        cand_vw_ed_top.pack(side='top', pady=(0, 10))
        cand_vw_ed_btm = tk.Frame(cand_vw_ed, bg=Win.SM_BG_HEX)
        cand_vw_ed_btm.pack(side='bottom')
        cand_vw_ed_pst = ttk.Combobox(
            cand_vw_ed_top, values=post, state='readonly', style='TCombobox')
        cand_vw_ed_pst.set('Post')
        cand_vw_ed_pst.pack(side='left', padx=(0, 10))
        cand_vw_ed_cand = ttk.Combobox(cand_vw_ed_top, state='readonly')
        cand_vw_ed_cand.set('Candidate')
        cand_vw_ed_cand.pack(side='left')
        str_reg = self.register(self.str_check)
        cand_vw_ed_ent = ttk.Entry(cand_vw_ed_btm, validate='key',
                                   validatecommand=(str_reg, '%S'))
        cand_vw_ed_ent.pack(side='left', padx=(0, 45))
        cand_vw_ed_ent.insert(1, 'Candidate')
        cand_vw_ed_btn = ttk.Button(cand_vw_ed_btm, text='Edit', style='m.TButton', command=lambda: self.wrt_edt(
            cand_vw_ed_pst, cand_vw_ed_cand, cand_vw_ed_ent), takefocus=0)
        cand_vw_ed_btn.pack(side='left', padx=(0, 25))

        cand_add = ttk.LabelFrame(cand, text='Add', padding=10)
        cand_add.pack(pady=(0, 10))
        cand_add_pst = ttk.Combobox(cand_add, values=post, state='readonly')
        cand_add_pst.set('Post')
        cand_add_pst.pack(side='left', padx=(0, 10))
        cand_add_ent = ttk.Entry(cand_add, validate='key',
                                 validatecommand=(str_reg, '%S'))
        cand_add_ent.pack(side='left', padx=(0, 10))
        cand_add_ent.insert(1, 'Candidate')
        cand_add_btn = ttk.Button(cand_add, text='Add', style='m.TButton', command=lambda: (
            self.wrt_add(cand_add_pst, cand_add_ent), cand_add_ent.delete(0, tk.END)), takefocus=0)
        cand_add_btn.pack(side='left')

        cand_del = ttk.LabelFrame(cand, text='Delete', padding=10)
        cand_del.pack(pady=(0, 20))
        cand_del_pst = ttk.Combobox(cand_del, values=post, state='readonly')
        cand_del_pst.set('Post')
        cand_del_pst.pack(side='left', padx=(0, 10))
        cand_del_cand = ttk.Combobox(cand_del, state='readonly')
        cand_del_cand.set('Candidate')
        cand_del_cand.pack(side='left', padx=(0, 10))
        cand_del_btn = ttk.Button(cand_del, text='Delete', style='m.TButton',
                                  command=lambda: self.cand_del(cand_del_pst, cand_del_cand), takefocus=0)
        cand_del_btn.pack(side='left')

        cand_clr = ttk.Button(cand, text='Clear', padding=10, style='m.TButton', command=lambda: (
            self.wrt(1, Default_Config.candidate_config), mg.showinfo('Candidancy', 'Cleared!', parent=self)), takefocus=0)
        cand_clr.pack()
        cand_vw_ed_pst.bind('<<ComboboxSelected>>', lambda event: (cand_vw_ed_cand.config(values=Access_Config().cand_config[cand_vw_ed_pst.get(
        )]), cand_vw_ed_cand.set(''), self.cur(cand_vw_ed_cand), cand_vw_ed_ent.delete(0, tk.END), cand_vw_ed_ent.insert(0, cand_vw_ed_cand.get())))
        cand_vw_ed_cand.bind('<<ComboboxSelected>>', lambda event: (
            cand_vw_ed_ent.delete(0, tk.END), cand_vw_ed_ent.insert(0, cand_vw_ed_cand.get())))
        cand_add_pst.bind('<<ComboboxSelected>>',
                          lambda event: cand_add_ent.delete(0, tk.END))
        cand_del_pst.bind('<<ComboboxSelected>>', lambda event: (cand_del_cand.config(
            values=Access_Config().cand_config[cand_del_pst.get()]), cand_del_cand.set(''), self.cur(cand_del_cand)))
        # Clss&Sec Frame__________________________
        clss_lst = list(Access_Config().clss_config.keys())

        clss_vw = ttk.LabelFrame(clss, text='View', padding=10)
        clss_vw.pack(pady=(30, 10))
        clss_vw_clss = ttk.Combobox(clss_vw, values=clss_lst, state='readonly')
        clss_vw_clss.set('Class')
        clss_vw_clss.pack(pady=(0, 10))
        clss_vw_sec = ScrolledText(clss_vw, wrap=tk.WORD, font=(
            'Segue UI', 8), width=30, height=5, relief='flat', fg='#5C616C')
        clss_vw_sec.insert(0.0, 'Sections Here')
        clss_vw_sec.pack()
        clss_vw_sec.config(state='disabled')

        clss_add = ttk.LabelFrame(clss, text='Add', padding=10)
        clss_add.pack(pady=(0, 10))
        clss_add_clss = ttk.Combobox(
            clss_add, values=clss_lst, state='readonly')
        clss_add_clss.set('Class')
        clss_add_clss.pack(side='left', padx=(0, 10))
        one_reg = self.register(self.one_check)
        self.clss_add_sec = ttk.Entry(clss_add, validate='key',
                                      validatecommand=(one_reg, '%P'))
        self.clss_add_sec.pack(side='left', padx=(0, 10))
        clss_add_btn = ttk.Button(clss_add, text='Add', style='m.TButton', command=lambda: (
            self.clss_add(clss_add_clss, self.clss_add_sec), self.clss_add_sec.delete(0, tk.END)), takefocus=0)
        clss_add_btn.pack(side='left')

        clss_del = ttk.LabelFrame(clss, text='Delete', padding=10)
        clss_del.pack(pady=(0, 10))
        clss_del_clss = ttk.Combobox(
            clss_del, values=clss_lst, state='readonly')
        clss_del_clss.set('Class')
        clss_del_clss.pack(side='left', padx=(0, 10))
        clss_del_sec = ttk.Combobox(clss_del, state='readonly')
        clss_del_sec.set('Section')
        clss_del_sec.pack(side='left', padx=(0, 10))
        clss_del_btn = ttk.Button(clss_del, text='Delete', style='m.TButton',
                                  command=lambda: self.clss_del(clss_del_clss, clss_del_sec), takefocus=0)
        clss_del_btn.pack(side='left')

        clss_def = ttk.Button(clss, text='Default', padding=10, style='m.TButton', command=lambda: (
            self.wrt(2, Default_Config.clss_config), mg.showinfo('Class&Sec', 'Set to Default.', parent=self)), takefocus=0)
        clss_def.pack()
        clss_vw_clss.bind('<<ComboboxSelected>>', lambda event: (clss_vw_sec.config(state='normal'), clss_vw_sec.delete(
            0.0, tk.END), clss_vw_sec.insert(0.0, Access_Config().clss_config[int(clss_vw_clss.get())]), clss_vw_sec.config(state='disabled')))
        clss_add_clss.bind('<<ComboboxSelected>>',
                           lambda event: self.clss_add_sec.delete(0, tk.END))
        clss_del_clss.bind('<<ComboboxSelected>>', lambda event: (clss_del_sec.config(values=Access_Config(
        ).clss_config[int(clss_del_clss.get())]), clss_del_sec.set(''), self.cur(clss_del_sec)))

    @staticmethod
    def str_check(inp: str) -> bool:
        """Checks if the input is an alphabet or not."""
        if inp.isalpha():
            return True
        else:
            return False

    def one_check(self, inp: str) -> bool:
        """Check to allow only 1 alphabet."""
        if (len(inp+self.clss_add_sec.get()) <= 1 and (inp.isalpha()) or inp is ''):
            return True
        else:
            return False

    @staticmethod
    def cur(cand: ttk.Combobox):
        """Selects 1st value in a combobox."""
        try:
            cand.current(0)
        except:
            pass

    @staticmethod
    def wrt(fle: int, cfg: str):
        """Writes Default config. files."""
        with open(rf'{Write_Default.loc}\{Write_Default.fles[fle]}', 'w') as f:
            f.write(str(cfg))
            f.flush()

    def wrt_edt(self, key: ttk.Combobox, pos: ttk.Combobox, val: tk.Entry):
        """Writes changes to the Candidate file."""
        cfg = Access_Config().cand_config
        if val.get().strip() != '':
            try:
                cfg[key.get()][cfg[key.get()].index(
                    pos.get())] = val.get().strip()
                self.wrt(1, cfg)
                pos.set(val.get())
                pos.config(values=Access_Config().cand_config[key.get()])
            except:
                mg.showerror('Error', 'No Canidate was selected.', parent=self)
        else:
            mg.showerror('Error', 'Enter a value first.', parent=self)

    def wrt_add(self, key: ttk.Combobox, val: tk.Entry):
        """Adds value to the candidate file."""
        cfg = Access_Config().cand_config
        if val.get().strip() != '':
            try:
                cfg[key.get()].append(val.get().strip())
                self.wrt(1, cfg)
            except:
                mg.showerror('Error', 'Select a Post first.', parent=self)
        else:
            mg.showerror('Error', 'Enter a value first.', parent=self)

    def cand_del(self, key: ttk.Combobox, val: ttk.Combobox):
        """Deletes value from candidate file."""
        cfg = Access_Config().cand_config
        try:
            cfg[key.get()].remove(val.get())
            self.wrt(1, cfg)
            val.set('')
            val.config(values=Access_Config().cand_config[key.get()])
            val.current(0)
        except (ValueError, KeyError):
            val.set('')
            mg.showerror('Error', 'Candidate doesn\'t exist.', parent=self)
        except tk.TclError:
            pass

    def clss_del(self, key: ttk.Combobox, val: ttk.Combobox):
        """Deletes value from class file."""
        cfg = Access_Config().clss_config
        try:
            cfg[int(key.get())].remove(val.get())
            self.wrt(2, cfg)
            val.set('')
            val.config(values=Access_Config().clss_config[int(key.get())])
            val.current(0)
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
                    self.wrt(2, cfg)
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
        mrg_lblfrm = ttk.Labelframe(self, text='Merge', padding=10)
        shw_lblfrm = ttk.Labelframe(self, text='Show', padding=10)
        mrg_lblfrm.pack(pady=(20, 10))
        shw_lblfrm.pack()

        mrg_left = tk.Frame(mrg_lblfrm, bg=Win.SM_BG_HEX)
        mrg_left.pack(side='left', padx=(0, 10))
        mrg_right = tk.Frame(mrg_lblfrm, bg=Win.SM_BG_HEX)
        mrg_right.pack(side='right')
        self.mrg_drctr = tk.Listbox(
            mrg_left, height=5, relief='groove', bd=2, highlightthickness=0)
        self.mrg_drctr.pack(side='top')
        mrg_clr = tk.Button(mrg_left, text='Remove', relief='groove', highlightthickness=0, bg=Win.SM_BG_HEX,
                            activebackground=Win.SM_BG_HEX, activeforeground='#5C616C', fg='#5C616C',
                            command=lambda: self.rmv_item(), takefocus=0)
        mrg_clr.pack(side='top', fill='x')
        mrg_brws = ttk.Button(mrg_right, text='Browse',
                              command=lambda: self.opn_mrg_fles(), takefocus=0)
        mrg_brws.pack(side='top', pady=(10, 10))
        mrg_shw = ttk.Button(mrg_right, text='Merge',
                             command=lambda: self.do_mrg(), takefocus=0)
        mrg_shw.pack(side='top', pady=(0, 10))
        mrg_conv_exl = ttk.Button(
            mrg_right, text='Export Merge File', command=lambda: self.crt_mrg_fle(), takefocus=0)
        mrg_conv_exl.pack(side='top', pady=(0, 10))
        # Show Frame______________________
        self.shw_db = ttk.Combobox(
            shw_lblfrm, state='readonly', values=Yr_fle().yr)
        self.shw_db.set('Database')
        shw_lblfrm_top = tk.Frame(shw_lblfrm)
        shw_lblfrm_sup = tk.Frame(shw_lblfrm)
        shw_lblfrm_btw = tk.Frame(shw_lblfrm)
        shw_lblfrm_btm = tk.Frame(shw_lblfrm)
        self.shw_shw = ttk.Button(
            shw_lblfrm, text='Show', state='disabled', command=lambda: self.shw_res(), takefocus=0)
        self.shw_db.pack(side='top', pady=(0, 10))
        shw_lblfrm_top.pack(side='top', pady=(0, 10))
        shw_lblfrm_sup.pack(side='top', pady=(0, 10))
        shw_lblfrm_btw.pack(side='top', pady=(0, 10))
        shw_lblfrm_btm.pack(side='top', pady=(0, 10))
        self.shw_shw.pack(side='bottom')

        self.shw_opt_var = tk.IntVar()
        self.shw_chk_var_tchr = tk.IntVar()
        self.shw_chk_var_std = tk.IntVar()
        self.shw_chk_var_clss = tk.IntVar()
        self.shw_chk_var_sec = tk.IntVar()
        self.shw_chk_var_HB = tk.IntVar()
        self.shw_chk_var_VHB = tk.IntVar()
        self.shw_chk_var_HG = tk.IntVar()
        self.shw_chk_var_VHG = tk.IntVar()
        shw_opt_cstm = ttk.Radiobutton(
            shw_lblfrm_top, text='Custom', variable=self.shw_opt_var, value=0, command=lambda: self.opt_call(shw_chk_clss))
        shw_opt_all = ttk.Radiobutton(shw_lblfrm_top, text='Select All',
                                      variable=self.shw_opt_var, value=1, command=lambda: self.opt_call(shw_chk_clss))
        shw_chk_tchr = ttk.Checkbutton(shw_lblfrm_sup, text='Staff', takefocus=0, variable=self.shw_chk_var_tchr, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_std = ttk.Checkbutton(shw_lblfrm_sup, text='Student', takefocus=0, variable=self.shw_chk_var_std, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_clss = ttk.Checkbutton(shw_lblfrm_btw, text='Class', takefocus=0, variable=self.shw_chk_var_clss, command=lambda: (
            self.chk_clss_sec(self.shw_chk_var_clss, shw_chk_clss, self.shw_chk_var_sec), self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_sec = ttk.Checkbutton(shw_lblfrm_btw, text='Section', takefocus=0, variable=self.shw_chk_var_sec, command=lambda: (
            self.chk_clss_sec(self.shw_chk_var_clss, shw_chk_clss, self.shw_chk_var_sec), self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_HB = ttk.Checkbutton(shw_lblfrm_btw, text='Headboy', takefocus=0, variable=self.shw_chk_var_HB, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_VHB = ttk.Checkbutton(shw_lblfrm_btm, text='ViceHeadboy', takefocus=0, variable=self.shw_chk_var_VHB, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_HG = ttk.Checkbutton(shw_lblfrm_btm, text='Headgirl', takefocus=0, variable=self.shw_chk_var_HG, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_chk_VHG = ttk.Checkbutton(shw_lblfrm_btm, text='ViceHeadgirl', takefocus=0, variable=self.shw_chk_var_VHG, command=lambda: (
            self.chk_btn(), self.shw_opt_var.set(0)))
        shw_opt_cstm.pack(side='left')
        shw_opt_all.pack(side='left')
        shw_chk_tchr.pack(side='left')
        shw_chk_std.pack(side='left')
        shw_chk_clss.pack(side='left')
        shw_chk_sec.pack(side='left')
        shw_chk_HB.pack(side='left')
        shw_chk_VHB.pack(side='left')
        shw_chk_HG.pack(side='left')
        shw_chk_VHG.pack(side='left')
        self.shw_db.bind("<<ComboboxSelected>>", lambda event: self.chk_btn())

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
                    mg.showinfo(
                        'Info', 'Merge file has been generated.', parent=self)
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
                        mrg_tbl_data.append(eval(f.read()))
                Sql_init(0, dtb=1).mrg_dtb_res(mrg_tbl_n, mrg_tbl_data)
        else:
            mg.showwarning('Alert', 'No Merge file is selected!', parent=self)

    def shw_res(self):
        """Creates a string from a list of columns to be shown and it is passed to the Result window."""
        try:
            if self.shw_db.get() != 'merged':
                pst_cand, _ = Sql_init(0).cols(self.shw_db.get())
            else:
                pst_cand, _ = Sql_init(0, dtb=1).cols(self.shw_db.get())
            hb = (str([i for i in pst_cand if i.startswith('HB')]
                      ).lstrip('[').rstrip(']')).replace("'", "")
            vhb = (str([i for i in pst_cand if i.startswith('VHB')]
                       ).lstrip('[').rstrip(']')).replace("'", "")
            hg = (str([i for i in pst_cand if i.startswith('HG')]
                      ).lstrip('[').rstrip(']')).replace("'", "")
            vhg = (str([i for i in pst_cand if i.startswith('VHG')]
                       ).lstrip('[').rstrip(']')).replace("'", "")
            vals = ['STAFF', 'STUDENT', 'CLASS', 'SEC', hb, vhb, hg, vhg]
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
        self.var_val_lst = [self.shw_chk_var_tchr.get(), self.shw_chk_var_std.get(), self.shw_chk_var_clss.get(), self.shw_chk_var_sec.get(),
                            self.shw_chk_var_HB.get(), self.shw_chk_var_VHB.get(), self.shw_chk_var_HG.get(), self.shw_chk_var_VHG.get()]
        if self.shw_db.get() in Yr_fle.yr:
            if any(self.var_val_lst) == 0:
                self.shw_shw.config(state='disabled')
            else:
                self.shw_shw.config(state='enabled')

    def opt_call(self, clss: ttk.Combobox):
        """Tickmarks all for select all and change to custom for any changes."""
        var_lst = [self.shw_chk_var_tchr, self.shw_chk_var_std, self.shw_chk_var_clss, self.shw_chk_var_sec, self.shw_chk_var_HB,
                   self.shw_chk_var_VHB, self.shw_chk_var_HG, self.shw_chk_var_VHG]
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
        lbl_hed_bse = ttk.LabelFrame(frm_btm, text='Advanced', padding=10)
        lbl_hed_bse.pack()
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
        lbfrm_tkn_top = tk.Frame(lbfrm_tkn)
        lbfrm_tkn_top.pack(side='top', pady=(0, 10), fill='x')
        lbfrm_tkn_btm = tk.Frame(lbfrm_tkn)
        lbfrm_tkn_btm.pack(side='top')

        tkn_reg = self.register(self.tkn_check)
        ent_tkn = ttk.Entry(lbfrm_tkn_top, width=5,
                            validate='key', validatecommand=(tkn_reg, '%P'))
        ent_tkn.pack(side='left', padx=(0, 10))

        gen_tkn = ttk.Button(lbfrm_tkn_top, text='Generate Tokens',
                             command=lambda: self.tkn_gen(ent_tkn))
        gen_tkn.pack(side='left', fill='x', expand=1)

        vw_tkn = ttk.Button(lbfrm_tkn_btm, text='View Tokens', command=lambda: Token_Show())
        vw_tkn.pack(side='left', padx=(0, 10))

        del_tkn = ttk.Button(lbfrm_tkn_btm, text='Delete Tokens', command=lambda: self.tkn_del())
        del_tkn.pack(side='left')
        # Base Settings_______________________________
        lbfrm_bse_passwd = ttk.LabelFrame(
            lbl_hed_bse, text='Password', padding=10)
        lbfrm_bse_passwd.pack(side='top', pady=(0, 10))
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

    def dtb_del(self, *args: '(str, ttk.Combobox, ttk.Button)'):
        """Deletes the selected database."""
        sel_yr, bx_up, btn, = args
        fle = Yr_fle.fle
        yr = Yr_fle.yr
        if mg.askokcancel('Attention', 'You are about to delete a database!', parent=self):
            bx_up.set('Database')
            btn.config(state='disabled')
            ind = yr.index(sel_yr)
            fl_dl = fle[ind]
            remove(rf'{Write_Default.loc}\{fl_dl}')
            bx_up.config(values=Yr_fle().yr)
    
    def tkn_del(self):
        if mg.askokcancel('Attention', 'You are about to delete the Token file!', parent=self):
            remove(rf'{Tokens.LOC}\{Tokens.FL}')

    def chng_pswd(self, pswd: tk.Entry):
        """Changes the password in base config file."""
        cfg = Access_Config().bse_config
        if cfg['passwd'] != pswd.get().strip():
            try:
                cfg['passwd'] = pswd.get().strip()
                with open(f'{Write_Default.loc}\\{Write_Default.fles[0]}', 'w') as f:
                    f.write(str(cfg))
                pswd.delete(0, tk.END)
                pswd.insert(0, Access_Config().bse_config['passwd'])
                mg.showinfo('Settings', 'Password Changed!', parent=self)
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
                    with open(f'{Write_Default.loc}\\{Write_Default.fles[0]}', 'w') as f:
                        f.write(str(cfg))
                    pswd.delete(0, tk.END)
                    pswd.insert(0, Access_Config().bse_config['key'])
                    mg.showinfo('Settings', 'Key Changed!', parent=self)
                except:
                    raise
            else:
                if pswd.get().strip() == '':
                    pswd.delete(0, tk.END)
                mg.showerror(
                    'Error', 'Same Key found,\nType in a different Key.', parent=self)


class Result_Show_Sep(tk.Tk):
    """Constructs a Result window to the show the fetched data and to save it."""

    def __init__(self, yr: str, *args: '(String of fields to be shown)'):
        super().__init__()
        args = str(args).lstrip("('").rstrip("',)")
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
        file_menu.add_command(label='Export to Excel',
                              command=lambda: self.exp_exl(res, col))
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.destroy)

        hedbar = tk.Frame(self)
        hedbar.pack(side='top', fill='x')
        lblres = tk.Label(hedbar, text='Result', font=('Segoe UI', 24, 'bold'),
                          fg='#FFFFFF', bg='#0077CC', relief='solid', bd=1)
        lblres.pack(fill='x', ipady=10)
        self.flval = 0
        self.r_navbar()
        h_scrlbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        h_scrlbar.pack(side='bottom', fill='x')

        self.res_tbl = ScrolledText(self, font=(
            'Consolas', 14), wrap=tk.NONE, xscrollcommand=h_scrlbar.set)
        self.res_tbl.pack(fill='both', expand=1)
        h_scrlbar.config(command=self.res_tbl.xview)

        if yr != 'merged':
            res, col = Sql_init(0, yr=yr).result(args)
        else:
            res, col = Sql_init(0, dtb=1).result(args)
        pr = tabulate(res, col, tablefmt='fancy_grid',
                      missingval='-', numalign='center', stralign='center')
        total = self.total(['STAFF', 'STUDENT', 'CLASS', 'SEC'], res, col)
        if self.ttl != []:
            pr += '\n'+tabulate([['TOTAL']], tablefmt='fancy_grid')
        pr += '\n'+tabulate(total, headers='firstrow',
                            tablefmt='fancy_grid', numalign='center', stralign='center')
        self.res_tbl.insert(0.0, pr)
        self.res_tbl.config(state='disabled')

    def total(self, expt: list, *args: '(list, list)'):
        """To get total of result."""
        res, col = args
        ind = [i for i in range(len(list(col))) if col[i] not in expt]
        self.ttl = []
        for i in ind:
            _ = 0
            for j in range(len([list(i) for i in res])):
                try:
                    _ += [list(i) for i in res][j][i]
                except:
                    continue
            self.ttl.append(_)
        col = [col[i] for i in range(len(col)) if i in ind]
        return col, self.ttl if self.ttl != [] else ''

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
            mg.showinfo('Info', 'File Saved.', parent=self)

    def exp_exl(self, *args: '(list, list)'):
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
            wrksht.set_column(0, len(col), max([len(i) for i in col]))
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
            ttl = self.total(['CLASS', 'SEC'], val, col)
            _ = 0
            wrksht.write(row-1, 0, 'Total:', head_format)
            for i in range(len(col)):
                if i in ind:
                    wrksht.write(row, i, ttl[1][_], val_format)
                    _ += 1
                else:
                    wrksht.write(row, i, '-', val_format)
            wrkbk.close()
            mg.showinfo('Info', 'File Saved.', parent=self)

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

class Token_Show(tk.Tk):
    def __init__(self):
        super().__init__()
        x = self.winfo_screenwidth()/2 - 400
        y = self.winfo_screenheight()/2 - 300 - 40
        self.title('Tokens')
        self.geometry('800x600+%d+%d' % (x, y))
        self.iconbitmap(Root.DATAFILE[0])
        self.minsize(800, 600)

        menu_bar = tk.Menu(self)
        self.configure(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save as Text',
                              command=lambda: self.save())
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.destroy)
        self.flval = 0
        self.r_navbar()

        h_scrlbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        h_scrlbar.pack(side='bottom', fill='x')
        self.res_tbl = ScrolledText(self, font=(
            'Consolas', 14), wrap=tk.NONE, xscrollcommand=h_scrlbar.set)
        self.res_tbl.pack(fill='both', expand=1)
        h_scrlbar.config(command=self.res_tbl.xview)

        with open(rf'{Tokens.LOC}\{Tokens.FL}', 'r') as f:
            tkns = ''
            try:
                tkn_lst = eval(f.read())
                line = len(tkn_lst)//7
                if (len(tkn_lst)/7)-line > 0:
                    line += 1
                for _ in range(line):
                    tkn_tab = tabulate([tkn_lst[:7]],
                            tablefmt='fancy_grid', numalign='center', stralign='center')
                    tkns += tkn_tab+'\n'
            except:
                pass

        self.res_tbl.insert(0.0, tkns)
        self.res_tbl.config(state='disabled')

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
            mg.showinfo('Info', 'File Saved.', parent=self)

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


if __name__ == '__main__':
    root = Root()
    root.lower()
    root.iconify()

    app = Win(root)
    app.mainloop()

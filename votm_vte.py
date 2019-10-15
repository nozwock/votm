# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import date
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from tkinter import messagebox as mg
from votmapi.logic import Write_Default, Access_Config, Sql_init, Ent_Box, Tokens, __author__, __version__


class Root(ThemedTk):
    """Root Dummy Window."""
    DATAFILE = []

    def __init__(self):
        super().__init__(theme='arc')
        self.title('Voting Master-Vote')
        self.attributes('-alpha', 0.0)
        self.protocol('WM_DELETE_WINDOW', Win.s_cls)
        self.ins_dat(['res\\v_r.ico', 'res\\bg.png'])
        self.iconbitmap(default=Root.DATAFILE[0])

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
        Write_Default()

        self.config(background=Win.SM_BG_HEX, relief='groove',
                    highlightbackground='#000000', highlightcolor='#000000', highlightthickness=1)
        ttk.Style().configure('TButton', focuscolor=self.cget('background'))

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

        x = self.winfo_screenwidth()/2 - 400
        y = self.winfo_screenheight()/2 - 240
        self.geometry('800x480+%d+%d' % (x, y))
        self.resizable(0, 0)
        self.iconbitmap(default=Root.DATAFILE[0])
        self.navbar()
        self.frame_n = None
        self.replace_frame(Home)
        self.protocol('WM_DELETE_WINDOW', self.s_cls)
        self.lift()

        if Write_Default.exist is 1:
            mg.showinfo('One-Time Process',
                        'Some default configuration files has been saved.', parent=self)

        if any([(Access_Config().cand_config[i]) == [] for i in list(Access_Config().cand_config.keys())]):
            mg.showerror(
                'Error', 'No Candidate found!, Add Candidate in Main App.', parent=self)
            self.master.destroy()
            exit()
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
                text='⚫ Home', background='#EFEFEF', foreground='#0077CC')
            self.vote.config(
                text='⚪ Vote  ', background='#0077CC', foreground='#EFEFEF')
            self.clss.config(
                text='⚪ Class*', background='#0077CC', foreground='#EFEFEF')
            self.done.config(
                text='⚪ Done ', background='#0077CC', foreground='#EFEFEF')
        elif cont == Class:
            self.clss.config(
                text='⚫ Class*', background='#EFEFEF', foreground='#0077CC')
            self.home.config(
                text='⚪ Home', background='#0077CC', foreground='#EFEFEF')
            self.vote.config(
                text='⚪ Vote  ', background='#0077CC', foreground='#EFEFEF')
            self.done.config(
                text='⚪ Done ', background='#0077CC', foreground='#EFEFEF')
        elif cont == Vote:
            self.vote.config(
                text='⚫ Vote  ', background='#EFEFEF', foreground='#0077CC')
            self.home.config(
                text='⚪ Home', background='#0077CC', foreground='#EFEFEF')
            self.clss.config(
                text='⚪ Class*', background='#0077CC', foreground='#EFEFEF')
            self.done.config(
                text='⚪ Done ', background='#0077CC', foreground='#EFEFEF')
        else:
            self.done.config(
                text='⚫ Done ', background='#EFEFEF', foreground='#0077CC')
            self.home.config(
                text='⚪ Home', background='#0077CC', foreground='#EFEFEF')
            self.clss.config(
                text='⚪ Class*', background='#0077CC', foreground='#EFEFEF')
            self.vote.config(
                text='⚪ Vote  ', background='#0077CC', foreground='#EFEFEF')

        if self.frame_n is not None:
            self.frame_n.pack_forget()

        self.frame_n = frame
        self.frame_n.pack(side='right', expand=True, fill='both')

    def about(self) -> str:
        """Dialog box of about."""
        mg.showinfo(
            'About', f'Version: {__version__}\nAuthor: {__author__}, 12\'A, 2019-20\nArmy Public School\nMathura Cantt\nPrinciple - Mrs. Gayatri Kulshreshtha\nTeacher - Mr. Amit Bansal, PGT - Comp.Sc', parent=self)

    def ext(self):
        if Ent_Box(self, icn=Root.DATAFILE[0]).get():
            self.master.destroy()

    @staticmethod
    def session() -> str:
        """Return current session."""
        yr = date.today().strftime('%Y')  # Return Year only
        ssn = str(yr) + ' - ' + f'{int(yr) + 1}'
        return ssn

    # NAVBAR______________________________
    def navbar(self):
        """Left sided navbar for main window."""
        fl = tk.Frame(self, background='#0077CC', width=223)
        fl.pack(side='left', expand=0, fill='y')
        fl.pack_propagate(0)
        # NAVBAR's internal items______________________________
        flt = tk.Frame(fl, height=55)
        flt.pack(side='top', fill='both', expand=1)
        flt.pack_propagate(0)
        self.lg_img = ImageTk.PhotoImage(Image.open(Root.DATAFILE[1]))
        lg_canv = tk.Canvas(flt, borderwidth=0, highlightthickness=0)
        lg_canv.place(x=0, y=0, relheight=1, relwidth=1, anchor='nw')
        lg_canv.create_image(0, 0, image=self.lg_img, anchor='nw')
        lg_canv.create_text(108, 45, text='» ' + self.session(),
                            fill='#EFEFEF', font=('Segoe UI', 18, 'bold'))
        lg_canv.bind('<Button-1>', self.get_pos)
        lg_canv.bind('<B1-Motion>', lambda event: self.geometry(
            f'+{event.x_root+self.xwin}+{event.y_root+self.ywin}'))

        flb = tk.Frame(fl, background='#0077CC')
        flb.pack(side='bottom', fill='x', expand=1, anchor='s')
        btxlb = tk.Button(flb, text='X', highlightthickness=0, background='#FF3232', activebackground='#FF4C4C',
                          relief='flat', borderwidth=1, foreground='#EFEFEF', height=2, command=self.ext, font=('Segoe UI', 10, 'bold'))
        btxlb.pack(side='left', fill='x', expand=1, anchor='s')
        bthlb = tk.Button(flb, text='?', highlightthickness=0, background='#303030', activebackground='#6D6D6D',
                          relief='flat', borderwidth=1, foreground='#EFEFEF', height=2, command=self.about, font=('Segoe UI', 10, 'bold'))
        bthlb.pack(side='left', fill='x', expand=1, anchor='s')
        # NAVBAR's Content______________________________
        self.home = tk.Label(fl, text='⚪ Home', foreground='#FFFFFF',
                             background='#0077CC', font=('Segoe UI', 16, 'bold'))
        self.home.pack(side='top', ipady=20, fill='x')
        self.clss = tk.Label(fl, text='⚪ Class*', foreground='#FFFFFF',
                             background='#0077CC', font=('Segoe UI', 16, 'bold'))
        self.clss.pack(side='top', ipady=20, fill='x')
        self.vote = tk.Label(fl, text='⚪ Vote  ', foreground='#FFFFFF',
                             background='#0077CC', font=('Segoe UI', 16, 'bold'))
        self.vote.pack(side='top', ipady=20, fill='x')
        self.done = tk.Label(fl, text='⚪ Done ', foreground='#FFFFFF',
                             background='#0077CC', font=('Segoe UI', 16, 'bold'))
        self.done.pack(side='top', ipady=20, fill='x')

    def get_pos(self, event):
        self.xwin = self.winfo_x() - event.x_root
        self.ywin = self.winfo_y() - event.y_root


class Home(tk.Frame):
    """Constructs a frame for selection of type of voting, Staff or Students."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure('TLabelframe.Label', font=('Segoe UI', 17))
        ttk.Style().configure('1.TButton', font=('Segoe UI', 15))
        self.config(background=Win.SM_BG_HEX)

        btnfrm = ttk.LabelFrame(self, text='Choose', padding=10)
        btnfrm.pack(pady=160)
        btnt = ttk.Button(btnfrm, text='Staff', style='1.TButton',
                          command=lambda:  self.tch_sel(btnt, btns))
        btnt.pack(pady=(0, 8))
        btns = ttk.Button(btnfrm, text='Students', style='1.TButton',
                          command=lambda: self.std_sel(btns, btnt))
        btns.pack()

    def tch_sel(self, *args: ttk.Button):
        """Takes to Vote frame if Staff selected."""
        global sel
        btn1, btn2, = args
        sel = 0  # for Staff, direct to Vote
        btn1.config(state='disabled')
        btn2.config(state='disabled')
        if Tokens(self).check() is False:
            root.destroy()
            exit()
        Sql_init(1, master=self).tbl()
        if Ent_Box(self, 'Enter SuperKey & Confirm to Continue.', Root.DATAFILE[0], 'key').get() and Sql_init.NXT == 1:
            app.replace_frame(Vote)
        else:
            btn1.config(state='enabled')
            btn2.config(state='enabled')

    def std_sel(self, *args: ttk.Button):
        """Takes to Class frame if Students selected."""
        global sel
        btn1, btn2, = args
        sel = 1  # for students, move to Class frame
        btn1.config(state='disabled')
        btn2.config(state='disabled')
        if Tokens(self).check() is False:
            root.destroy()
            exit()
        Sql_init(1, master=self).tbl()
        if Ent_Box(self, 'Enter SuperKey & Confirm to Continue.', Root.DATAFILE[0], 'key').get() and Sql_init.NXT == 1:
            app.replace_frame(Class)
        else:
            btn1.config(state='enabled')
            btn2.config(state='enabled')


class Class(tk.Frame):
    """Constructs a Class frame to choose a class & section for the students."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure('1.TButton', font=('Segoe UI', 12))
        self.config(background=Win.SM_BG_HEX)
        clss_lst = [str(i) for i in list(Access_Config().clss_config.keys())]

        btnfrm_class = ttk.LabelFrame(self, text='Class', padding=10)
        btnfrm_class.pack(side='top', pady=(150, 0))
        btn_class = ttk.Combobox(
            btnfrm_class, values=clss_lst, state='readonly')
        btn_class.set('Select')
        btn_class.pack()

        btnfrm_sec = ttk.LabelFrame(self, text='Section', padding=10)
        btnfrm_sec.pack(pady=(20, 0))
        btn_sec = ttk.Combobox(btnfrm_sec, state='readonly')
        btn_sec.set('Select')
        btn_sec.pack()

        btnnxt = ttk.Button(self, text='Next', style='1.TButton', command=lambda: self.mv_Vote(
            btn_class.get(), btn_sec.get()), state='disabled')
        btnnxt.pack(side='bottom', pady=(0, 10))

        btn_class.bind('<<ComboboxSelected>>', lambda event: (
            btn_sec.config(values=Access_Config().clss_config[int(btn_class.get())])))
        btn_sec.bind('<<ComboboxSelected>>',
                     lambda event: btnnxt.config(state='enabled'))

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
        ttk.Style().configure('TLabelframe.Label', font=('Segoe UI', 13))
        ttk.Style().configure('1.TButton', font=('Segoe UI', 15))
        self.config(background=Win.SM_BG_HEX)

        cls_txt = tk.Label(self, text='', font=(
            'Segoue UI', 12, 'bold'), bg='#C39EFF', fg='#FFFFFF')
        cls_txt.pack(side='top', anchor='n', fill='x')
        if sel == 1:
            cls_txt.config(text=f'{ch_clss}\' {ch_sec}')
        else:
            cls_txt.config(text='Staff')

        tkn_frm = ttk.LabelFrame(self, text='Token', padding=10)
        tkn_frm.pack(pady=(50, 0))

        uppr = tk.Frame(self, background=Win.SM_BG_HEX)
        uppr.pack(pady=(40, 20))
        lwr = tk.Frame(self, background=Win.SM_BG_HEX)
        lwr.pack()

        self.chk_val = 0
        tkn_reg = self.register(self.tkn_check)
        self.tkn_ent = ttk.Entry(tkn_frm, validate='key',
                               validatecommand=(tkn_reg, '%P'))
        self.tkn_ent.pack()

        bhead = ttk.LabelFrame(uppr, text='HeadBoy', padding=10)
        bhead.pack(side='left', padx=(0, 10))
        vbhead = ttk.LabelFrame(uppr, text='ViceHeadBoy', padding=10)
        vbhead.pack(side='left')
        ghead = ttk.LabelFrame(lwr, text='HeadGirl', padding=10)
        ghead.pack(side='left', padx=(0, 10))
        vghead = ttk.LabelFrame(lwr, text='ViceHeadGirl', padding=10)
        vghead.pack(side='left')

        self.bhead_ch = ttk.Combobox(bhead, values=Sql_init(
            0).db_cands()['HB'], state='readonly')
        self.bhead_ch.set('Select')
        self.bhead_ch.pack()

        self.vbhead_ch = ttk.Combobox(vbhead, values=Sql_init(
            0).db_cands()['VHB'], state='readonly')
        self.vbhead_ch.set('Select')
        self.vbhead_ch.pack()

        self.ghead_ch = ttk.Combobox(ghead, values=Sql_init(
            0).db_cands()['HG'], state='readonly')
        self.ghead_ch.set('Select')
        self.ghead_ch.pack()

        self.vghead_ch = ttk.Combobox(vghead, values=Sql_init(
            0).db_cands()['VHG'], state='readonly')
        self.vghead_ch.set('Select')
        self.vghead_ch.pack()

        self.btnvt = ttk.Button(self, text='Vote', style='1.TButton', state='disabled', command=lambda: (
            self.mv_Done(self.btnvt, self.bhead_ch.get(), self.vbhead_ch.get(), self.ghead_ch.get(), self.vghead_ch.get())))
        self.btnvt.pack(side='bottom', pady=(0, 10))
        self.bhead_ch.bind('<<ComboboxSelected>>', lambda event: self.chk_vote())
        self.vbhead_ch.bind('<<ComboboxSelected>>', lambda event: self.chk_vote())
        self.ghead_ch.bind('<<ComboboxSelected>>', lambda event: self.chk_vote())
        self.vghead_ch.bind('<<ComboboxSelected>>', lambda event: self.chk_vote())

    def tkn_check(self, inp: str) -> bool:
        """Restricts all but numbers and that too upto 5 digits only."""
        self.chk_val = 1
        self.chk_vote()
        if (inp.isalnum() or inp is '') and len(inp) <= 8:
            return True
        else:
            return False

    def chk_vote(self):
        """Makes sure Vote button stays disabled untill a candidate has been selected in each menu."""
        btn = self.btnvt
        args=(self.bhead_ch.get(), self.vbhead_ch.get(),
              self.ghead_ch.get(), self.vghead_ch.get())
        n=0
        m=0
        for j in [Sql_init(0).db_cands()[x] for x in list(Sql_init(0).db_cands().keys())]:
            if args[m] in j:
                n += 1
            m += 1
        if n == 4 and self.chk_val == 1:
            btn.config(state='enabled')

    def mv_Done(self, btnvt: ttk.Button, *args: str):
        """Move to Done frame while saving votes in database through the logic module."""
        global vte_lst  # Votes of 1 turn
        if Tokens(self).get(self.tkn_ent.get()):
            if mg.askokcancel('Confirm', 'Are you sure?', parent=self):
                vte_lst=list(args)
                vte_lst[0], vte_lst[1], vte_lst[2], vte_lst[
                    3]=f'HB_{vte_lst[0]}', f'VHB_{vte_lst[1]}', f'HG_{vte_lst[2]}', f'VHG_{vte_lst[3]}'
                if sel == 0:  # Staff
                    btnvt.config(state='disabled')
                    Sql_init(0).tchr_vte(vte_lst)
                    app.replace_frame(Done_0)
                else:  # Students
                    btnvt.config(state='disabled')
                    Sql_init(0).std_vte(vte_lst, ch_clss, ch_sec)
                    app.replace_frame(Done_1)


class Done(tk.Frame):
    """Constructs a Done frame providing options for Next or to end session."""

    def __init__(self, parent: Win):
        tk.Frame.__init__(self, parent)
        ttk.Style().configure('1.TButton', font=('Segoe UI', 15))
        self.config(background=Win.SM_BG_HEX)

        cls_txt=tk.Label(self, text='', font=(
            'Segoue UI', 12, 'bold'), bg='#C39EFF', fg='#FFFFFF')
        cls_txt.pack(side='top', anchor='n', fill='x')
        if sel == 1:
            cls_txt.config(text=f'{ch_clss}\' {ch_sec}')
        else:
            cls_txt.config(text='Staff')

        botmos=tk.Frame(self, background=Win.SM_BG_HEX)
        botmos.pack(fill='x', pady=(170, 100))
        self.lowos=tk.Frame(self, background=Win.SM_BG_HEX)
        self.lowos.pack(side='bottom', pady=(0, 30))
        klb=tk.Label(botmos, text='Done', font=(
            'Segoe UI', 35, 'bold'), background='#29B539', foreground='#FFFFFF')
        klb.pack(fill='x')

    def bck_vote_next(self):
        """Moves to Vote frame again."""
        app.replace_frame(Vote)

    @staticmethod
    def bck_chng_clss_save():
        """Moves to Class frame from calling on in the Close/Continue Dialog box which requires passsword."""
        if Ent_Box(app, icn=Root.DATAFILE[0]).get():
            app.replace_frame(Class)


class Done_0(Done):
    """Inheritates from Done frame and is to be used while Staff voting."""

    def __init__(self, parent: Win):
        Done.__init__(self, parent)
        bcktovote=ttk.Button(self.lowos, text='Next',
                               style='1.TButton', command=self.bck_vote_next)
        bcktovote.pack(side='left')


class Done_1(Done):
    """Inheritates from Done frame, also have a additional Change class button
    and is to be used while Students voting."""

    def __init__(self, parent: Win):
        Done.__init__(self, parent)
        bcktovote=ttk.Button(self.lowos, text='Next',
                               style='1.TButton', command=self.bck_vote_next)
        bcktovote.pack(side='left', padx=(0, 40))
        bcktoclss=ttk.Button(self.lowos, text='Change Class*',
                               style='1.TButton', command=self.bck_chng_clss_save)
        bcktoclss.pack(side='left')


if __name__ == '__main__':
    root=Root()
    root.lower()
    root.iconify()

    app=Win(root)
    app.mainloop()

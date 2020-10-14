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
import sqlite3 as sql
from datetime import date
from tkinter import messagebox as mg

from votm.config import Config
from votm.locations import DATA_PATH


class Sql_init:
    """Establishes connection with the requested database."""

    TBL_NM = "votm_vte"
    NXT = 1

    def __init__(self, _key: int, yr=None, master=None):
        self.master = master
        Sql_init.NXT = 1
        self.yr = date.today().strftime("%Y")
        if yr:
            self.db = os.path.join(DATA_PATH, f"votm_{yr}.db")
        else:
            self.db = os.path.join(DATA_PATH, f"votm_{self.yr}.db")

        self.con = sql.connect(self.db, isolation_level=None)
        if _key:
            mg.showinfo(
                "Connection Established",
                "Connection to the Database has been successfully established.",
                parent=master,
            )
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
            cand_lst = [
                [eval(x)[-1], Config().load("candidate")[x]]
                for x in list(Config().load("candidate").keys())
            ]
            tbl_cand = Sql_init(0).cols(self.yr)[0]
            tbl_cand = tbl_cand[4 : len(tbl_cand)]
            if tbl_cand == []:
                pass
            else:
                chk_cand = []
                for i in range(len(cand_lst)):
                    for j in range(len(cand_lst[i][1])):
                        pst_cand = f"{cand_lst[i][0]}_{cand_lst[i][1][j]}"
                        chk_cand.append(pst_cand)
                if any([i not in tbl_cand for i in chk_cand]) or any(
                    [i not in chk_cand for i in tbl_cand]
                ):
                    ch = mg.askyesnocancel(
                        "Voting Master",
                        "The Data in the Settings and in the Database are different.\nDo you want to Recreate the Database with the New Data<Yes>, Or Continue with the Data in the Database<No>?",
                        parent=self.master,
                    )
                    if ch is True:
                        __drp_sy = f"DROP TABLE {Sql_init.TBL_NM}"
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
                        pst_cand = f"{cand_lst[i][0]}_{cand_lst[i][1][j]}"
                        __tbl_upd_sy = f"ALTER TABLE {Sql_init.TBL_NM} ADD {pst_cand} INT DEFAULT(NULL)"
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
            vte_lst = repr(vte_lst).replace("'", "").strip("[]")
            __tbl_upd_sy = f"""
            UPDATE {Sql_init.TBL_NM}
            SET STAFF = STAFF + 1, {vte_lst}
            WHERE STAFF IS NOT NULL
            """
            self.cur.execute(__tbl_upd_sy)
        else:  #! does not exist i.e Create
            tbl_cand, _ = Sql_init(0).cols(self.yr)
            tbl_cand = tbl_cand[4 : len(tbl_cand)]
            temp, _ = Sql_init(0).cols(self.yr)
            temp = temp[4 : len(temp)]
            for i in range(len(temp)):
                if temp[i] in vte_lst:
                    temp[i] = 1
                else:
                    temp[i] = 0
            cand = str(tbl_cand).strip("[]")
            cand = cand.replace("'", "")
            """
            *This can be used too for above requirements->
            !<str>.translate(str.marktrans({"'":None}))
            """
            __tbl_ins_sy = f"""INSERT INTO {Sql_init.TBL_NM}(
                STAFF, {cand}
                )
            VALUES(
                1, {str(temp).strip("[]")}
            )
            """
            self.cur.execute(__tbl_ins_sy)

    def std_vte(self, *args: "(list, str, str)"):
        """Updates database with selected entries."""
        vte_lst, clss, sec = args
        __tbl_chk_sy = f"""SELECT CLASS, SEC FROM {Sql_init.TBL_NM}
        WHERE CLASS = {clss} AND SEC LIKE '{sec}'"""
        self.cur.execute(__tbl_chk_sy)
        val = self.cur.fetchone()
        if val is not None:  #! UPDATE block
            vte_lst = [f"{i} = {i} + 1" for i in vte_lst]
            vte_lst = repr(vte_lst).replace("'", "").strip("[]")
            __tbl_upd_sy = f"""
            UPDATE {Sql_init.TBL_NM}
            SET STUDENT = STUDENT + 1, {vte_lst}
            WHERE CLASS = {clss} AND SEC LIKE '{sec}'
            """
            self.cur.execute(__tbl_upd_sy)
        else:  #! CREATE block
            tbl_cand, _ = Sql_init(0).cols(self.yr)
            tbl_cand = tbl_cand[4 : len(tbl_cand)]
            temp, _ = Sql_init(0).cols(self.yr)
            temp = temp[4 : len(temp)]
            for i in range(len(temp)):
                if temp[i] in vte_lst:
                    temp[i] = 1
                else:
                    temp[i] = 0
            cand = str(tbl_cand).replace("'", "").strip("[]")
            __tbl_ins_sy = f"""INSERT INTO {Sql_init.TBL_NM}(
                CLASS, SEC, STUDENT, {cand}
                )
            VALUES(
                {clss}, '{sec}', 1, {str(temp).strip("[]")}
            )
            """
            #! Single qoutes in string above
            self.cur.execute(__tbl_ins_sy)

    def result(self, *args: "(String of fields to be shown)"):
        """Provides result in the form of list containing Records & Fields."""
        # ? args -> ('STAFF, STUDENT, CLASS, SEC, HB_A, HB_C...',)
        # * args = str(args).lstrip("('").rstrip("',)")
        args = args[0]
        if (
            args.find("CLASS", 0, len(args)) == -1
            and args.find("SEC", 0, len(args)) == -1
            and args.find("STUDENT", 0, len(args)) == -1
            and args.find("STAFF", 0, len(args)) != -1
        ):
            __res_sel_sy = f"""
            SELECT {args} FROM {Sql_init.TBL_NM}
            WHERE STAFF IS NOT NULL
            ORDER BY CLASS
            """
        elif (
            args.find("CLASS", 0, len(args)) == -1
            and args.find("SEC", 0, len(args)) == -1
            and args.find("STUDENT", 0, len(args)) != -1
        ):
            if args.find("STAFF", 0, len(args)) == -1:
                args = (
                    repr(
                        [
                            f"SUM({i}) AS {i}"
                            for i in [i.strip() for i in args.split(",")]
                        ]
                    )
                    .replace("'", "")
                    .strip("[]")
                )
                __res_sel_sy = f"""
                SELECT {args} FROM {Sql_init.TBL_NM}
                WHERE STUDENT IS NOT NULL
                ORDER BY CLASS
                """
            else:
                args = (
                    repr(
                        [
                            f"SUM({i}) AS {i}"
                            for i in [i.strip() for i in args.split(",")]
                            if i != "STAFF"
                        ]
                    )
                    .replace("'", "")
                    .strip("[]")
                )
                __res_sel_sy = f"""
                SELECT STAFF, {args} FROM {Sql_init.TBL_NM}
                GROUP BY STAFF
                ORDER BY CLASS
                """
        elif (
            args.find("SEC", 0, len(args)) == -1
            and args.find("CLASS", 0, len(args)) != -1
        ):
            if args.find("STAFF", 0, len(args)) == -1:
                args = (
                    repr(
                        [
                            f"SUM({i}) AS {i}"
                            for i in [i.strip() for i in args.split(",")]
                            if i != "CLASS" and i != "STAFF"
                        ]
                    )
                    .replace("'", "")
                    .strip("[]")
                )
                __res_sel_sy = f"""
                SELECT CLASS, {args} FROM {Sql_init.TBL_NM}
                WHERE STUDENT IS NOT NULL
                GROUP BY CLASS
                ORDER BY CLASS
                """
            else:
                args = (
                    repr(
                        [
                            f"SUM({i}) AS {i}"
                            for i in [i.strip() for i in args.split(",")]
                            if i != "CLASS" and i != "STAFF"
                        ]
                    )
                    .replace("'", "")
                    .strip("[]")
                )
                __res_sel_sy = f"""
                SELECT STAFF ,CLASS, {args} FROM {Sql_init.TBL_NM}
                GROUP BY CLASS
                ORDER BY CLASS
                """
        elif (
            args.find("CLASS", 0, len(args)) != -1
            or args.find("SEC", 0, len(args)) != -1
            or args.find("STUDENT", 0, len(args)) != -1
        ) and args.find("STAFF", 0, len(args)) == -1:
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
        (yr,) = args
        self.con.close()
        db = os.path.join(DATA_PATH, f"votm_{yr}.db")
        con = sql.connect(db, isolation_level=None)
        cur = con.cursor()
        __dsc_sy = f"PRAGMA table_info({Sql_init.TBL_NM})"
        cur.execute(__dsc_sy)
        desc = cur.fetchall()
        cols = [tup[1] for tup in desc]
        con.close()
        return cols, desc

    def db_cands(self):
        """Returns candidates in the database."""
        self.cur.execute("PRAGMA table_info(votm_vte)")
        desc = self.cur.fetchall()
        cols = [
            tup[1] for tup in desc if tup[1] not in ["STAFF", "CLASS", "SEC", "STUDENT"]
        ]
        cols = [i.split("_") for i in cols]
        # ? dfl = {'HB': [], 'VHB': [], 'HG': [], 'VHG': []}
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

    def mrg_dtb_res(
        self, *args: "(list of tables, list of (tables desc, records))", name="merged"
    ):
        """Creates "merged" named database consisting merged result."""
        (
            tbl,
            vals,
        ) = args
        __fnl_sy = f"""CREATE TABLE {Sql_init.TBL_NM} \nAS """
        datype, _ = vals[0]
        lst = (
            repr(
                [
                    f"SUM({j}) AS {j}"
                    for j in [i[0] for i in list(datype)]
                    if j != "CLASS" and j != "SEC"
                ]
            )
            .replace("'", "")
            .strip("[]")
        )
        __fnl_sy += f"""SELECT CLASS, SEC, {lst}\nFROM (\n"""
        for i in range(len(tbl)):
            (
                datype,
                rcrds,
            ) = vals[i]
            # * datype = str(tuple([(repr(i).replace(',', ' ')).strip("()") for i in datype])).replace(
            # *     '"', "").replace("'", '')
            datype = repr(
                tuple(
                    [
                        (repr(i).replace(",", " ")).strip("()").replace("'", "")
                        for i in datype
                    ]
                )
            ).replace("'", "")
            if len(rcrds) > 1:
                rcrds = (
                    "("
                    + repr(
                        tuple(
                            [
                                repr(b).replace("None", "NULL").replace("'", '"')
                                for b in rcrds
                            ]
                        )
                    )
                    .replace("'", "")
                    .strip("()")
                    + ")"
                )
            else:
                rcrds = (
                    "("
                    + tuple(
                        [
                            repr(b).replace("None", "NULL").replace("'", '"')
                            for b in rcrds
                        ]
                    )[0].replace("'", "")
                    + ")"
                )
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

        __fnl_sy = __fnl_sy.rstrip("UNION ALL\n")
        __fnl_sy += "\n)\nGROUP BY CLASS, SEC"
        try:
            self.cur.execute(__fnl_sy)
            #!###########################
            #!## Recreating the tabel ###
            #!###########################
            cols, _ = Sql_init(0).cols(name)
            cols = [i for i in cols if not i in ["CLASS", "SEC", "STAFF", "STUDENT"]]
            val = self.gen_mrg_fle()
            if len(val) > 1:
                val = repr(val).replace("None", "NULL").replace("'", '"').strip("[]")
            else:
                val = repr(val[0]).replace("None", "NULL").replace("'", '"')
            """
            Ot_ways:
            val = [tuple(map(lambda x: "NULL" if x==None else x, i)) for i in self.gen_mrg_fle()]
            """
            __drp_sy = f"DROP TABLE {Sql_init.TBL_NM}"
            self.cur.execute(__drp_sy)
            __tbl_sy = f"""CREATE TABLE IF NOT EXISTS {Sql_init.TBL_NM}(
                CLASS INT(2) DEFAULT(NULL),
                SEC VARCHAR(1) DEFAULT(NULL),
                STAFF INT DEFAULT(NULL),
                STUDENT INT DEFAULT(NULL))"""
            self.cur.execute(__tbl_sy)
            for i in cols:
                __tbl_upd_sy = (
                    f"ALTER TABLE {Sql_init.TBL_NM} ADD {i} INT DEFAULT(NULL)"
                )
                self.cur.execute(__tbl_upd_sy)
            __ins_sy = f"""
            INSERT INTO {Sql_init.TBL_NM}
            VALUES {val}
            """
            self.cur.execute(__ins_sy)
            #!###########
            #!## DONE ###
            #!###########
        except:
            __drp_sy = f"DROP TABLE {Sql_init.TBL_NM}"
            self.cur.execute(__drp_sy)
            for i in tbl:
                __drp_sy = f"""
                DROP TABLE IF EXISTS {i}
                """
                self.cur.execute(__drp_sy)
            Sql_init(0, yr=name).mrg_dtb_res(tbl, vals, name=name)
        finally:
            for i in tbl:
                __drp_sy = f"""
                DROP TABLE IF EXISTS {i}
                """
                self.cur.execute(__drp_sy)


class Yr_fle:
    """Creates a list of names of database files existing."""

    yr = []
    fle = []

    def __init__(self):
        fle = []
        Yr_fle.fle = fle
        for _, _, f in os.walk(DATA_PATH):
            for file in f:
                if ".db" in file:
                    if "votm_" in file:
                        fle.append(file)
        yr = [i.replace("votm_", "").replace(".db", "") for i in fle]
        Yr_fle.yr = yr
        Yr_fle.fle = fle

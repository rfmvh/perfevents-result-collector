#!/usr/bin/env python

import argparse
import sys
import logging

from perfresultcollector import set_logger_level
from dbinterface import *

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--cmd", action="store", dest="cmd")
parser.add_argument("--description", action="store", dest="description")
parser.add_argument("--systemwide", action="store_true",
                    default=False, dest="systemwide")
parser.add_argument("--force", action="store_true",
                    default=False, dest="force")

options = parser.parse_args()

log = logging.getLogger(__name__)


def add(name, cmd, desc, syst_wide, force):
    # open DB
    db = DBConnection()
    if not name:
        log.warning("Insert the name of the experiment")
        sys.exit(1)

    sql_query = 'SELECT exp_id FROM experiments WHERE name = %(exp_name)s;'
    sql_params = {'exp_name': name}
    results = db.query(sql_query, sql_params)

    if results:
        if not force:
            log.warning("Name exists")
            sys.exit(1)
        sql_query_update = 'UPDATE experiments SET cmd = %(exp_cmd)s, description = %(exp_desc)s,' \
                           ' systemwide = %(exp_systemwide)s WHERE name=%(exp_name)s;'
        sql_params_update = {'exp_cmd': cmd, 'exp_desc': desc,
                             'exp_systemwide': syst_wide, 'exp_name': name}
        db.query(sql_query_update, sql_params_update, fetchall=False)
    else:
        ql_query_insert = 'INSERT INTO experiments (name, cmd, description, systemwide)' \
                        ' VALUES (%(exp_name)s, %(exp_cmd)s, %(exp_desc)s, %(exp_systemwide)s);'
        sql_params_insert = {'exp_name': name, 'exp_cmd': cmd, 'exp_desc': desc, 'exp_systemwide': syst_wide}
        db.query(sql_query_insert, sql_params_insert)

if __name__ == '__main__':
    add(options.name, options.cmd, options.description,
        options.systemwide, options.force)

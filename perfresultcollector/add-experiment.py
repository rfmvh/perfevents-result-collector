#!/usr/bin/env python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--cmd", action="store", dest="cmd")
optparser.add_option("", "--description", action="store", dest="description")
optparser.add_option("", "--systemwide", action="store_true", default=False, dest="systemwide")
optparser.add_option("", "--force", action="store_true", default=False, dest="force")

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()


def add(name, cmd, desc, systWide, force):
    if not name:
        print "Error: Insert the name of the experiment"
        sys.exit(1)

    else:
        sql_query = 'SELECT exp_id FROM experiments WHERE name = %(exp_name)s;'
        sql_params = {'exp_name': name}

        results = db.query(sql_query, sql_params)

        if not results:
            # Vlozeni do db
            sql_query_insert = 'INSERT INTO experiments (name, cmd, description, systemwide) VALUES (%(exp_name)s, %(exp_cmd)s, %(exp_desc)s, %(exp_systemwide)s);'
            sql_params_insert = {'exp_name': name, 'exp_cmd': cmd, 'exp_desc': desc, 'exp_systemwide': systWide}
            db.query(sql_query_insert, sql_params_insert)

        else:
            if not force:
                # Error
                print "Error: Name exists"
                sys.exit(1)

            else:
                # Prepsat v DB - update
                sql_query_update = 'UPDATE experiments SET cmd = %(exp_cmd)s, description = %(exp_desc)s, systemwide = %(exp_systemwide)s WHERE name=%(exp_name)s;'
                sql_params_update = {'exp_cmd': cmd, 'exp_desc': desc, 'exp_systemwide': systWide, 'exp_name': name}
            db.query(sql_query_update, sql_params_update)


add(options.name, options.cmd, options.description, options.systemwide, options.force)

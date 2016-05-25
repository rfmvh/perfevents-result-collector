#!/usr/bin/python

import sys
import re
import os

from dbinterface import *

reg_parse = re.compile(r"""
                      (?P<arch>\w+);
                      (?P<vendor>\w+);
                      (?P<cpuFamily>\d+);
                      (?P<cpuModel>\d+);
                      (?P<microarch>[\w\-]+)
                      """, re.VERBOSE)

arch=None
vendor=None
cpuModel=None
cpuFamily=None

db = DBConnection()

for line in sys.stdin:
  match = reg_parse.match(line)
  if match:
    arch=match.group("arch")
    vendor=match.group("vendor")
    cpuModel=match.group("cpuModel")
    cpuFamily=match.group("cpuFamily")
    microarch=match.group("microarch")
    
    sql_query = """UPDATE environments AS e 
                SET microarch = %(microarch)s 
                FROM environments
                INNER JOIN vendors AS v ON environments.vendor_id=v.vendor_id 
                WHERE e.arch = %(arch)s  and v.name = %(vendor)s and e.family = %(cpuFamily)s and e.model = %(cpuModel)s;"""
    sql_params = {'microarch': microarch, 'arch':arch, 'vendor': vendor, 'cpuFamily': cpuFamily, 'cpuModel' : cpuModel}
  
    results = db.query(sql_query, sql_params)

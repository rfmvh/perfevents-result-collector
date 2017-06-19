#!/usr/bin/python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")

(options, args) = optparser.parse_args() 

# open DB
db = DBConnection()


def show_virt(name, csv):
  if name:
    sql_query = 'SELECT * FROM virt WHERE name = %(virt_name)s;'
    sql_params = {'virt_name': name}
    
    results = db.select(sql_query, sql_params)
    
    if not results:
      print "Error: Name does not exist"
      sys.exit(1)     
                
  else:
    sql_query = 'SELECT * FROM virt;'
    
    results = db.select(sql_query)
      
  if csv:
    print "#name"
    for line in results:
      print "%s" % (line[1])
    
  else:
    print "name"
    for line in results:
      print "%s" % (line[1])

show_virt(options.name, options.csv)

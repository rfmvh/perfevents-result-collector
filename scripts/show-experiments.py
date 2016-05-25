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


def show_experiment(name, csv):
  if name:
    sql_query = 'SELECT * FROM experiments WHERE name = %(exp_name)s;'
    sql_params = {'exp_name': name}
    
    results = db.select(sql_query, sql_params)
    
    if not results:
      print "Error: Name does not exist"
      sys.exit(1)
                
  else:
    sql_query = 'SELECT * FROM experiments;'
    
    results = db.select(sql_query)
      
  if csv:
    print "#name;system-wide;cmd;description"
    for line in results:
      print "%s;%s;%s;%s" % (line[4], line[3], line[1], line[2])
    
  else:
    print "name system-wide cmd description"
    for line in results:
      print "%s %s %s %s" % (line[4], line[3], line[1], line[2])

show_experiment(options.name, options.csv)

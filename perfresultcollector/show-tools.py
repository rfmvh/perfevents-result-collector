#!/usr/bin/python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--version", action="store", dest="version")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")

(options, args) = optparser.parse_args() 

# open DB
db = DBConnection()


def show_tool(name, version, csv):
  if name and version:
    sql_query = 'SELECT * FROM tools WHERE name = %(tool_name)s and version = %(tool_version)s;'
    sql_params = {'tool_name': name, 'tool_version': version}
    
    results = db.select(sql_query, sql_params)
    
    if not results:
      print "Error: Name with version does not exist"
      sys.exit(1)
      
  elif name:
    sql_query = 'SELECT * FROM tools WHERE name = %(tool_name)s;'
    sql_params = {'tool_name': name}
    
    results = db.select(sql_query, sql_params)
    
    if not results:
      print "Error: Name does not exist"
      sys.exit(1)
                
                
  else:
    sql_query = 'SELECT * FROM tools;'
    
    results = db.select(sql_query)
      
  if csv:
    print "#name;version"
    for line in results:
      print "%s;%s" % (line[1], line[2])
    
  else:
    print "name version"
    for line in results:
      print "%s %s" % (line[1], line[2])

show_tool(options.name, options.version, options.csv)

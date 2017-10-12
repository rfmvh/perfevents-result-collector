#!/usr/bin/python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--idgroup", action="store", dest="idGroup")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")

(options, args) = optparser.parse_args() 

# open DB
db = DBConnection()


def show_event(name, idGroup, csv):
  if name:
    sql_query = 'SELECT * FROM events WHERE name = %(evt_name)s;'
    sql_params = {'evt_name': name}
    
    results = db.select(sql_query, sql_params)
    
    if not results:
      print "Error: Name does not exist"
      sys.exit(1)
      
  elif idGroup:
    sql_query = 'SELECT * FROM events WHERE idGroup = %(idg)s;'
    sql_params = {'idg': idGroup}
    
    results = db.select(sql_query, sql_params)
    
    if not results:
      print "Error: ID Group does not exist"
      sys.exit(1)
                
                
  else:
    sql_query = 'SELECT * FROM events;'
    
    results = db.select(sql_query)
      
  if csv:
    print "#name;evt_num;nmask;idGroup"
    for line in results:
      print "%s;%s;%s;%s" % (line[1], line[2], line[3], line[4])
    
  else:
    print "name evt_num nmask idGroup"
    for line in results:
      print "%s %s %s %s" % (line[1], line[2], line[3], line[4])

show_event(options.name, options.idGroup, options.csv)

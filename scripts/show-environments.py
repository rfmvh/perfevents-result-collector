#!/usr/bin/python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--arch", action="store", dest="arch")
optparser.add_option("", "--microarch", action="store", dest="microarch")
optparser.add_option("", "--family", action="store", dest="family")
optparser.add_option("", "--model", action="store", dest="model")
optparser.add_option("", "--stepping", action="store", dest="stepping")
optparser.add_option("", "--virt", action="store", dest="virt")
optparser.add_option("", "--kernel", action="store", dest="kernel")
optparser.add_option("", "--vendor", action="store", dest="vendor")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")

(options, args) = optparser.parse_args() 

# open DB
db = DBConnection()


def show_environment(arch, microarch, family, model, stepping, virt, kernel, vendor, csv):
  conditions=""
  sql_params={}
  
  if arch:
    conditions+=" and arch = %(arch)s"
    sql_params['arch'] = arch
    
  if microarch:
    conditions+=" and microarch = %(microarch)s"
    sql_params['microarch'] = microarch
    
  if family:
    conditions+=" and family = %(family)s"
    sql_params['family'] = family
    
  if model:
    conditions+=" and model = %(model)s"
    sql_params['model'] = model
    
  if stepping:
    conditions+=" and stepping = %(stepping)s"
    sql_params['stepping']= stepping
    
  if virt:
    sql_query_virt = 'SELECT virt_id FROM virt WHERE name = %(virt_name)s;'
    sql_params_virt = {'virt_name': virt}
    
    results = db.select(sql_query_virt, sql_params_virt)
    
    conditions+=" and virt_id = %(virt)s "
    sql_params['virt'] = results[0][0]
                  
  if kernel:
    sql_query_kernel = 'SELECT kernel_id FROM kernels WHERE name = %(kernel_name)s;'
    sql_params_kernel = {'kernel_name': kernel}
    
    results = db.select(sql_query_kernel, sql_params_kernel)
    
    conditions+=" and kernel_id = %(kernel)s "
    sql_params['kernel'] = results[0][0]
    
  if vendor:
    sql_query_vendor = 'SELECT vendor_id FROM vendors WHERE name = %(vendor_name)s;'
    sql_params_vendor = {'vendor_name': vendor}
    
    results = db.select(sql_query_vendor, sql_params_vendor)
    
    conditions+=" and vendor_id = %(vendor)s "
    sql_params['vendor'] =  results[0][0]
                 
  sql_query = """ SELECT e.env_id, e.arch, e.microarch, e.family, e.model, e.stepping,  
              virt.name, kernels.name, vendors.name
              FROM environments AS e 
              INNER JOIN virt ON e.virt_id=virt.virt_id
              INNER JOIN kernels ON e.kernel_id=kernels.kernel_id
              INNER JOIN vendors ON e.vendor_id=vendors.vendor_id
              WHERE TRUE"""+ conditions + ';'
  results = db.select(sql_query, sql_params)
    
  if csv:
    print "#arch;microarch;family;model;stepping;virt;kernel;vendor"
    for line in results:
      print "%s;%s;%s;%s;%s;%s;%s;%s" % (line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])
    
  else:
    print "arch microarch family model stepping virt kernel vendor"
    for line in results:
      print "%s %s %s %s %s %s %s %s" % (line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])
show_environment(options.arch, options.microarch, options.family, options.model, options.stepping, options.virt, options.kernel, options.vendor, options.csv)

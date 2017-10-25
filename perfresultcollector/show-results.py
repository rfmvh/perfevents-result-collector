#!/usr/bin/env python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--event", action="store", dest="event", help="name event")
optparser.add_option("", "--event-group", action="store", dest="eventGroup")
optparser.add_option("", "--tool-name", action="store", dest="toolName")
optparser.add_option("", "--tool-version", action="store", dest="toolVersion")
optparser.add_option("", "--experiment", action="store", dest="experiment")
optparser.add_option("", "--cpu-family", action="store", dest="family")
optparser.add_option("", "--cpu-model", action="store", dest="model")
optparser.add_option("", "--cpu-vendor", action="store", dest="vendor")
optparser.add_option("", "--cpu-arch", action="store", dest="arch")
optparser.add_option("", "--cpu-microarch", action="store", dest="microarch")
optparser.add_option("", "--kernel", action="store", dest="kernel")
optparser.add_option("", "--virt", action="store", dest="virt")

optparser.add_option("", "--event-details", action="store_true", default=False, dest="eventD")
optparser.add_option("", "--tool-details", action="store_true", default=False, dest="toolD")
optparser.add_option("", "--experiment-details", action="store_true", default=False, dest="expD")
optparser.add_option("", "--env-details", action="store", dest="envD", help="1 = arch, microarch; 2=arch, microarch, family, model")
optparser.add_option("", "--kernel-details", action="store_true", default=False, dest="kernelD")
optparser.add_option("", "--virt-details", action="store_true", default=False, dest="virtD")

optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")

(options, args) = optparser.parse_args() 

# open DB
db = DBConnection()

def getEnvID(kernelID=None, vendorID=None, virtID=None, family=None, model=None, arch=None, microarch=None):
  _conditions = "TRUE"
  _sql_params = {}
  if kernelID:
    _conditions += " and kernel_id = %(kernelID)s "
    _sql_params['kernelID'] = kernelID
  if virtID:
    _conditions += " and virt_id = %(kernelID)s "
    _sql_params['kernelID'] = kernelID

  if family:
    _conditions += " and family = %(family)s "
    _sql_params['family'] = family

  if model:
    _conditions += " and model = %(model)s "
    _sql_params['model'] = model

  if arch:
    _conditions += " and arch = %(arch)s "
    _sql_params['arch'] = arch

  if microarch:
    _conditions += " and microarch = %(microarch)s "
    _sql_params['microarch'] = microarch

  _sql_query = "SELECT env_id FROM environments WHERE " + _conditions + ";"
  return db.select(_sql_query, _sql_params)


def show_result(event, eventGroup, toolName, toolVersion, experiment, family, model, vendor, arch, microarch, kernel, virt, eventD, toolD, expD, envD, kernelD, virtD, csv):
  conditions=""
  sql_params={}
  
  if event:
    sql_query_event = 'SELECT event_id FROM events WHERE name = %(name)s;'
    sql_params_event = {'name': event}
    
    results = db.select(sql_query_event, sql_params_event)
    
    if not results:
      sys.exit(0)
    
    conditions+=" and r.event_id = %(event)s "
    sql_params['event'] = results[0][0]
    
  if eventGroup:
    sql_query_eventGroup = 'SELECT event_id FROM events WHERE idgroup = %(group)s;'
    sql_params_eventGroup = {'group': eventGroup}
    
    results = db.select(sql_query_eventGroup, sql_params_eventGroup)
    
    if not results:
      sys.exit(0)
    
    conditions+=" and r.evt_id = %(eventGroup)s "
    sql_params['eventGroup'] = results[0][0]
    
  if toolName and toolVersion:
    sql_query_tool = 'SELECT tool_id FROM tools WHERE name = %(name)s and version = %(version)s;'
    sql_params_tool = {'name': toolName, 'version':toolVersion}
    
    results = db.select(sql_query_tool, sql_params_tool)
    
    if not results:
      sys.exit(0)
    
    conditions+=" and r.tool_id = %(tool)s "
    sql_params['tool'] = results[0][0]
  
  elif toolName:
    sql_query_toolName = 'SELECT tool_id FROM tools WHERE name = %(name)s;'
    sql_params_toolName = {'name': toolName}
    
    results = db.select(sql_query_toolName, sql_params_toolName)
    
    if not results:
      sys.exit(0)
    
    conditions+=" and r.tool_id = ANY(%(toolSpec)s) "
    sql_params['toolSpec'] = [i[0] for i in results]
    
  if experiment:
    sql_query_experiment = 'SELECT exp_id FROM experiments WHERE name = %(name)s;'
    sql_params_experiment = {'name': experiment}
    
    results = db.select(sql_query_experiment, sql_params_experiment)
    
    if not results:
      sys.exit(0)
    
    conditions+=" and r.exp_id = %(experiment)s "
    sql_params['experiment'] = results[0][0]
    
  # environment
  vendorID = None
  kernelID = None
  virtID = None

  if kernel:
    sql_query_kernel1 = 'SELECT kernel_id FROM kernels WHERE name = %(name)s;'
    sql_params_kernel1 = {'name': kernel}
    results = db.select(sql_query_kernel1, sql_params_kernel1)
    
    if not results:
      sys.exit(0)
    kernelID = results[0][0]

  if vendor:
    sql_query_vendor1 = 'SELECT vendor_id FROM vendors WHERE name = %(name)s;'
    sql_params_vendor1 = {'name': vendor}
    results = db.select(sql_query_vendor1, sql_params_vendor1)
    
    if not results:
      sys.exit(0)
    vendorID = results[0][0]

  if virt:
    sql_query_virt1 = 'SELECT virt_id FROM virt WHERE name = %(name)s;'
    sql_params_virt1 = {'name': virt}
    results = db.select(sql_query_virt1, sql_params_virt1)
    
    if not results:
      sys.exit(0)
    virtID = results[0][0]

  environmentID = getEnvID(kernelID, vendorID, virtID, family, model, arch, microarch)

  if environmentID:
    conditions += " and r.env_id = ANY(%(envID)s) "
    sql_params['envID'] = [i[0] for i in environmentID]

                 
  sql_query = """ SELECT r.val, 
              events.name, events.evt_num, events.nmask, events.idgroup,
              tools.name, tools.version,
              experiments.name,
              environments.arch, environments.microarch, environments.family, environments.model,
              kernels.name,
              virt.name
              FROM results AS r
              INNER JOIN experiments ON r.exp_id=experiments.exp_id
              INNER JOIN tools ON r.tool_id=tools.tool_id
              INNER JOIN environments ON r.env_id=environments.env_id
              INNER JOIN events ON r.event_id=events.event_id
              INNER JOIN virt ON environments.virt_id=virt.virt_id
              INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
              INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id
              WHERE TRUE"""+ conditions + ';'
  results = db.select(sql_query, sql_params)

# 0-value; 1-Event name; 2-Event num; 3-Event nmask; 4-ID group; 5-Tool name; 6-Tool version; 7-Experiments Name; 8-arch; ....
# ... 9-microarch; 10-family; 11-model; 12-kernel; 13-virt

  symbol=""
  extract=""
  if csv:
    symbol=";"
    
  else:
    symbol=" "
  
  heading="#value" + symbol + "event" + symbol + "group"
  
  if eventD:
    heading += symbol + "num:nmask"
  
  if toolD:
    heading += symbol + "tool-version"
    
  if expD:
    heading += symbol + "experiment"
    
  if envD=="1":
    heading += symbol + "arch" + symbol + "microarch"

  if envD=="2":
    heading += symbol + "arch" + symbol + "microarch"  + symbol + "family"  + symbol + "model"
    
  if kernelD:
    heading += symbol + "kernel"
    
  if virtD:
    heading += symbol + "virt"
  
  for line in results:
    # Default = value, event name, event - id group
    extract += str(line[0]) + symbol + line[1] + symbol + str(line[4])
    
    if eventD:
      if line[2] and line[3]:
        extract += symbol + str(hex(line[2])) + ":" + str(hex(line[3]))
      else:
        extract += symbol + str(line[2]) + ":" + str(line[3])
    
    if toolD:
      extract += symbol + line[5] + "-" + line[6]
      
    if expD:
      extract += symbol + line[7]
      
    if envD=="1":
      extract += symbol + str(line[8]) + symbol + str(line[9])
      
    if envD=="2":
      extract += symbol + str(line[8]) + symbol + str(line[9]) + symbol + str(line[10]) + symbol + str(line[11])
      
    if kernelD:
      extract += symbol + line[12]
      
    if virtD:
      extract += symbol + line[13]
      
    extract+="\n"
      
  print heading
  print extract
   
show_result(options.event, options.eventGroup, options.toolName, options.toolVersion, options.experiment, options.family, options.model, options.vendor, options.arch, options.microarch, options.kernel, options.virt, options.eventD, options.toolD, options.expD, options.envD, options.kernelD, options.virtD, options.csv)

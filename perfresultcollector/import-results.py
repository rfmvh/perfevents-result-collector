#!/usr/bin/env python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser


def detectCPU_aarch64():
    fileName = "/proc/cpuinfo"

    regParseVariant = re.compile(r"""
                            (?P<name>CPU\svariant)\s*:\s*
                            (?P<value>[\da-fx]+)
                            """, re.VERBOSE)

    regParseRevision = re.compile(r"""
                            (?P<name>CPU\srevision)\s*:\s*
                            (?P<value>\d+)
                            """, re.VERBOSE)

    cpuModel = None  # model is used for variant here
    cpuFamily = None  # we would like to use family for "armv7"
    cpuStepping = None  # stepping is used for revision here
    vendor = "generic_ARM"  # FIXME: we would like to detect APM/ARM/Qualcomm...

    with open(fileName, 'r') as f:
        for line in f:
            match = regParseVariant.match(line)
            if match:
                cpuModel = int(match.group("value"), 0)
            match = regParseRevision.match(line)
            if match:
                cpuStepping = match.group("value")

            if cpuModel and cpuStepping:
                break

        f.close()

    return cpuModel, cpuFamily, cpuStepping, vendor


def detectCPU_ppc():
    fileName = "/proc/cpuinfo"

    regParseRevision = re.compile(r"""
                            (?P<name>revision)\s*:\s*
                            (?P<value>\d+\.\d+)\s+\(pvr\s+
                            (?P<model>[\da-f]+)\s+
                            (?P<rev>[\da-f]+)\)
                            """, re.VERBOSE)

    cpuModel = None  # model will serve for model number (003f fo POWER7, etc.)
    cpuFamily = None  # family is None here
    cpuStepping = None  # stepping will serve for revision here
    vendor = "IBM"  # vendor is always IBM for ppc64

    with open(fileName, 'r') as f:
        for line in f:
            match = regParseRevision.match(line)
            if match:
                cpuModel = int(match.group("model"), 16)
                cpuStepping = int(match.group("rev"), 16)

            if cpuModel and cpuStepping:
                break

        f.close()

    return cpuModel, cpuFamily, cpuStepping, vendor


def detectCPU_x86():
    fileName = "/proc/cpuinfo"

    regParseModel = re.compile(r"""
                            (?P<name>model)\s*:\s*
                            (?P<value>\d+)
                            """, re.VERBOSE)

    regParseFamily = re.compile(r"""
                            (?P<name>cpu\sfamily)\s*:\s*
                            (?P<value>\d+)
                            """, re.VERBOSE)

    regParseStepping = re.compile(r"""
                            (?P<name>stepping)\s*:\s*
                            (?P<value>[\da-fx]+)
                            """, re.VERBOSE)

    regParseVendor = re.compile(r"""
                            (?P<name>vendor_id)\s*:\s*
                            (?P<value>\w+)
                            """, re.VERBOSE)
    cpuModel = None
    cpuFamily = None
    cpuStepping = None
    vendor = None

    with open(fileName, 'r') as f:
        for line in f:
            match = regParseModel.match(line)
            if match:
                cpuModel = match.group("value")
            match = regParseFamily.match(line)
            if match:
                cpuFamily = match.group("value")
            match = regParseStepping.match(line)
            if match:
                cpuStepping = match.group("value")
            match = regParseVendor.match(line)
            if match:
                vendor = match.group("value")
            if cpuFamily and cpuModel and cpuStepping and vendor:
                break

        f.close()

    return cpuModel, cpuFamily, cpuStepping, vendor


# tries to detect environment configuration from /proc/cpuinfo, arch and kernel version from uname
def detectEnv():
    arch = os.popen('uname -m').read().rstrip()
    kernel = os.popen('uname -r').read().rstrip()

    # CPU detection needs to be arch-specific
    if arch == "aarch64":
        r = detectCPU_aarch64()
    elif arch == "ppc64" or arch == "ppc64le":
        r = detectCPU_ppc()
    elif arch == "i386" or arch == "i686" or arch == "x86_64":
        r = detectCPU_x86()

    return arch, kernel, r[0], r[1], r[2], r[3]


# Get kernel id
def dbGetKernelId(db, kernel):
    sql_query = 'SELECT kernel_id FROM kernels WHERE name = %(kernel_name)s;'
    sql_params = {'kernel_name': kernel}

    results = db.query(sql_query, sql_params)
    if not results:
        sql_query_insert = 'INSERT INTO kernels (name) VALUES (%(kernel_name)s);'
        db.query(sql_query_insert, sql_params)
        results = db.query(sql_query, sql_params)

    return results[0][0]


# Get tool id
def dbGetToolId(db, tool, version):
    sql_query = 'SELECT tool_id FROM tools WHERE name = %(tool_name)s AND version = %(tool_version)s;'
    sql_params = {'tool_name': tool, 'tool_version': version}

    results = db.query(sql_query, sql_params)
    if not results:
        sql_query_insert = 'INSERT INTO tools (name, version) VALUES (%(tool_name)s, %(tool_version)s);'
        db.query(sql_query_insert, sql_params)
        results = db.query(sql_query, sql_params)

    return results[0][0]


# Get experiment id
def dbGetExperimentId(db, name):
    sql_query = 'SELECT exp_id FROM experiments WHERE name = %(exp_name)s;'
    sql_params = {'exp_name': name}

    results = db.query(sql_query, sql_params)
    if not results:
        return None

    return results[0][0]


# Get vendor id
def dbGetVendorId(db, vendor):
    sql_query = 'SELECT vendor_id FROM vendors WHERE name = %(vendor_name)s;'
    sql_params = {'vendor_name': vendor}

    results = db.query(sql_query, sql_params)
    if not results:
        sql_query_insert = 'INSERT INTO vendors (name) VALUES (%(vendor_name)s);'
        db.query(sql_query_insert, sql_params)
        results = db.query(sql_query, sql_params)

    return results[0][0]


# Get virt id
def dbGetVirtId(db, virt):
    if not virt:
        virt = "none"

    sql_query = 'SELECT virt_id FROM virt WHERE name = %(virt_name)s;'
    sql_params = {'virt_name': virt}

    results = db.query(sql_query, sql_params)
    if not results:
        sql_query_insert = 'INSERT INTO virt (name) VALUES (%(virt_name)s);'
        db.query(sql_query_insert, sql_params)
        results = db.query(sql_query, sql_params)

    return results[0][0]


# Get environment id
def dbGetEnvironmentId(db, arch, family, model, stepping, idKernel, idVendor, idVirt):
    if family:
        familyStr = 'family = %(env_family)s and '
    else:
        familyStr = ''
    sql_query = 'SELECT env_id FROM environments WHERE arch = %(env_arch)s and ' + familyStr + 'model = %(env_model)s and stepping = %(env_stepping)s and kernel_id = %(kernel_id)s and vendor_id = %(vendor_id)s and virt_id = %(virt_id)s;'
    sql_params = {'env_arch': arch, 'env_family': family, 'env_model': model, 'env_stepping': stepping,
                  'kernel_id': idKernel, 'vendor_id': idVendor, 'virt_id': idVirt}

    results = db.query(sql_query, sql_params)
    if not results:
        sql_query_insert = 'INSERT INTO environments (arch, family, model, stepping, kernel_id, vendor_id, virt_id) VALUES (%(env_arch)s, %(env_family)s, %(env_model)s, %(env_stepping)s, %(kernel_id)s, %(vendor_id)s, %(virt_id)s);'
        db.query(sql_query_insert, sql_params)
        results = db.query(sql_query, sql_params)

    return results[0][0]


# Get event id
def dbGetEventId(db, event):
    sql_query = 'SELECT event_id FROM events WHERE name = %(event_name)s;'
    sql_params = {'event_name': event}

    results = db.query(sql_query, sql_params)
    if not results:
        sql_query_insert = 'INSERT INTO events (name) VALUES (%(event_name)s);'
        db.query(sql_query_insert, sql_params)
        results = db.query(sql_query, sql_params)

    return results[0][0]


def prepareRegexpByTool(toolName):
    if toolName == "perf":
        return re.compile(r"""
                        (?P<value>[\d\.]+);[^;]*;
                        (?P<name>[\w\/=,:\-]+);
                        """, re.VERBOSE)

    elif toolName == "oprofile":
        return re.compile(r"""
                     (?P<name>[\w:]+),
                     (?P<value>\d+),
                      """, re.VERBOSE)

    elif toolName == "papi":
        return re.compile(r"""
                     (?P<name>\w+);
                     (?P<value>\d+)
                      """, re.VERBOSE)

    else:
        return None


# Add results to DB
def dbAddResult(db, experimentId, toolId, environmentId, eventId, value):
    sql_query_insert = 'INSERT INTO results (exp_id, tool_id, env_id, event_id, val) VALUES (%(experiment_id)s, %(tool_id)s, %(environment_id)s, %(event_id)s, %(value)s);'
    sql_params = {'experiment_id': experimentId, 'tool_id': toolId, 'environment_id': environmentId,
                  'event_id': eventId, 'value': value}
    db.query(sql_query_insert, sql_params)


#################

#
# main
#

class Main:
    def __init__(self, options):
        self.arch = options.arch
        self.kernel = options.kernel
        self.cpuModel = options.cpuModel
        self.cpuFamily = options.cpuFamily
        self.cpuStepping = options.cpuStepping
        self.vendor = options.vendor
        self.tool = options.tool
        self.virt = options.virt
        self.inputCSV = options.inputCSV
        self.experiment = options.experiment

        # environment
        if self.arch == None and self.kernel == None and self.cpuModel == None and self.cpuFamily == None and self.cpuStepping == None and self.vendor == None:
            self.arch, self.kernel, self.cpuModel, self.cpuFamily, self.cpuStepping, self.vendor = detectEnv()
        elif self.arch and self.kernel and self.cpuModel and self.cpuFamily and self.cpuStepping and self.vendor:
            pass
        else:
            print "Error: The environment must be either specified or not. Nothing in between."
            sys.exit(1)

        if not self.tool:
            print "Error: The tool must be always specified (e.g. --tool=perf-4.5.0)"
            sys.exit(1)

        regParseToolNameVersion = re.compile(r"""
                            (?P<name>\w+)\-
                            (?P<value>\d[\w\.\-\:\+]*)
                            """, re.VERBOSE)

        match = regParseToolNameVersion.match(self.tool)
        if not match:
            print "Error: The tool format is incorrect, we need tool-version (e.g. --tool=perf-4.5.0)"
        self.toolName = match.group("name")
        self.toolVersion = match.group("value")

        if not self.experiment:
            print "Error: The experiment must be always specified (e.g. --experiment=\"linpack1000d\")"
            sys.exit(1)


### FIXME parse args

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--arch", action="store", dest="arch", help="architecture cpu")
optparser.add_option("", "--vendor", action="store", dest="vendor", help="cpu vendor")
optparser.add_option("", "--cpu-model", action="store", dest="cpuModel", help="model cpu")
optparser.add_option("", "--cpu-family", action="store", dest="cpuFamily", help="family cpu")
optparser.add_option("", "--cpu-stepping", action="store", dest="cpuStepping", help="steping cpu")
optparser.add_option("", "--kernel", action="store", dest="kernel", help="kernel")
optparser.add_option("", "--virt", action="store", dest="virt", help="virtual pc")
optparser.add_option("", "--microarch", action="store", dest="microarch", help="microarchitecture cpu")
optparser.add_option("", "--tool", action="store", dest="tool", help="tool (perf)")
optparser.add_option("", "--input", action="store", dest="inputCSV", help="input csv")
optparser.add_option("", "--experiment", action="store", dest="experiment", help="experiment name")

(options, args) = optparser.parse_args()

m = Main(options)

# open DB
db = DBConnection()

# FIXME

# same pro virt, ktery bude mit defaultne hodnotu id = 0

kernelId = dbGetKernelId(db, m.kernel)
toolId = dbGetToolId(db, m.toolName, m.toolVersion)
vendorId = dbGetVendorId(db, m.vendor)
virtId = dbGetVirtId(db, m.virt)
environmentId = dbGetEnvironmentId(db, m.arch, m.cpuFamily, m.cpuModel, m.cpuStepping, kernelId, vendorId, virtId)
experimentId = dbGetExperimentId(db, m.experiment)

if not experimentId:
    print "Error: Unknown experiment %s. You need to define it first (see rcl-add-experiment)." % m.experiment
    sys.exit()

regexp = prepareRegexpByTool(m.toolName)
if not regexp:
    print "Error"

fileName = m.inputCSV

if fileName:
    try:
        f = open(fileName, 'r')
    except IOError:
        print "Error: File %s can not be opened" % fileName
        sys.exit()

else:
    f = sys.stdin

for line in f:
    match = regexp.search(line)
    if match:
        eventId = dbGetEventId(db, match.group("name"))
        value = match.group("value")
        dbAddResult(db, experimentId, toolId, environmentId, eventId, value)

if f != sys.stdin:
    f.close()

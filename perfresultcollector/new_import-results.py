#!/usr/bin/env python

import argparse
import re
import sys
import os

from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--arch", action="store", dest="arch", help="architecture cpu")
parser.add_argument("--vendor", action="store", dest="vendor", help="cpu vendor")
parser.add_argument("--cpu-model", action="store", dest="cpuModel", help="model cpu")
parser.add_argument("--cpu-family", action="store", dest="cpuFamily", help="family cpu")
parser.add_argument("--cpu-stepping", action="store", dest="cpuStepping", help="steping cpu")
parser.add_argument("--kernel", action="store", dest="kernel", help="kernel")
parser.add_argument("--virt", action="store", dest="virt", help="virtual pc")
parser.add_argument("--microarch", action="store", dest="microarch", help="microarchitecture cpu")
parser.add_argument("--tool", action="store", dest="tool", help="tool (perf)")
parser.add_argument("--input", action="store", dest="inputCSV", help="input csv")
parser.add_argument("--experiment", action="store", dest="experiment", help="experiment name")

options = parser.parse_args()

tool_id = Query("tools").getID_or_create("tool_id", name="perf", version="1.1.0")
virt_id = Query("virt").getID_or_create("virt_id", name="kvm")
vendor_id = Query("vendors").getID_or_create("vendor_id", name="IBM")
experiment_id = Query("experiments").getID_or_create("exp_id", name="sleep 0.1")

Query("kernels").inserte(name=["3e010105","3e101017","3e101019"])

kernel_id = Query("kernels").getID_or_create("kernel_id", name="3e51110100")
print kernel_id
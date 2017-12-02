#!/usr/bin/env python

import argparse
from models import Query


def detect(name=""):
    pass

def get_env_details(**kwargs):
    query_environments = Query("environments")
    query_environments.set_select("env_id", "virt.virt_id", "vendors.vendor_id", "kernels.kernel_id")
    query_environments.getID_or_create("kernel_id", name=10000)
    for option in kwargs:
        pass


def get_results_details(**kwargs):
    query_environments = Query("results")
    query_environments.set_select("env_id", "virt.virt_id", "vendors.vendor_id", "kernels.kernel_id")

    for option in kwargs:
        query_environments.filter()

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

kernel_id = Query("kernels").getID_or_create("kernel_id", name="3.10.0-637.el7.ppc64le4")
toolId = Query("tools").getID_or_create("tool_id", name="perf", version="1.1.0")
virtId = Query("virt").getID_or_create("virt_id", name="kvm")
experimentId= Query("experiments").getID_or_create("exp_id", name="sleep 0.1")
environmentId= Query("environments").getID_or_create("env_id", arch="aarch64", family=None, model="1", stepping="0", kernels__kernel_id=10033, vendors__vendor_id=15, virt__virt_id=1)
print environmentId
#!/usr/bin/env python

import argparse
import os
import re
import sys

from logger import Logger
from models import Query


def detectCPU_aarch64():
    inputCSV = "/proc/cpuinfo"

    regParseVariant = re.compile(r"""
                            (?P<name>CPU\svariant)\s*:\s*
                            (?P<value>[\da-fx]+)
                            """, re.VERBOSE)

    regParseRevision = re.compile(r"""
                            (?P<name>CPU\srevision)\s*:\s*
                            (?P<value>\d+)
                            """, re.VERBOSE)

    cpu_model = None  # model is used for variant here
    cpu_family = None  # we would like to use family for "armv7"
    cpu_stepping = None  # stepping is used for revision here
    # FIXME: we would like to detect APM/ARM/Qualcom ..
    vendor = "generic_ARM"

    with open(inputCSV, 'r') as f:
        for line in f:
            match = regParseVariant.match(line)
            if match:
                cpu_model = int(match.group("value"), 0)
            match = regParseRevision.match(line)
            if match:
                cpu_stepping = match.group("value")

            if cpu_model and cpu_stepping:
                break

        f.close()

    return cpu_model, cpu_family, cpu_stepping, vendor


def detectCPU_ppc():
    inputCSV = "/proc/cpuinfo"

    regParseRevision = re.compile(r"""
                            (?P<name>revision)\s*:\s*
                            (?P<value>\d+\.\d+)\s+\(pvr\s+
                            (?P<model>[\da-f]+)\s+
                            (?P<rev>[\da-f]+)\)
                            """, re.VERBOSE)

    # model will serve for model number (003f fo POWER7, etc.)
    cpu_model = None
    cpu_family = None  # family is None here
    cpu_stepping = None  # stepping will serve for revision here
    vendor = "IBM"  # vendor is always IBM for ppc64

    with open(inputCSV, 'r') as f:
        for line in f:
            match = regParseRevision.match(line)
            if match:
                cpu_model = int(match.group("model"), 16)
                cpu_stepping = int(match.group("rev"), 16)

            if cpu_model and cpu_stepping:
                break

        f.close()

    return cpu_model, cpu_family, cpu_stepping, vendor


def detectCPU_x86():
    inputCSV = "/proc/cpuinfo"

    regParse_model = re.compile(r"""
                            (?P<name>model)\s*:\s*
                            (?P<value>\d+)
                            """, re.VERBOSE)

    regParse_family = re.compile(r"""
                            (?P<name>cpu\sfamily)\s*:\s*
                            (?P<value>\d+)
                            """, re.VERBOSE)

    regParse_stepping = re.compile(r"""
                            (?P<name>stepping)\s*:\s*
                            (?P<value>[\da-fx]+)
                            """, re.VERBOSE)

    regParseVendor = re.compile(r"""
                            (?P<name>vendor_id)\s*:\s*
                            (?P<value>\w+)
                            """, re.VERBOSE)
    cpu_model = None
    cpu_family = None
    cpu_stepping = None
    vendor = None

    with open(inputCSV, 'r') as f:
        for line in f:
            match = regParse_model.match(line)
            if match:
                cpu_model = match.group("value")
            match = regParse_family.match(line)
            if match:
                cpu_family = match.group("value")
            match = regParse_stepping.match(line)
            if match:
                cpu_stepping = match.group("value")
            match = regParseVendor.match(line)
            if match:
                vendor = match.group("value")
            if cpu_family and cpu_model and cpu_stepping and vendor:
                break

        f.close()

    return cpu_model, cpu_family, cpu_stepping, vendor


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


parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--arch", action="store",
                    dest="arch", help="architecture cpu")
parser.add_argument("--vendor", action="store",
                    dest="vendor", help="cpu vendor")
parser.add_argument("--cpu-model", action="store",
                    dest="cpu_model", help="model cpu")
parser.add_argument("--cpu-family", action="store",
                    dest="cpu_family", help="family cpu")
parser.add_argument("--cpu-stepping", action="store",
                    dest="cpu_stepping", help="steping cpu")
parser.add_argument("--kernel", action="store", dest="kernel", help="kernel")
parser.add_argument("--virt", action="store", dest="virt", help="virtual pc")
parser.add_argument("--microarch", action="store",
                    dest="microarch", help="microarchitecture cpu")
parser.add_argument("--tool", action="store", dest="tool", help="tool (perf)")
parser.add_argument("--input", action="store",
                    dest="inputCSV", help="input csv")
parser.add_argument("--experiment", action="store",
                    dest="experiment", help="experiment name")

options = parser.parse_args()

# Query("kernels").insert(name=["3e010105", "3e101017", "3e101019"])
# kernel_id = Query("kernels").getID_or_create("kernel_id", name="3e51110100")


if __name__ == "__main__":
    LOGGER = Logger(__name__)
    arch = options.arch
    kernel = options.kernel
    cpu_model = options.cpu_model
    cpu_family = options.cpu_family
    cpu_stepping = options.cpu_stepping
    vendor = options.vendor
    tool = options.tool
    experiment = options.experiment
    inputCSV = options.inputCSV
    virt = options.virt

    if not virt:
        virt = "none"

    if not (arch and kernel and cpu_model and cpu_family and cpu_stepping):
        arch, kernel, cpu_model, cpu_family, cpu_stepping, vendor = detectEnv()

    if arch and kernel and vendor:
        pass
    else:
        LOGGER.warning(
            "Error: The environment must be either specified or not. Nothing in between.")
        sys.exit(1)

    if not tool:
        LOGGER.warning(
            "Error: The tool must be always specified (e.g. --tool=perf-4.5.0)")
        sys.exit(1)

    regParseToolNameVersion = re.compile(r"""
                        (?P<name>\w+)\-
                        (?P<value>\d[\w\.\-\:\+]*)
                        """, re.VERBOSE)

    match = regParseToolNameVersion.match(tool)
    if not match:
        LOGGER.warning(
            "Error: The tool format is incorrect, we need tool-version (e.g. --tool=perf-4.5.0)")
    toolName = match.group("name")
    toolVersion = match.group("value")

    if not experiment:
        LOGGER.warning(
            "Error: The experiment must be always specified (e.g. --experiment=\"linpack1000d\")")
        sys.exit(1)

    regexp = prepareRegexpByTool(toolName)
    if not regexp:
        LOGGER.warning("Error")

        if inputCSV:
            try:
                f = open(inputCSV, 'r')
            except IOError:
                LOGGER.warning("Error: File %s can not be opened" % inputCSV)
                sys.exit()
    else:
        f = sys.stdin
    event_ids = []
    values = []
    experiment_ids = []
    tool_ids = []
    env_ids = []

    tool_id = Query("tools").getID_or_create(
        "tool_id", name=toolName, version=toolVersion)
    virt_id = Query("virt").getID_or_create("virt_id", name=virt)
    vendor_id = Query("vendors").getID_or_create(
        "vendor_id", name=vendor)
    kernel_id = Query("kernels").getID_or_create(
        "kernel_id", name=kernel)
    experiment_id = Query("experiments").getID_or_create(
        "exp_id", name=experiment)
    environment_id = Query("environments").getID_or_create(
        "env_id", arch=arch, family=cpu_family, model=cpu_model, stepping=cpu_stepping)

    for line in f:
        match = regexp.search(line)
        if match:
            event_ids.append(Query("events").getID_or_create(
                "event_id", name=match.group("name")))
            values.append(match.group("value"))

            experiment_ids.append(experiment_id)
            env_ids.append(environment_id)
            tool_ids.append(tool_id)

    Query("results").insert(exp_id=experiment_ids, tool_id=tool_ids,
                            event_id=event_ids, env_id=env_ids, val=values)
    if f != sys.stdin:
        f.close()

#!/usr/bin/env python
import argparse
import logging

from perfresultcollector.formatter import format_output, join_data
from perfresultcollector.models import Query
from perfresultcollector import set_logger_level

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)


parser.add_argument("--tool-name1", action="append")
parser.add_argument("--tool-version1", action="append")
parser.add_argument("--not1", action="store_true", default=False)

parser.add_argument("--tool-name2", action="append")
parser.add_argument("--tool-version2", action="append")
parser.add_argument("--not2", action="store_true", default=False)

parser.add_argument("--cpu-arch", action="append")
parser.add_argument("--cpu-microarch", action="append")

parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--table", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)


options = parser.parse_args()

log = logging.getLogger(__name__)

def compare(**kwargs):
    if options.debug:
        set_logger_level(logging.DEBUG)
    group_by=["experiments.name","events.name"]
    header = ["AVG(results.val)","STDDEV(results.val)","COUNT(results.val)"]

    qr1 = Query("results")
    qr1.set_select(group_by+header)
    negation1 = ""

    qr2 = Query("results")
    qr2.set_select(header)
    negation2 = ""

    if options.not2:
        negation2 = "__not"
    if options.not1:
        negation1 = "__not"
    for key, value in kwargs.items():
        if not value:
            continue
        if key[-1] == "2":
            for value in value:
                if value:
                    qr2.filter(**{key[:-1] + negation2: value})
        else:
            for value in value:
                if value:
                    qr1.filter(**{key + negation1: value})
    qr1.set_group(group_by)
    qr2.set_group(group_by)
    try:
        data=join_data(qr1.execute(),qr2.execute())
    except Exception as e:
        print(e)
    for line in format_output(data,options.csv,group_by+["AVG(A)","STDDEV(A)","N(A)","AVG(B)","STDDEV(B)","N(B)"],options.table):
        print(line)

if __name__ == "__main__":
    compare(
        tools__name=options.tool_name1,
        tools__version=options.tool_version1,
        tools__name2=options.tool_name2,
        tools__version2=options.tool_version2,
        environments__arch=options.cpu_arch,
        environments__microarch=options.cpu_microarch,
        environments__arch2=options.cpu_arch,
        environments__microarch2=options.cpu_microarch)


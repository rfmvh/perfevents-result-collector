#!/usr/bin/env python

import argparse
import copy
import logging

from perfresultcollector import set_logger_level
from perfresultcollector.dbinterface import DBConnection
from perfresultcollector.formatter import format_output

db = DBConnection()

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)

parser.add_argument("--cpu-arch1", action="append")
parser.add_argument("--cpu-microarch1", action="append")
parser.add_argument("--not1", action="store_true")

parser.add_argument("--cpu-arch2", action="append")
parser.add_argument("--cpu-microarch2", action="append")
parser.add_argument("--not2", action="store_true")

parser.add_argument("--experiment1", action="append")
parser.add_argument("--experiment2", action="append")

parser.add_argument("--tool-name", action="append")
parser.add_argument("--tool-version", action="append")

parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--table", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)

options = parser.parse_args()

log = logging.getLogger(__name__)

query = """
 SELECT events.name, AVG(results.val), STDDEV(results.val), COUNT(results.val) FROM results
 INNER JOIN experiments ON results.exp_id=experiments.exp_id
 INNER JOIN tools ON results.tool_id=tools.tool_id
 INNER JOIN environments ON results.env_id=environments.env_id
 INNER JOIN events ON results.event_id=events.event_id
 INNER JOIN virt ON environments.virt_id=virt.virt_id
 INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
 INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id
 {format}
 GROUP BY events.event_id  
"""


def compare(**kwargs):
    IDS = 2
    COLUMNS = 3

    def lookup_line_in_table(line, table):
        for i in range(len(table)):
            if line[0] == table[i][0] and line[1] == table[i][1]:
                return table[i] + line[IDS:]

    if options.debug:
        set_logger_level(logging.DEBUG)

    format1 = "WHERE true"
    format2 = "WHERE true"
    _not1 = " "
    _not2 = " "
    if options.not1:
        _not1 += "!"
    if options.not2:
        _not1 += "!"

    for key, val in kwargs.items():
        if val:
            condition = ".".join(key.split("__")[1:])
            if key.split("__")[0] == "A":
                format1 += " AND " + condition + _not1 + "= '" + val[0] + "'"
            else:
                format2 += " AND " + condition + _not2 + "= '" + val[0] + "'"
    log.debug(query.format(format=format1))
    log.debug(query.format(format=format2))
    out1 = db.query(query.format(format=format1), {})
    out2 = db.query(query.format(format=format2), {})

    main = out2
    out = out1
    resp = []
    switch = False

    if len(out1) > len(out2):
        main = out1
        switch = True
        out = out2
    for line in out:
        line = lookup_line_in_table(line, main)
        if line:
            resp.append(line)
    if switch:
        save_resp = copy.copy(resp)
        for i in range(len(resp)):
            resp[i] = list(resp[i])
            resp[i][IDS:IDS + COLUMNS] = resp[i][-COLUMNS:]
            resp[i][-COLUMNS:] = save_resp[i][IDS:IDS + COLUMNS]

    head = ["events.name", "AVG(A)", "STDDEV(A)", "COUNT(A)", "AVG(B)", "STDDEV(B)", "COUNT(B)"]
    resp = sorted(resp, key=lambda x: x[0])
    for line in format_output(resp, options.csv, head, options.table):
        print(line)


if __name__ == "__main__":
    compare(
        A__tools__name=options.tool_name,
        A__tools__version=options.tool_version,
        B__tools__name=options.tool_name,
        B__tools__version=options.tool_version,
        A__environments__arch=options.cpu_arch1,
        A__environments__microarch=options.cpu_microarch1,
        B__environments__arch=options.cpu_arch2,
        B__environments__microarch=options.cpu_microarch2,
        A__experiments__name=options.experiment1,
        B__experiments__name=options.experiment2
    )

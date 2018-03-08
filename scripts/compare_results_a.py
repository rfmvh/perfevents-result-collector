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

parser.add_argument("--tool-name1", action="append", required=True)
parser.add_argument("--tool-version1", action="append", required=True)
parser.add_argument("--not1", action="store_true", default=False)

parser.add_argument("--tool-name2", action="append", required=True)
parser.add_argument("--tool-version2", action="append", required=True)
parser.add_argument("--not2", action="store_true", default=False)

parser.add_argument("--cpu-arch", action="append")
parser.add_argument("--cpu-microarch", action="append")

parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--table", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)

options = parser.parse_args()

log = logging.getLogger(__name__)

query = """
 SELECT experiments.name,events.name, AVG(results.val), STDDEV(results.val), COUNT(results.val) FROM results
 INNER JOIN experiments ON results.exp_id=experiments.exp_id
 INNER JOIN tools ON results.tool_id=tools.tool_id
 INNER JOIN environments ON results.env_id=environments.env_id
 INNER JOIN events ON results.event_id=events.event_id {format}
 GROUP BY experiments.exp_id, events.event_id  
"""


def compare(**kwargs):
    NAMES = 2
    COLUMNS = 3

    def lookup_line_in_table(line, table):
        for i in range(len(table)):
            if line[0] == table[i][0] and line[1] == table[i][1]:
                return table[i] + line[NAMES:]

    if options.debug:
        set_logger_level(logging.DEBUG)

    _not1 = " "
    _not2 = " "
    if options.not1:
        _not1 += "!"
    if options.not2:
        _not1 += "!"

    format1 = "WHERE true"
    format2 = "WHERE true"
    for key, val in kwargs.items():
        if val:
            condition = ".".join(key.split("__")[1:])
            if key.split("__")[0] == "A":
                format1 += " AND " + condition + _not1+"= '" + val[0] + "'"
            else:
                format2 += " AND " + condition + _not2 +" = '" + val[0] + "'"
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
            resp[i][NAMES:NAMES + COLUMNS] = resp[i][-COLUMNS:]
            resp[i][-COLUMNS:] = save_resp[i][NAMES:NAMES + COLUMNS]

    resp = sorted(resp, key=lambda x: x[0])
    head = ["experiments.name", "events.name", "AVG(A)", "STDDEV(A)", "COUNT(A)", "AVG(B)", "STDDEV(B)", "COUNT(B)"]
    for line in format_output(resp, options.csv, head, options.table):
        print(line)


if __name__ == "__main__":
    compare(
        A__tools__name=options.tool_name1,
        A__tools__version=options.tool_version1,
        B__tools__name=options.tool_name2,
        B__tools__version=options.tool_version2,
        A__environments__arch=options.cpu_arch,
        A__environments__microarch=options.cpu_microarch,
        B__environments__arch=options.cpu_arch,
        B__environments__microarch=options.cpu_microarch)

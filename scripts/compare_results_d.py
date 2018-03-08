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

parser.add_argument("--cpu-arch-A", action="append")
parser.add_argument("--cpu-microarch-A", action="append")
parser.add_argument("--not-A", action="store_true", default=False)

parser.add_argument("--cpu-arch-B", action="append")
parser.add_argument("--cpu-microarch-B", action="append")
parser.add_argument("--not-B", action="store_true", default=False)

parser.add_argument("--tool-name", action="append")
parser.add_argument("--tool-version", action="append")

parser.add_argument("--event-A", action="append")
parser.add_argument("--event-B", action="append")

parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--table", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)

options = parser.parse_args()

log = logging.getLogger(__name__)

query = """
 SELECT experiments.name, AVG(results.val), STDDEV(results.val), COUNT(results.val) FROM results
 INNER JOIN experiments ON results.exp_id=experiments.exp_id
 INNER JOIN tools ON results.tool_id=tools.tool_id
 INNER JOIN environments ON results.env_id=environments.env_id
 INNER JOIN events ON results.event_id=events.event_id
 INNER JOIN virt ON environments.virt_id=virt.virt_id
 INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
 INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id
 {format}
 GROUP BY experiments.exp_id
"""


def compare(**kwargs):
    IDS = 2
    COLUMNS = 3

    def lookup_row_in_table(row, table):
        # This function is going to iterate whole table until it will find same ID and it will return row on which it is.
        for i in range(len(table)):
            if row[0] == table[i][0] and row[1] == table[i][1]:
                return table[i]

    if options.debug:
        set_logger_level(logging.DEBUG)

    _not_A = " "
    _not_B = " "
    if options.not_A:
        _not_A += "!"
    if options.not_B:
        _not_B += "!"

    format1 = "WHERE true"
    format2 = "WHERE true"
    for key, val in kwargs.items():
        if val:
            condition = ".".join(key.split("__")[1:])
            if key.split("__")[0] == "A":
                format1 += " AND " + condition + _not_A + "= '" + val[0] + "'"
            else:
                format2 += " AND " + condition + _not_B + "= '" + val[0] + "'"
    log.debug(query.format(format=format1))
    log.debug(query.format(format=format2))
    result_A = db.query(query.format(format=format1), {})
    result_B = db.query(query.format(format=format2), {})
    # smaller = results with less rows and bigger with more rows
    results_bigger = result_B
    results_smaller = result_A
    resp = []
    switch = False

    if len(result_A) > len(result_B):
        results_bigger = result_A
        switch = True
        results_smaller = result_B
    for row_smaller in results_smaller:
        row_bigger = lookup_row_in_table(row_smaller, results_bigger)
        if row_bigger:
            resp.append(row_bigger + row_smaller[IDS:])
    if switch:
        save_resp = copy.copy(resp)
        for index, row in enumerate(resp):
            row = list(row)
            row[IDS:IDS + COLUMNS] = row[-COLUMNS:]
            row[-COLUMNS:] = save_resp[index][IDS:IDS + COLUMNS]

    resp = sorted(resp, key=lambda x: x[0])
    head = ["experiments.name", "events.name", "AVG(A)", "STDDEV(A)", "COUNT(A)", "AVG(B)", "STDDEV(B)", "COUNT(B)"]
    for line in format_output(resp, options.csv, head, options.table):
        print(line)


if __name__ == "__main__":
    compare(
        A__tools__name=options.tool_name,
        A__tools__version=options.tool_version,
        B__tools__name=options.tool_name,
        B__tools__version=options.tool_version,
        A__environments__arch=options.cpu_arch_A,
        A__environments__microarch=options.cpu_microarch_A,
        B__environments__arch=options.cpu_arch_B,
        B__environments__microarch=options.cpu_microarch_B,
        A__events__name=options.event_A,
        B__events__name=options.event_B
    )

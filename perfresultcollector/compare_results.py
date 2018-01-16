#!/usr/bin/env python

import logging

import argparse
from formatter import compare_data_fromat

from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)

parser.add_argument("--event", action="append", help="name event")
parser.add_argument("--event-group", action="append")
parser.add_argument("--tool-name", action="append")
parser.add_argument("--tool-version", action="append")
parser.add_argument("--experiment", action="append")
parser.add_argument("--cpu-family", action="append")
parser.add_argument("--cpu-model", action="append")
parser.add_argument("--cpu-vendor", action="append")
parser.add_argument("--cpu-arch", action="append")
parser.add_argument("--cpu-microarch", action="append")
parser.add_argument("--kernel", action="append")
parser.add_argument("--virt", action="append")
parser.add_argument("--not1", action="store_true", default=False)

parser.add_argument("--event2", action="append", help="name event")
parser.add_argument("--event-group2", action="append")
parser.add_argument("--tool-name2", action="append")
parser.add_argument("--tool-version2", action="append")
parser.add_argument("--experiment2", action="append")
parser.add_argument("--cpu-family2", action="append")
parser.add_argument("--cpu-model2", action="append")
parser.add_argument("--cpu-vendor2", action="append")
parser.add_argument("--cpu-arch2", action="append")
parser.add_argument("--cpu-microarch2", action="append")
parser.add_argument("--kernel2", action="append")
parser.add_argument("--virt2", action="append")
parser.add_argument("--not2", action="store_true", default=False)


parser.add_argument("--event-basic", action="store_true", default=False)
parser.add_argument("--event-details", action="store_true", default=False)
parser.add_argument("--tool-details", action="store_true", default=False)
parser.add_argument("--experiment-details", action="store_true", default=False)
parser.add_argument(
    "--env-details",
    action="store",
    help="1 = arch, microarch; 2=arch, microarch, family, model")
parser.add_argument("--kernel-details", action="store_true", default=False)
parser.add_argument("--virt-details", action="store_true", default=False)

parser.add_argument("--avg", action="store_true", default=False)
parser.add_argument("--stddev", action="store_true", default=False)
parser.add_argument("--group", action="store")

parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--table", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)


options = parser.parse_args()


def compare(**kwargs):
    basic_details = {
        "events.evt_num": options.event_details,
        "events.nmask": options.event_details,
        "tools.name": options.tool_details,
        "tools.version": options.tool_details,
        "experiments.name": options.experiment_details,
        "kernels.name": options.kernel_details,
        "events.name": options.event_basic,
        "events.idgroup": options.event_basic,
        "virt.name": options.virt_details}
    details = ["results.val"]
    for index in basic_details:
        if basic_details[index]:
            details.append(index)
    if options.env_details == "1":
        details += ["environments.arch", "environments.microarch"]
    elif options.env_details == "2":
        details += ["environments.arch", "environments.microarch",
                    "environments.family", "environments.model"]

    qr1 = Query("results")
    qr1.set_select(details)
    negation1 = ""

    qr2 = Query("results")
    qr2.set_select(details)
    negation2 = ""

    for key, list_of_values in kwargs.items():
        if not list_of_values:
            continue
        if options.not2:
            negation2 = "__not"
        if options.not1:
            negation1 = "__not"
        if key[-1] == "2":
            for value in list_of_values:
                if value:
                    qr2.filter(**{key[:-1] + negation2: value})
        else:
            for value in list_of_values:
                if value:
                    qr1.filter(**{key + negation1: value})
    details = details[1:]
    if options.group:
        qr1.set_group(details)
        qr2.set_group(details)
    if options.avg:
        qr2.get_avg(details)
        qr1.get_avg(details)
    if options.stddev:
        qr1.get_stddev(details)
        qr2.get_stddev(details)
    qr1.set_details(details)
    qr2.set_details(details)
    data1 = qr1.execute(options.avg or options.stddev)
    data2 = qr2.execute(options.avg or options.stddev)

    for line in compare_data_fromat(data1, data2):
        print line


if __name__ == "__main__":
    compare(
        events__name=options.event,
        events__idgroup=options.event_group,
        tools__name=options.tool_name,
        tools__version=options.tool_version,
        experiments__name=options.experiment,
        environments__family=options.cpu_family,
        environments__model=options.cpu_model,
        vendors__name=options.cpu_vendor,
        environments__arch=options.cpu_arch,
        environments__microarch=options.cpu_microarch,
        kernels__name=options.kernel,
        virt__name=options.virt,

        events__name2=options.event2,
        events__idgroup2=options.event_group2,
        tools__name2=options.tool_name2,
        tools__version2=options.tool_version2,
        experiments__name2=options.experiment2,
        environments__family2=options.cpu_family2,
        environments__model2=options.cpu_model2,
        vendors__name2=options.cpu_vendor2,
        environments__arch2=options.cpu_arch2,
        environments__microarch2=options.cpu_microarch2,
        kernels__name2=options.kernel2, virt__name2=options.virt2)

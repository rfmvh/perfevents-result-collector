#!/usr/bin/env python

from dbinterface import DBConnection

# TODO diff soubor pro... mail 2.1
# open DB
db = DBConnection()


class Query(object):
    def __init__(self, _from=""):
        self._select = "*"
        self.connection = ""
        self._from = _from
        self.sql_query_event = ""
        self._where = "WHERE True"
        self._conditions = ""
        self.sql_parms_event = {}

    def set_from(self, _from):
        self._from = _from

    def get_inner(self):
        if self._from == "results":
            inner = """
              INNER JOIN experiments ON results.exp_id=experiments.exp_id
              INNER JOIN tools ON results.tool_id=tools.tool_id
              INNER JOIN environments ON results.env_id=environments.env_id
              INNER JOIN events ON results.event_id=events.event_id
              INNER JOIN virt ON environments.virt_id=virt.virt_id
              INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
              INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id
              """
        elif self._from == "environments":
            inner = """
              INNER JOIN virt ON environments.virt_id=virt.virt_id
              INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
              INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id"""
        else:
            inner = ""
        return inner

    def set_select(self, *select):
        self._select = ""
        if  type(select[0]) is list:
            select = select[0]
        if len(select) == 0 or select[0] == "":
            self._select += "*"
        for index, item in enumerate(select):
            self._select += item
            if index != len(select) - 1:
                self._select += ", "

    def filter(self, option=None, **kwargs):
        if option is None:
            option = {}

        if kwargs != {}:
            _where = kwargs
        else:
            _where = option
        for index, item in enumerate(_where):
            s_item = item.split("__")
            operator = "="
            fk = ""
            negation = ""
            if len(s_item) > 1:
                for it in s_item:
                    if it == "gt":
                        operator = ">="
                    elif it == "lt":
                        operator = "<="
                    if it not in ["gt", "lt", "not"]:
                        fk = "." + it
                    if it == "not":
                        negation = "NOT "

            self._where += " and "
            self._where += "" + negation + s_item[0] + fk + " " + operator + " %(my_" + s_item[0] + str(index) + ")s"
            self.sql_parms_event["my_" + s_item[0] + str(index)] = _where[item]

    def debug(self):
        for res in self.execute():
            print res
        print self._query

    def execute(self, operation="", column="*"):
        if operation:
            self._query = "SELECT {0} ( {1} ) FROM {table} {join} {where}".format(operation,column,
                                                                                               table=self._from,
                                                                                               join=self.get_inner(),
                                                                                               where=self._where)

        else:
            self._query = "SELECT {columns} FROM {table} {join} {where}".format(columns=self._select, table=self._from,
                                                                                join=self.get_inner(),
                                                                                where=self._where)

        results = db.select(self._query, self.sql_parms_event)
        return results

    def get_min(self, column):
        return self.execute("min", column)

    def get_avg(self, column):
        return self.execute("avg", column)

    def get_max(self, column):
        return self.execute("max", column)

    def get_stddev(self, column):
        return self.execute("stddev", column)

    def get_select(self):
        return self._select

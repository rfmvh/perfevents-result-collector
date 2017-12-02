#!/usr/bin/env python

from dbinterface import DBConnection

# TODO diff soubor pro... mail 2.1
# open DB
db = DBConnection()


class Query(object):
    def __init__(self, _from=""):
        self._select = "*"
        self.connection = ""
        self.counter = 0
        self._from = _from
        self.sql_query_event = ""
        self._where = "WHERE True"
        self._conditions = ""
        self.sql_parms_event = {}
        self.last_filter_name = ""

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
        if type(select[0]) is list:
            select = select[0]
        if len(select) == 0 or select[0] == "":
            self._select += "*"
        for index, item in enumerate(select):
            self._select += item
            if index != len(select) - 1:
                self._select += ", "

    def filter(self, **kwargs):
        for index, item in enumerate(kwargs):
            split_item = item.split("__")
            operator = "="
            fk = ""
            negation = ""
            if len(split_item) > 1:
                for it in split_item:
                    if it == "gt":
                        operator = ">="
                    elif it == "lt":
                        operator = "<="
                    if it not in ["gt", "lt", "not"]:
                        fk = "." + it
                    if it == "not":
                        negation = "NOT "

            self.counter += 1
            if self.last_filter_name == item:
                self._where += " or "
            else:
                self.last_filter_name = item
                self._where += " and "

            self._where += "" + negation + split_item[0] + fk + " " + operator + " %(my_" + split_item[0] + str(
                self.counter) + ")s"
            self.sql_parms_event["my_" + split_item[0] + str(self.counter)] = kwargs[item]

    def execute(self, operation="", column="*", debug=False):

        if operation:
            self._query = "SELECT {0} ( {1} ) FROM {table} {join} {where}".format(operation, column,
                                                                                  table=self._from,
                                                                                  join=self.get_inner(),
                                                                                  where=self._where)
        else:
            self._query = "SELECT {columns} FROM {table} {join} {where}".format(columns=self._select, table=self._from,
                                                                                join=self.get_inner(),
                                                                                where=self._where)
        if debug:
            return self._query
        else:
            results = db.query(self._query, self.sql_parms_event)
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

    def inserte(self,column, **kwargs):
        columns="("
        values="("
        for index, item in enumerate(kwargs):
            columns += item
            values += "%("+item+")s"
            if not index==len(kwargs)-1:
                columns +=", "
                values+=", "
        columns+=")"
        values+=")"
        sql_query_insert='INSERT INTO '+column+" "+columns+" VALUES "+values
        db.query(sql_query_insert, kwargs)
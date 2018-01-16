from dbinterface import DBConnection
from perfresultcollector import set_logger_level

import logging

# TODO diff soubor pro... mail 2.1
# open DB
db = DBConnection()

log = logging.getLogger(__name__)


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
        self.group = ""
        self.details = ""
        self.clmn_operation = []

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
        if isinstance(select[0], list):
            select = select[0]
        if len(select) == 0 or select[0] == "":
            self._select += "*"
        for index, item in enumerate(select):
            self._select += item
            if index != len(select) - 1:
                self._select += ", "

    def getID_or_create(self, column, **kwargs):
        # returns ID
        self._select = column
        self.filter(**kwargs)
        results = self.execute()
        if not results:
            if self._from == "experiments":
                return None
            self.insert_one(**kwargs)
            results = self.execute()

        return results[0][0]

    def filter(self, **kwargs):
        for index, item in enumerate(kwargs):
            split_item = item.split("__")
            if kwargs[item] is None:
                operator = "IS"
            else:
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

            self._where += "" + negation + \
                split_item[0] + fk + " " + operator + " %(my_" + split_item[0] + str(self.counter) + ")s"
            self.sql_parms_event["my_" + split_item[0] +
                                 str(self.counter)] = kwargs[item]

    def execute(self, operation=False, column="results.val", debug=False):
        if operation:
            self._query = "SELECT {column_operation} {details} FROM {table} {join} {where} {group}" .format(
                column_operation=",".join(self.clmn_operation),
                group=self.group,
                table=self._from,
                join=self.get_inner(),
                where=self._where,
                details=self.details)
        else:
            self._query = "SELECT {columns} FROM {table} {join} {where} {group}".format(
                columns=self._select,
                group=self.group,
                table=self._from,
                join=self.get_inner(),
                where=self._where)

        print self._query
        if debug:
            return self._query
        else:
            results = db.query(self._query, self.sql_parms_event)
            return results

    def set_group(self, group):
        if group:
            self.group = "GROUP BY " + ",".join(group)

    def get_min(self, details, column="results.val"):
        self.set_group(details)
        self.clmn_operation.append("MIN(" + column + ")")

    def get_avg(self, details, column="results.val"):
        self.set_group(details)
        self.clmn_operation.append("AVG(" + column + ")")

    def set_details(self, details):
        if details:
            self.details = "," + ",".join(details)

    def get_max(self, details, column="results.val"):
        self.set_group(details)
        self.clmn_operation.append("MAX(" + column + ")")

    def get_stddev(self, details, column="results.val"):
        self.set_group(details)
        self.clmn_operation.append("STDDEV(" + column + ")")

    def get_select(self):
        return self._select

    def insert_one(self, table="", **kwargs):
        # when you want to insert only one line
        for name, item in kwargs.items():
            kwargs[name] = [item]
        self.insert(table, **kwargs)

    def insert(self, table="", **kwargs):
        # kwargs contains name of columns which you want to import and value
        # and if you want import multiple values you can put array
        if table == "":
            table = self._from
        kwargs_values = {}
        values = ""

        if isinstance(kwargs.values()[0], list):
            val = kwargs.values()[0]
        else:
            val = [kwargs.values()]
        for index in range(len(val)):
            x = kwargs.keys()
            values += "(" + ','.join(map(lambda x: " %(" +
                                         str(x) + str(index) + ")s", x)) + ")"
            if index < len(val) - 1:
                values += ","
            for key, value in kwargs.items():
                kwargs_values[str(key) + str(index)] = value[index]
        values += ""
        columns = "(" + ", ".join(kwargs.keys()) + ")"
        sql_query_insert = 'INSERT INTO ' + table + " " + columns + " VALUES " + values
        db.query(sql_query_insert, kwargs_values, fetchall=False)

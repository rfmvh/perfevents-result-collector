#!/usr/bin/env python

from dbinterface import DBConnection

# TODO vse krom... DONE
# TODO stddev(standartni odchylka), avg, min, max - postgresql funkce DONE
# TODO diff soubor pro... mail 2.1
# open DB
db = DBConnection()


class Query:
    def __init__(self, _from=""):
        self._select = "*"
        self.connection = ""
        self._from = _from
        self._inner = ""
        self.sql_query_event = ""
        self._where = "WHERE True"
        self._conditions = ""
        self.sql_parms_event = {}

    def set_from(self, _from):
        self._from = _from

    def forigner_key(self):
        if self._from == "results":
            self._inner = """
              INNER JOIN experiments ON results.exp_id=experiments.exp_id
              INNER JOIN tools ON results.tool_id=tools.tool_id
              INNER JOIN environments ON results.env_id=environments.env_id
              INNER JOIN events ON results.event_id=events.event_id
              INNER JOIN virt ON environments.virt_id=virt.virt_id
              INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
              INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id
              """
        elif self._from == "environments":
            self._inner = """
              INNER JOIN virt ON environments.virt_id=virt.virt_id
              INNER JOIN kernels ON environments.kernel_id=kernels.kernel_id
              INNER JOIN vendors ON environments.vendor_id=vendors.vendor_id"""

    def set_select(self, *select):
        self._select = ""
        if len(select) == 0 or select[0] == "":
            self._select += "*"
        for index, item in enumerate(select):
            self._select += item
            if index != len(select) - 1:
                self._select += ", "

    def filter(self, *dic_where, **where):
        if where != {}:
            _where = where
        else:
            _where = dic_where
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
                    if it != "gt" and it != "lt" and it != "not":
                        fk = "." + it
                    if it == "not":
                        negation = "NOT "

            self._where += " and "
            self._where += "" + negation + s_item[0] + fk + " " + operator + " %(my_" + s_item[0] + str(index) + ")s"
            self.sql_parms_event["my_" + s_item[0] + str(index)] = _where[item]

    def execute(self, operation="",column=""):
        self.forigner_key()
        if operation == "":
            self._query = "SELECT " + self._select + " FROM " + self._from + "" + self._inner + " " + self._where
        else:
            self._query = "SELECT " + operation + "(" + column + ")" + " FROM " + self._from + "" + self._inner + " " + self._where
        results = db.select(self._query, self.sql_parms_event)
        return results

    def debug(self):
        for res in self.execute():
            print res
        print self._query

    def save_data_to_excel(self):
        from collections import OrderedDict
        from pyexcel_ods import save_data
        data = OrderedDict()
        arra = []
        for resp in self.execute():
            help = []
            for i in resp:
                if i != None:
                    help.append(i)
                else:
                    help.append("None")
            arra.append(help)
        data.update({"Sheet 1": arra})
        save_data("data.ods", data)

    def get_min(self,column):
        return self.execute("min")

    def get_avg(self,column):
        return self.execute("avg")

    def get_max(self,column):
        return self.execute("max")

    def get_stddev(self,column):
        return self.execute("stddev")

    def get_select(self):
        return self._select
def type_of_log(data, csv, head, table=False):
    if not table:
        ret = []
        _head = "#"
        if csv:
            clmn=";"
        else:
            clmn=" "
        for index, hl in enumerate(head):
            if index + 1 != len(head):
                _head += hl + ";"
            else:
                _head += hl
        ret.append(_head)
        for line in data:
            _data = ""
            for index in range(1,len(line)):
                if index + 1 != len(line):
                    _data += str(line[index]) + clmn
                else:
                    _data += str(line[index])
            ret.append(_data)
        return ret
    else:
        ret = [head]
        for line in data:
            _data = []
            for index in range(1,len(line)):
                _data.append(str(line[index]))
            ret.append(_data)
        return ret
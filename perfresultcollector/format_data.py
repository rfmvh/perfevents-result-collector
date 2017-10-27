def type_of_log(data, csv, head, table=False):
    if table:
        ret = [head]
        for line in data:
            _data = []
            for index in range(len(line)):
                _data.append(str(line[index]))
            ret.append(_data)
        return ret
    else:
        _head = "#"
        if csv:
            clmn = ";"
        else:
            clmn = " "
        for index, hl in enumerate(head):
            _head += hl + ";"
        ret = [_head[:-1]]

        for line in data:
            _data = ""
            for index in range(len(line)):
                _data += str(line[index]) + clmn
            _data = _data[:-1]
            ret.append(_data)
        return ret

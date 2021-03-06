def format_output(data, csv, head, table=False):
    if table:
        response = []
        main = [head]
        for line in data:
            _data = []
            for index in line:
                _data.append(str(index))
            main.append(_data)

        widths = [max(map(len, column))  for column in zip(*main) ]
        for row in main:
            response.append(" | ".join((val.ljust(width) for val, width in zip(row, widths))))
        return response

    else:
        _head = "#"
        if csv:
            clmn = ";"
        else:
            clmn = " "
        for index, hl in enumerate(head):
            _head += hl + ";"
        main = [_head[:-1]]

        for line in data:
            _data = ""
            for index in range(len(line)):
                _data += str(line[index]) + clmn
            _data = _data[:-1]
            main.append(_data)
        return main
def join_data(data1, data2):
    response = []
    for line, line2 in zip(data1,data2):
        response.append(line+line2)
    return response

def type_of_log(data, type, head):
    ret = []
    if type:
        hlavicka = "#"
        clmn=";"
    else:
        hlavicka = ""
        clmn=" "
    for index, hl in enumerate(head):
        if index + 1 != len(head):
            hlavicka += hl + clmn
        else:
            hlavicka += hl
    ret.append(hlavicka)
    for line in data:
        _data = ""
        for index in range(len(line)):
            if index + 1 != len(line):
                _data += str(line[index]) + clmn
            else:
                _data += str(line[index])
        ret.append(_data)
    return ret

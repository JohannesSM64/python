def flatten(lst):
    out = []
    for i in lst:
        if isinstance(i, list):
            out.extend(flatten(i))
        else:
            out.append(i)
    return out

def exert(elms, lst, pos):
    for i in elms:
        lst.insert(pos, i)
        pos += 1

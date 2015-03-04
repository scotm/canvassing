__author__ = 'scotm'


def consume_int(x):
    sum_total = 0
    for i in x:
        if i.isdigit():
            sum_total = sum_total*10 + int(i)
        else:
            break
    return sum_total


def domecile_cmp(x,y):
    if x.address_4 != y.address_4:
        return cmp(x.address_4, y.address_4)
    a, b = consume_int(x.address_2),consume_int(y.address_2)
    if a == b:
        c = cmp(x.address_2, y.address_2)
        if c == 0:
            return cmp(x.address_1, y.address_1)
        return c
    return cmp(a, b)
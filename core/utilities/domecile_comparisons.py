from functools import cmp_to_key

__author__ = 'scotm'


def consume_int(x):
    sum_total = 0
    for i in x:
        if i.isdigit():
            sum_total = sum_total * 10 + int(i)
        else:
            break
    return sum_total

# Its intention is to turn a postcode into a readable summary.
# Instead of a list of addresses - we get:
# postcode: 'DD2 3AG'
# return '28-48 (Evens) Whorterbank, Dundee, DD2 3AG'
def domecile_list_to_string(domecile_list):
    domecile_list = sorted(domecile_list, key=domecile_key)
    number_types = ''
    domecile_indices = [consume_int(x.address_2) for x in domecile_list]
    comparisons = [x % 2 for x in domecile_indices]
    if all([x == 1 for x in comparisons]):
        number_types = '(Odds)'
    elif all([x == 0 for x in comparisons]):
        number_types = '(Evens)'

    first_index = 0
    for i, domecile in enumerate(domecile_list):
        if consume_int(domecile.address_2) > 0:
            first_index = i
            break

    first_domecile = domecile_list[first_index]
    residue = ", ".join(y for y in [first_domecile.address_4, first_domecile.address_5, first_domecile.address_6,
                                    first_domecile.postcode] if y)
    return " ".join(
        x for x in [str(consume_int(first_domecile.address_2)) + "-" + str(consume_int(domecile_list[-1].address_2)),
                    number_types, residue,] if x), len(domecile_list)


def domecile_key(domecile):
    data = [getattr(domecile, x) for x in
            ["address_1", "address_2", "address_3", "address_4", "address_5", "address_6", "address_7", "address_8",
             "address_9"] if getattr(domecile, x)]
    secondkey = " ".join(data)
    for i in reversed(data):
        number = consume_int(i)
        if number:
            return number, secondkey
    return 0, secondkey
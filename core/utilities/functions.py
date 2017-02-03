from __future__ import print_function
__author__ = 'scotm'


def split_dict(my_dict, my_list):
    return {x: my_dict[x] for x in my_list}


def transform_dict(my_dict, rename_dict):
    renamed_dict = {}
    for x, y in my_dict.items():
        if x in rename_dict:
            try:
                renamed_dict[rename_dict[x]] = y.strip()
            except:
                print(rename_dict[x], x, y)
                raise
    return renamed_dict


def cast_as_int(x):
    try:
        return int(x)
    except ValueError:
        return x

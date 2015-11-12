__author__ = 'scotm'


def split_dict(my_dict, my_list):
    return {x: my_dict[x] for x in my_list}


def transform_dict(my_dict, rename_dict):
    renamed_dict = {rename_dict[x]: y.strip() for x, y in my_dict.items() if x in rename_dict}
    return renamed_dict
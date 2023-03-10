def tuple_to_str(tp):
    return '$'.join([str(i) for i in tp])

def str_to_tuple(s):
    return tuple([int(i) for i in s.split('$')])
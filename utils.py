def length(c):
    return c.__len__()

def in_range(c, min, max):
    return min <= c <= max

def len_in_range(c, min, max):
    return min <= c.__len__() <= max
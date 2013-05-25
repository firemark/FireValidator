def length(c):
    return c.__len__()

#Why Python? I cannot to override and and or method :(
#bxxx - boolean xxx
def band(a, b):
    return a.__eval_str_arg__("({0} and {1})", b)

def bor(a, b):
    return b.__eval_str_arg__("({0} or {1})", b)

def in_range(c, min, max):
    return band(min <= c, c <= max)

def len_in_range(c, min, max):
    cc = length(c)
    return band(min <= cc, cc <= max)
import types

__all__ = ['C', 'Validator', 'ValidationError']

class Condition(object):

    """Magic. Don't touch"""

    __ps = None
    __globals = {}

    def __init__(self, parse_string="x", __globals=None):
        self.__ps = parse_string
        self.__globals = __globals or {}

    def __eval_str_arg(self, string, *objs):
        globs = self.__globals.copy()
        size = len(globs)
        names = []
        for i, obj in enumerate(objs):
            name = "_%d" % (size + i)
            globs[name] = obj
            names.append(name)

        return self.__class__(string.format(self.__ps, *names), globs)

    def __lt__(self, obj):
        return self.__eval_str_arg("({0} < {1})", obj)

    def __le__(self, obj):
        return self.__eval_str_arg("({0} <= {1})", obj)

    def __gt__(self, obj):
        return self.__eval_str_arg("({0} > {1})", obj)

    def __ge__(self, obj):
        return self.__eval_str_arg("({0} >= {1})", obj)

    def __eq__(self, obj):
        return self.__eval_str_arg("({0} == {1})", obj)

    def __ne__(self, obj):
        return self.__eval_str_arg("({0} != {1})", obj)

    def __or__(self, obj):
        return self.__eval_str_arg("({0} or {1})", obj)

    def __ror__(self, obj):
        return self.__eval_str_arg("({1} or {0})", obj)

    def __and__(self, obj):
        return self.__eval_str_arg("({0} and {1})", obj)

    def __add__(self, obj):
        return self.__eval_str_arg("({0} + {1})", obj)

    def __radd__(self, obj):
        return self.__eval_str_arg("({1} + {0})", obj)

    def __sub__(self, obj):
        return self.__eval_str_arg("({0} - {1})", obj)

    def __rsub__(self, obj):
        return self.__eval_str_arg("({1} - {0})", obj)

    def __mul__(self, obj):
        return self.__eval_str_arg("({0} * {1})", obj)

    def __rmul__(self, obj):
        return self.__eval_str_arg("({1} * {0})", obj)

    def __pow__(self, obj):
        return self.__eval_str_arg("({0} ** {1})", obj)

    def __rpow__(self, obj):
        return self.__eval_str_arg("({1} ** {0})", obj)

    def __nonzero__(self):
        return self.__eval_str_arg("bool({0})")

    def __contains__(self, obj):
        return self.__eval_str_arg("({1} in {0})", obj)

    def __mod__(self, obj):
        return self.__eval_str_arg("({0} % {1})", obj)

    def __rmod__(self, obj):
        return self.__eval_str_arg("({1} % {0})", obj)

    def __getattr__(self, name):
        return self.__class__("%s.%s" % (self.__ps, name), self.__globals.copy())

    def __getitem__(self, key):
        return self.__eval_str_arg("{0}[{1}]", key)

    def __getslice__(self, i=None, j=None):
        return self.__class__("%s[%s:%s]" % (self.__ps, i or "", j or ""),
                              self.__globals)

    def __call__(self, *args, **kwargs):
        if args:
            if kwargs:
                return self.__eval_str_arg("{0}(*{1},**{2})", args, kwargs)
            else:
                return self.__eval_str_arg("{0}(*{1})", args)
        elif kwargs:
            return self.__eval_str_arg("{0}(**{2})", kwargs)
        else:
            return self.__eval_str_arg("{0}()")

    def __hash__(self):
        return id(self)

    def __compile__(self):
        """compile eval string and return lambda to execute"""
        globs = self.__globals.copy()
        comp = compile(self.__ps, "", "eval")
        return lambda obj: bool(eval(comp, globs, {"x": obj}))
                                     

class Validator(object):

    def __init__(self, cast_to, conditions):
        self.cast_to = cast_to
        if isinstance(conditions, dict):
            conditions = conditions.items()
        self.conditions = [(con.__compile__() if isinstance(con, Condition) else con, msg)
                           for con, msg in conditions]

    def validate(self, obj):
        casted = self.cast_to(obj)

        for condition, message in self.conditions:
            if not condition(casted):
                raise ValidationError(message)

        return casted


class ValidationError(Exception):

    def __init__(self, msg):
        self.message = msg
        Exception.__init__(self, msg)

C = Condition()
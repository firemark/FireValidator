import types

__all__ = ['C', 'Validator', 'ValidationError']


class Condition(object):

    """Magic. Don't touch"""

    def __init__(self, parse_string="x", __globs__=None):
        self.__ps__ = parse_string
        self.__globs__ = __globs__ or {}

    def __eval_str_arg__(self, string, *objs):
        globs = self.__globs__.copy()
        size = len(globs)
        names = []
        for i, obj in enumerate(objs):
            if isinstance(obj, Condition):
                names.append(obj.__ps__)
                globs.update(obj.__globs__)
            else:
                name = "_%d" % id(obj)
                globs[name] = obj
                names.append(name)

        return self.__class__(string.format(self.__ps__, *names), globs)

    def __lt__(self, obj):
        return self.__eval_str_arg__("({0} < {1})", obj)

    def __le__(self, obj):
        return self.__eval_str_arg__("({0} <= {1})", obj)

    def __gt__(self, obj):
        return self.__eval_str_arg__("({0} > {1})", obj)

    def __ge__(self, obj):
        return self.__eval_str_arg__("({0} >= {1})", obj)

    def __eq__(self, obj):
        return self.__eval_str_arg__("({0} == {1})", obj)

    def __ne__(self, obj):
        return self.__eval_str_arg__("({0} != {1})", obj)

    def __or__(self, obj):
        return self.__eval_str_arg__("({0} | {1})", obj)

    def __ror__(self, obj):
        return self.__eval_str_arg__("({1} | {0})", obj)

    def __and__(self, obj):
        return self.__eval_str_arg__("({0} & {1})", obj)

    def __rand__(self, obj):
        return self.__eval_str_arg__("({1} & {0})", obj)

    def __add__(self, obj):
        return self.__eval_str_arg__("({0} + {1})", obj)

    def __radd__(self, obj):
        return self.__eval_str_arg__("({1} + {0})", obj)

    def __sub__(self, obj):
        return self.__eval_str_arg__("({0} - {1})", obj)

    def __rsub__(self, obj):
        return self.__eval_str_arg__("({1} - {0})", obj)

    def __mul__(self, obj):
        return self.__eval_str_arg__("({0} * {1})", obj)

    def __rmul__(self, obj):
        return self.__eval_str_arg__("({1} * {0})", obj)

    def __pow__(self, obj, pow=None):
        return (
            self.__eval_str_arg__("({0} ** {1} % {2})", obj, pow) if pow
            else self.__eval_str_arg__("({0} ** {1})", obj)
        )

    def __rpow__(self, obj):
        return self.__eval_str_arg__("({1} ** {0})", obj)

    def __mod__(self, obj):
        return self.__eval_str_arg__("({0} % {1})", obj)

    def __rmod__(self, obj):
        return self.__eval_str_arg__("({1} % {0})", obj)

    def __getattr__(self, name):
        return self.__class__("%s.%s" % (self.__ps__, name), self.__globs__.copy())

    def __getitem__(self, key):
        return self.__eval_str_arg__("{0}[{1}]", key)

    def __call__(self, *args, **kwargs):
        if args:
            if kwargs:
                return self.__eval_str_arg__("{0}(*{1},**{2})", args, kwargs)
            else:
                return self.__eval_str_arg__("{0}(*{1})", args)
        elif kwargs:
            return self.__eval_str_arg__("{0}(**{2})", kwargs)
        else:
            return self.__eval_str_arg__("{0}()")

    def __hash__(self):
        return id(self)

    def __compile__(self):
        """compile eval string and return lambda to execute"""
        globs = self.__globs__.copy()
        comp = compile(self.__ps__, "", "eval")
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

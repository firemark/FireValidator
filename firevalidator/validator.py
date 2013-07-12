import types

__all__ = ['C', 'Validator', 'ValidationError', 'Con']


class Condition(object):

    """Magic. Don't touch"""

    def __init__(self, parse_string="x", __globs__=None):
        self.__ps__ = parse_string
        self.__globs__ = __globs__ or {}

    def __eval_str_arg__(self, string, *objs):
        """
        >>> C.__eval_str_arg__('test').__ps__
        'test'
        >>> C.__eval_str_arg__('{0} + 5').__ps__
        'x + 5'
        >>> C.__eval_str_arg__('{0} + 5', 5, 4, 3).__ps__
        'x + 5'
        >>> C.__eval_str_arg__('{0}.macarena[50]', 5, 4, 3).__ps__
        'x.macarena[50]'
        >>> str_id = '_%d' % id(' ')
        >>> C.__eval_str_arg__('{1} in {0}', ' ').__globs__[str_id] == ' '
        True
        >>> len(C.__eval_str_arg__('{0} + 5', 5, 4, 3).__globs__)
        3
        >>> len(C.__eval_str_arg__('{0} + 5').__globs__)
        0
        >>> type(C.__eval_str_arg__('{0}')) is type(C)
        True
        """
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
        """
        >>> con = (C < 5).__compile__()
        >>> con(5)
        False
        >>> con(4)
        True
        """
        return self.__eval_str_arg__("({0} < {1})", obj)

    def __le__(self, obj):
        """
        >>> con = (C <= 5).__compile__()
        >>> con(6)
        False
        >>> con(5)
        True
        """
        return self.__eval_str_arg__("({0} <= {1})", obj)

    def __gt__(self, obj):
        """
        >>> con = (C > 5).__compile__()
        >>> con(5)
        False
        >>> con(6)
        True
        """
        return self.__eval_str_arg__("({0} > {1})", obj)

    def __ge__(self, obj):
        """
        >>> con = (C >= 5).__compile__()
        >>> con(5)
        True
        >>> con(4)
        False
        """
        return self.__eval_str_arg__("({0} >= {1})", obj)

    def __eq__(self, obj):
        """
        >>> con = (C == 6).__compile__()
        >>> con(6)
        True
        >>> con(5)
        False
        """
        return self.__eval_str_arg__("({0} == {1})", obj)

    def __ne__(self, obj):
        """
        >>> con = (C != 6).__compile__()
        >>> con(6)
        False
        >>> con(5)
        True
        """
        return self.__eval_str_arg__("({0} != {1})", obj)

    def __or__(self, obj):
        """
        >>> con = (C | 0 == C).__compile__()
        >>> con(5)
        True
        >>> con(3)
        True
        >>> con(1)
        True
        >>> con(0)
        True
        """
        return self.__eval_str_arg__("({0} | {1})", obj)

    def __ror__(self, obj):
        """
        >>> con = (1 | C == 3).__compile__()
        >>> con(2)
        True
        >>> con(1<<1)
        True
        >>> con(3)
        True
        >>> con(4)
        False
        """
        return self.__eval_str_arg__("({1} | {0})", obj)

    def __and__(self, obj):
        """
        >>> con = (C & C == 3).__compile__()
        >>> con(3)
        True
        >>> con(4)
        False
        """
        return self.__eval_str_arg__("({0} & {1})", obj)

    def __rand__(self, obj):
        """
        >>> con = (1 & C == 0).__compile__()
        >>> con(0)
        True
        >>> con(1)
        False
        >>> con(2)
        True
        >>> con(3)
        False
        """
        return self.__eval_str_arg__("({1} & {0})", obj)

    def __add__(self, obj):
        """
        >>> con = (C + 1 == 1).__compile__()
        >>> con(0)
        True
        >>> con(1)
        False
        """
        return self.__eval_str_arg__("({0} + {1})", obj)

    def __radd__(self, obj):
        """
        >>> con = (1 + C == 1).__compile__()
        >>> con(0)
        True
        >>> con(1)
        False
        """
        return self.__eval_str_arg__("({1} + {0})", obj)

    def __sub__(self, obj):
        """
        >>> con = (C - 1 == 0).__compile__()
        >>> con(0)
        False
        >>> con(1)
        True
        """
        return self.__eval_str_arg__("({0} - {1})", obj)

    def __rsub__(self, obj):
        """
        >>> con = (1 - C == 0).__compile__()
        >>> con(0)
        False
        >>> con(1)
        True
        """
        return self.__eval_str_arg__("({1} - {0})", obj)

    def __mul__(self, obj):
        """
        >>> con = (C * 2 != 6).__compile__()
        >>> con(3)
        False
        >>> con(4)
        True
        >>> con = (C * 2 == 'xxxx').__compile__()
        >>> con('xx')
        True
        >>> con('zz')
        False
        >>> con('x')
        False
        """
        return self.__eval_str_arg__("({0} * {1})", obj)

    def __rmul__(self, obj):
        """
        >>> con = (2 * C == 'xxxx').__compile__()
        >>> con('xx')
        True
        >>> con('zz')
        False
        """
        return self.__eval_str_arg__("({1} * {0})", obj)

    def __pow__(self, obj, mod=None):
        """
        >>> con = (C ** 2 == 4).__compile__()
        >>> con(2)
        True
        >>> con(3)
        False
        >>> con = (C ** 3 % 5  == 4).__compile__()
        >>> con(1)
        False
        >>> con(2)
        False
        >>> con(3)
        False
        >>> con(4)
        True
        """
        return (
            self.__eval_str_arg__("({0} ** {1} % {2})", obj, mod) if mod
            else self.__eval_str_arg__("({0} ** {1})", obj)
        )

    def __rpow__(self, obj):
        """
        >>> con = (2 ** C == 8).__compile__()
        >>> con(3)
        True
        >>> con(2)
        False
        """
        return self.__eval_str_arg__("({1} ** {0})", obj)

    def __mod__(self, obj):
        """
        >>> con = (C % 5 == 4).__compile__()
        >>> con(4)
        True
        >>> con(5)
        False
        >>> con(9)
        True
        >>> con = (C % 5 == '_5').__compile__()
        >>> con('_%d')
        True
        >>> con('_%i')
        True
        >>> con('_%s')
        True
        >>> con('x%s')
        False
        """
        return self.__eval_str_arg__("({0} % {1})", obj)

    def __rmod__(self, obj):
        """
        >>> con = ('_%d' % C  == '_4').__compile__()
        Traceback (most recent call last):
        ...
        TypeError: %d format: a number is required, not Condition
        >>> con = (4  % C  == 4).__compile__()
        >>> con(4)
        False
        >>> con(5)
        True
        >>> con(2)
        False
        """
        return self.__eval_str_arg__("({1} % {0})", obj)

    def __getattr__(self, name):
        """
        >>> from datetime import datetime
        >>> con = (C.year == 2010).__compile__()
        >>> con(datetime(year=2010,month=10,day=5))
        True
        >>> con(datetime(year=2012,month=10,day=5))
        False
        """
        return self.__class__("%s.%s" % (self.__ps__, name), self.__globs__.copy())

    def __getitem__(self, key):
        """
        >>> con = (C[1] == '5').__compile__()
        >>> con('456')
        True
        >>> con([4,'5',6])
        True
        >>> con('666')
        False
        >>> con((4,5,6))
        False
        """
        return self.__eval_str_arg__("{0}[{1}]", key)

    def __call__(self, *args, **kwargs):
        """
        >>> con = C.islower().__compile__()
        >>> con('test')
        True
        >>> con('TeSt')
        False
        >>> con('TEST')
        False
        >>> con = (C.format(0, 1,x=2) == "210").__compile__()
        >>> con("{x}{1}{0}")
        True
        >>> con = (C.format(0, 1) == "10").__compile__()
        >>> con("{1}{0}")
        True
        >>> con("{0}{1}")
        False
        >>> con = (C.format(x=5) == "50").__compile__()
        >>> con("{x}0")
        True
        >>> con("{x}1")
        False
        """
        if args:
            if kwargs:
                return self.__eval_str_arg__("{0}(*{1},**{2})", args, kwargs)
            else:
                return self.__eval_str_arg__("{0}(*{1})", args)
        elif kwargs:
            return self.__eval_str_arg__("{0}(**{1})", kwargs)
        else:
            return self.__eval_str_arg__("{0}()")

    def __hash__(self):
        return id(self)

    def __compile__(self):
        """compile eval string and return lambda to execute
        >>> con = C.__compile__()
        >>> con(True)
        True
        >>> con(False)
        False
        """
        globs = self.__globs__.copy()
        comp = compile(self.__ps__, "", "eval")
        return lambda obj: bool(eval(comp, globs, {"x": obj}))


class Validator(object):

    def __init__(self, *objs):
        sobjs = []
        for obj in objs:
            if isinstance(obj, dict):
                sobjs.append([(con.__compile__()
                               if isinstance(con, Condition) else con, msg)
                              for con, msg in obj.items()])
            elif isinstance(obj, tuple):
                sobjs.append([(con.__compile__()
                               if isinstance(con, Condition) else con, msg)
                              for con, msg in obj])
            elif isinstance(obj, types.FunctionType) or isinstance(obj, type):
                sobjs.append(obj)
            else:
                raise ValueError('Invalid object: %s' % obj)

        self.objs = sobjs

    def validate(self, item):
        for obj in self.objs:
            item = Validator.single_validate(obj, item)

        return item

    @staticmethod
    def single_validate(obj, item):
        if isinstance(obj, list):  # list with condictions
            for condition, message in obj:
                if not condition(item):
                    raise ValidationError(message)
        else:  # cast function
            try:
                return obj(item)
            except ValueError as e:
                raise ValidationError(str(e))

        return item


class Con(object):

    """
    Condition object
    >>> con = Con(C == 5, "number is not equal 5")
    >>> con(5)
    >>> con(4)
    Traceback (most recent call last):
    ...
    firevalidator.validator.ValidationError: number is not equal 5
    """

    def __init__(self, con, msg):
        self.con = con.__compile__() if isinstance(con, type(C)) else con
        self.msg = msg

    def __call__(self, item):
        if not self.con(item):
            raise ValidationError(self.msg)


class ValidationError(Exception):

    def __init__(self, msg):
        self.message = msg
        Exception.__init__(self, msg)


C = Condition()

from django.core.exceptions import ValidationError
from .validator import ValidationError as FireValidationError
from .validator import Validator as FireValidator
from .validator import Con as FireCon
from .validator import C
from functools import wraps
import types


class Validator(FireValidator):

    def generate_func(self, obj):
        def func(value):
            if value is not None:
                try:
                    FireValidator.single_validate(obj, value)
                except FireValidationError as e:
                    raise ValidationError(e.message)
        return func

    def __rlshift__(self, x):
        """
        Because django sucks and cannot into normal validators
        Modify clean method.
        """
        more_cleaned = x.clean

        @wraps(more_cleaned)
        def clean(s, value):
            value = more_cleaned(value)
            try:
                return self.validate(value)
            except FireValidationError as e:
                raise ValidationError(e.message)

        x.clean = types.MethodType(clean, x)
        return x


class Con(FireCon):

    def __call__(self, value):
        if value is not None:
            try:
                super(Con, self).__call__(value)
            except FireValidationError as e:
                raise ValidationError(e.message)

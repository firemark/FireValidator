"""
Support FireValidator to WTForms's fields
"""

from wtforms import ValidationError
from .validator import ValidationError as FireValidationError
from .validator import Validator as FireValidator
from .validator import Con as FireCon
from .validator import C
import types


class Validator(FireValidator):

    def __call__(self, form, field):
        if field.data is not None:
            try:
                self.validate(field.data)
            except FireValidationError as e:
                 raise ValidationError(e.message.format(field=field))

    def __iter__(self):
        for obj in self.objs:
            def func(form, field):
                if field.data is not None:
                    try:
                        field.data = FireValidator.single_validate(obj, field.data)
                    except FireValidationError as e:
                         raise ValidationError(e.message.format(field=field))

            yield func


class Con(FireCon):

    def __call__(self, form, field):
        if field.data is not None:
            try:
                super(Con, self).__call__(field.data)
            except FireValidationError as e:
                 raise ValidationError(e.message.format(field=field))

"""
Examples how to use FireValidator
"""

from datetime import datetime
from validator import *
from utils import length



def validate_int():
    int_validator = Validator(int, {
        C >= 5: "Number is too small",
        C != 8: "Number mustn't equal 8",
        C < 10:	"Number is too big",
        lambda x: True: "Number is always ok :-D"
    })

    for i in range(12):
        try:
            int_validator.validate(i)
        except ValidationError as e:
            print("%-20dFAIL: %s" % (i, e.message))
        else:
            print("%-20dOK" % i)


def validate_str():
    str_validator = Validator(str, {
        C.islower(): "String must be lower",
        length(C) >= 4: "String is too short",
        C[-1].upper() == 'T': "Last char must be 'T'"
    })

    for s in "Lorem ipsum dolor sit amet consectetur adipiscing elit".split():
        try:
            str_validator.validate(s)
        except ValidationError as e:
            print("%-20sFAIL: %s" % (s, e.message))
        else:
            print("%-20sOK" % s)


def validate_date():
    date_validator = Validator(lambda s: datetime.strptime(s, "%d-%m-%Y"), (
        (lambda date: date.year <= datetime.now().year,
            "Year mustn't be in the future"),
        (1 + C.day % 2, "Day must be even"),
        (C.month > 5, "Month must be later than May")
    ))

    date_data = [
        # DD-MM-YYYY,
        "12-06-2100",  # Future!
        "05-06-2012",
        "08-12-2013",
        "04-04-2010"
    ]

    for d in date_data:
        try:
            date_validator.validate(d)
        except ValidationError as e:
            print("%-20sFAIL: %s" % (d, e.message))
        else:
            print("%-20sOK" % d)


if __name__ == "__main__":
    print("numbers".center(50, '-'))
    validate_int()
    print("strings".center(50, '-'))
    validate_str()
    print("dates".center(50, '-'))
    validate_date()

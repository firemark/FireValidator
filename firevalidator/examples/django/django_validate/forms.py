from django.forms import IntegerField, Form, CharField, DateField
from firevalidator.utils import striped_str, length, in_range
from firevalidator.django import Validator, C, Con

int_validators = [Con(C % 2 == 0, 'Integer must be even.')]
date_validators = [Con(C > C.today(), 'Date must be in future.')]
name_validators = Validator(striped_str, {
    lambda s: ' ' not in s: 'field cannot contains spaces.',
    length(C) <= 20: 'field is too big.',
    C[0].upper() == C[0]: 'first letter must be big.'
})

zip_validators = Validator(striped_str, {
    length(C) == len('XX-XXX'): 'zip code must be XX-XXX',
    C[0:2].isdigit(): 'First part isn\'t a number.',
    C[2] == '-': 'prefix is not \'-\'.',
    C[3:5].isdigit(): 'Last part isn\'t a number.'
})


class MyForm(Form):
    number = IntegerField(label='Even integer', validators=int_validators)
    date = DateField(label='Date in future [DD-MM-YYYY]',
                     input_formats=['%d-%m-%Y'],
                     validators=date_validators)
    first_name = CharField(label='First name') << name_validators
    last_name = CharField(label='Last name') << name_validators
    zip_code = CharField(label='Zip Code') << zip_validators

from django import forms
from firevalidator.utils import striped_str, length, in_range
from firevalidator.wtform import Validator, C, Con

int_validators = [Con(C % 2 == 0, 'Integer must be even.')]
date_validators = [Con(
    lambda date: date > date.today(), 'Date must be in future.')]

zip_validators = Validator(striped_str, {
    length(C) == len('XX-XXX'): 'zip code must be XX-XXX',
    C[0:2].isdigit(): 'First part isn\'t a number.',
    C[2] == '-': 'prefix is not \'-\'.',
    C[3:5].isdigit(): 'Last part isn\'t a number.'
})


class MyForm(forms.Form):
    number = forms.IntegerField('Even integer', validators=int_validators)
    date = forms.DateField('Date in future [DD-MM-YYYY]',
                           validators=date_validators,
                           format="%d-%m-%Y")
    first_name = TextField('First name',
                           blank=False,
                           null=False,
                           validators=[name_validator])
    last_name = TextField('Last name',
                          blank=False,
                          null=False,
                          validators=[name_validator])
    zip_code = TextField('Zip Code', validators=zip_validators)

from firevalidator.utils import striped_str, length, in_range
from firevalidator.wtform import Validator, C, Con
from collections import defaultdict
from flask import Flask, request
from jinja2 import Template
from datetime import date
from wtforms import Form, DateField, IntegerField, TextField
from wtforms import validators

app = Flask(__name__)
app.debug = True

name_validator = Validator(striped_str, {
    length(C) <= 20: '{field.label} is too big.',
    lambda s: ' ' not in s: '{field.label} cannot contains spaces.'
})


class MyForm(Form):
    number = IntegerField('Even integer',
                          [Con(C % 2 == 0, 'Integer must be even.')])
    date = DateField('Date in future [DD-MM-YYYY]',
                     [Con(lambda date: date > date.today(),
                          'Date must be in future.')],
                     format="%d-%m-%Y")
    first_name = TextField('First name',
                           [validators.required(), name_validator])
    last_name = TextField('Last name', [validators.required(), name_validator])
    zip_code = TextField('Zip Code', Validator(striped_str, {
        length(C) == len('XX-XXX'): 'zip code must be XX-XXX',
        C[0:2].isdigit(): 'First part isn\'t a number.',
        C[2] == '-': 'prefix is not \'-\'.',
        C[3:5].isdigit(): 'Last part isn\'t a number.'
    }))

template = Template("""
<html>
<head>
    <title>Test site</title>
    <style>
        span { background-color: gray;}
        strong { color: red;}
    </style>
</head>
<body>
    <form method='POST' action='/'>
        <table>
        {% for field in form  %}
        <tr>
            <th>{{field.label}}</th>
            <td>{{field()}}</td>
            <td><strong>{% for error in field.errors %} {{error}} {% endfor %}</strong></td>
        </tr>
        {% endfor %}
        </table>
        <input type='submit' />
    </form>
    Valid records:
    <ul>
    {% for key, value in output.items() %}
        <li><b>{{key}} =></b> <span>{{value}}</span></li>
    {% endfor %}
    </ul>
</body>
</html>
""")


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = MyForm(request.form)

    return template.render(
        form=form,
        output=form.data if form.validate() else {}
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)

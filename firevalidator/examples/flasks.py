from firevalidator import *
from firevalidator.utils import striped_str, length, in_range
from collections import defaultdict
from flask import Flask, request
from jinja2 import Template
from datetime import datetime

app = Flask(__name__)
app.debug = True

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
        Even integer in range(0, 10)<input type='text' name='int' value='{{int}}'/><strong>{{err['int']}}</strong><br />
        Date in future [DD-MM-YYYY]<input type='text' name='date' value='{{date}}'/><strong>{{err['date']}}</strong><br />
        First name [Max len:20]<input type='text' name='first_name' value='{{first_name}}'/><strong>{{err['first_name']}}</strong><br />
        Last name [Max len:20]<input type='text' name='last_name' value='{{last_name}}'/><strong>{{err['last_name']}}</strong><br />
        Zip code [XX-XXX]<input type='text' name='zip_code' value='{{zip_code}}' /><strong>{{err['zip_code']}}</strong><br />
        Valid records:
        <ul>
        {% for key, value in output.items() %}
            <li><b>{{key}} =></b> <span>{{value}}</span></li>
        {% endfor %}
        </ul>
        <input type='submit' />
    </form>
</body>
</html>
""")

validators = {
    'int': Validator(int, {
        C % 2 == 0: 'Integer must be even',
        in_range(C, 0, 10): 'Integer must be between 0 and 10'
    }),
    'date': Validator(lambda s: datetime.strptime(s, "%d-%m-%Y"), {
        lambda date: date > datetime.now(): 'Date must be in future'
    }),
    'first_name': Validator(striped_str, {
        length(C) <= 20: 'First name is too big',
        C: 'First name is required',
        lambda s: ' ' not in s: 'First name cannot contains spaces'
    }),
    'last_name': Validator(striped_str, {
        length(C) <= 20: 'Last name is too big',
        C: 'Last name is required',
        lambda s: ' 'not in s: 'Last name cannot contains spaces'
    }),
    'zip_code': Validator(striped_str, {
        length(C) == len('XX-XXX'): 'zip code must be XX-XXX',
        C[0:2].isdigit(): 'First part isn\'t a number',
        C[2] == '-': 'prefix is not \'-\'', 
        C[3:5].isdigit(): 'Last part isn\'t a number'
    })
}


@app.route("/", methods=['GET', 'POST'])
def hello():
    err = defaultdict(str)
    vars = {}
    output = {}
    if request.method == "POST":
        for key, value in request.form.items():
            try:
                output[key] = validators[key].validate(value)
            except ValidationError as e:
                err[key] = e.message

            vars[key] = value

    return template.render(
        err=err,
        output=output,
        **vars
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)

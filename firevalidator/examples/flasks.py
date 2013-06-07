from firevalidator import *
from firevalidator.utils import striped_str, length, in_range
from collections import defaultdict
from flask import Flask, request, url_for
from jinja2 import Template
from datetime import datetime

app = Flask(__name__)
app.debug = True

template = Template("""
<html>
<head>
    <title>Test site</title>
    <link rel="stylesheet" type='text/css' href="static/css.css" />
</head>
<body>
    <form method='POST' action='/' class="form-horizontal">
        <h2>Validator &lt;3</h2>
        <label>Even integer in range(0, 10)</label>
            <input type='text' name='int' value='{{int}}'/>
            <span class="help-inline">{{err['int']}}</span>
        <label>Date in future [DD-MM-YYYY]</label>
            <input type='text' name='date' value='{{date}}'/>
            <span class="help-inline">{{err['date']}}</span>
        <label>First name [Max len:20]</label>
            <input type='text' name='first_name' value='{{first_name}}'/>
            <span class="help-inline">{{err['first_name']}}</span>
        <label>Last name [Max len:20]</label>
            <input type='text' name='last_name' value='{{last_name}}'/>
            <span class="help-inline">{{err['last_name']}}</span>
        <label>Zip code [XX-XXX]</label>
            <input type='text' name='zip_code' value='{{zip_code}}' />
            <span class="help-inline">{{err['zip_code']}}</span>
        <div>    
            <strong>Valid records:</strong>
            <ul>
            {% for key, value in output.items() %}
                <li><b>{{key}} =></b> <span>{{value}}</span></li>
            {% endfor %}
            </ul>
        </div>
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


@app.route("/", methods=['GET'])
def get():
    return template.render(
        err=defaultdict(str),
        output={}
    )

@app.route("/", methods=['POST'])
def post():
    err = defaultdict(str)
    vars = {}
    output = {}

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

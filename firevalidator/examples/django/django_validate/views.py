from django.shortcuts import render_to_response
from .forms import MyForm


def validate(request):
    # View code here...
    return render_to_response("validate.html")
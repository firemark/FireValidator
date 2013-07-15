from django.shortcuts import render
from django.views.generic import View
from .forms import MyForm


class ValidateView(View):

    def get(self, request, *args, **kwargs):
        form = MyForm()
        return render(request, 'validate.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MyForm(request.POST)
        form.is_valid() 
        return render(request, 'validate.html', {'form': form})
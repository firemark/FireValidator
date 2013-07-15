from django.conf.urls import patterns, include, url
from .views import ValidateView

urlpatterns = patterns('',
    url(r'^$', ValidateView.as_view(), name='home'),
)

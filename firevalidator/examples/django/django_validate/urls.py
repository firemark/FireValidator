from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'django_validate.views.validate', name='home'),
)

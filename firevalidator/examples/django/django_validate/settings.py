from os import path
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
SITE_ROOT = path.abspath(path.dirname(__name__))
STATIC_URL = '/static/'
STATICFILES_DIRS = (path.join(SITE_ROOT, 'static'),)
SECRET_KEY = 'fkgf_1ea1*g$hz)u(h_f*r6g9e1g^k78*6rf$8^7zo+$&s)22@'
ROOT_URLCONF = 'django_validate.urls'
WSGI_APPLICATION = 'django_validate.wsgi.application'
TEMPLATE_DIRS = ("template/",)
INSTALLED_APPS = ('django.contrib.staticfiles',)
from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-zc&=#&q%odr*i68j-23h51ybzdbuzxy8*=#fy9tr(ubg#z)_p@'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'console_santé_db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

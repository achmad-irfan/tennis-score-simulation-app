from .base import *

DEBUG= True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.3", "0.0.0.0",]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')]

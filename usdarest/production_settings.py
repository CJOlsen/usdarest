# this is a PRODUCTION settings file, this file should not be made public!


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y3m$=rs7$!91*31y*dt%m**ljam66otk4%ilm%d&b+y@lc7zvq'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

import dj_database_url
DATABASES = {'default': dj_database_url.config()}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'usdafood',
#         'USER': 'cj',
#         'PASSWORD': 'headgreenbooktee',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
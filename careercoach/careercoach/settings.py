import os

DEBUG                   = os.environ.get('DEBUG_MODE')

#############################
# project level settings
#############################
BASE_DIR                = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY              = "%@161s%q0w^y!7lvvn&9ni+%svsjy&xd-dw1jrjbe@tvn9jg&s"
ROOT_URLCONF            = "careercoach.urls"
WSGI_APPLICATION        = "careercoach.wsgi.application"
LANGUAGE_CODE           = "en-us"

## Network settings project level
DNS_NAME                = os.environ.get('DNS_NAME')
PROTOCOL 				= os.environ.get('PROTOCOL')
DOMAIN 					= os.environ.get('DOMAIN')

## list of allowed IP address
INTERNAL_IPS 			= ['127.0.0.1',]
ALLOWED_HOSTS           = ['*']
if DEBUG == True:
    ALLOWED_HOSTS = ['*', '0.0.0.0']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# old stuff
# ALLOWED_HOSTS           = ('localhost','127.0.0.1[::1]','127.0.0.1').split(",") #(os.environ.get('DJANGO_ALLOWED_HOSTS')).split(",")

MESSAGE_STORAGE         = 'django.contrib.messages.storage.session.SessionStorage'

# app versions 
APP_VERSION_RW          = os.environ.get('VERSION_RESUMEWEB')
APP_VERSION_SHOPCART    = os.environ.get('VERSION_RESUMEWEB')

## Login redirection
LOGIN_URL               = "/rw/home"
LOGIN_REDIRECT_URL      = "/rw/home"
CACHE_TTL               = 60*60

DEFAULT_AUTO_FIELD      = 'django.db.models.AutoField'
CRISPY_TEMPLATE_PACK    = 'bootstrap4'


from .settings_params import DATABASES
from .settings_params import ELASTICSEARCH_DSL
from .settings_params import PAYPAL_CLIENT_ENV
from .settings_params import STATIC_URL
from .settings_params import STATIC_ROOT
from .settings_params import MEDIA_ROOT
from .settings_params import MEDIA_URL

print("**********SERVER_TYPE ->>{}".format(os.environ.get('SERVER_TYPE')))
print("**********STATIC_URL ->>{}".format(STATIC_URL))
print("**********STATIC_ROOT ->>{}".format(STATIC_ROOT))
print("**********MEDIA_ROOT ->>{}".format(MEDIA_ROOT))
print("**********MEDIA_URL ->>{}".format(MEDIA_URL))
print("**********PAYPAL_CLIENT_ENV ->>>{}".format(PAYPAL_CLIENT_ENV))
print("**********DATABASE ->>>{}".format(DATABASES['default']['NAME']))
print("**********ELASTICSEARCH ->>>{}".format(ELASTICSEARCH_DSL['default']['hosts'][0]))


# Import all settings params
from .settings_params import *

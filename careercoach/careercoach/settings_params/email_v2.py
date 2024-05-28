import os
from django.conf import settings

# Email Config
####################################################
EMAIL_HOST 		                        = os.environ.get("EMAIL_HOST")
EMAIL_PORT 		                        = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS 	                        = os.environ.get("EMAIL_USE_TLS")
DEVELOPMENT_ONLY_EMAIL_RECIPIENTS       = ['def274753@gmail.com', 'django712345@protonmail.com']

if settings.DEBUG:
    EMAIL_CONFIG = {
        "AUTH": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_AUTH"),
                'EMAIL_HOST_PASSWORD' 	: os.environ.get("EMAIL_HOST_PASSWORD_AUTH")
        },
        "SHOPCART": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_SHOPCART"),
                'EMAIL_HOST_PASSWORD' 	: os.environ.get("EMAIL_HOST_PASSWORD_SHOPCART")
        },
        "PRODSERV": {
                'EMAIL_HOST_USER'               : os.environ.get("EMAIL_HOST_USER_PRODSERV"),
                'EMAIL_HOST_PASSWORD'           : os.environ.get("EMAIL_HOST_PASSWORD_PRODSERV")
        },        
        "CUSTSUPP": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_CUSTSUPP"),
                'EMAIL_HOST_PASSWORD' 	        : os.environ.get("EMAIL_HOST_PASSWORD_CUSTSUPP")
        },
        "GENERAL": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_CUSTSUPP"),
                'EMAIL_HOST_PASSWORD' 	        : os.environ.get("EMAIL_HOST_PASSWORD_CUSTSUPP")
        },


    }
else:
    EMAIL_CONFIG = {
        "AUTH": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_AUTH"),
                'EMAIL_HOST_PASSWORD' 	        : os.environ.get("EMAIL_HOST_PASSWORD_AUTH")
        },
        "SHOPCART": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_SHOPCART"),
                'EMAIL_HOST_PASSWORD' 	        : os.environ.get("EMAIL_HOST_PASSWORD_SHOPCART")
        },
        "PRODSERV": {
                'EMAIL_HOST_USER'               : os.environ.get("EMAIL_HOST_USER_PRODSERV"),
                'EMAIL_HOST_PASSWORD'           : os.environ.get("EMAIL_HOST_PASSWORD_PRODSERV")
        },        
        "CUSTSUPP": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_CUSTSUPP"),
                'EMAIL_HOST_PASSWORD' 	        : os.environ.get("EMAIL_HOST_PASSWORD_CUSTSUPP")
        },
        "GENERAL": {
                'EMAIL_HOST_USER' 		: os.environ.get("EMAIL_HOST_USER_CUSTSUPP"),
                'EMAIL_HOST_PASSWORD' 	        : os.environ.get("EMAIL_HOST_PASSWORD_CUSTSUPP")
        },

    }
    
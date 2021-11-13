import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
 'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wavecompany$lima',
            'USER': 'wavecompany',
            'PASSWORD': 't73@ZeN89B5mt75',
            'HOST': 'wavecompany.mysql.pythonanywhere-services.com',
            'PORT': '3306',
                'OPTIONS': {
                'sql_mode': 'traditional',
            }
        },

}


#For Django Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'thewavecompany.app@gmail.com'
EMAIL_HOST_PASSWORD = 'bworedjxndeiivbw'  # os.environ['password_key'] suggested
EMAIL_USE_TLS = True

# email log
EMAIL_BACKEND = 'email_log.backends.EmailBackend'

DEBUG = True
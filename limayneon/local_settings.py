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




DEBUG = True
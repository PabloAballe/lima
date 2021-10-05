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
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wavecompany$lima_slave',
            'USER': 'wavecompany',
            'PASSWORD': 't73@ZeN89B5mt75',
            'HOST': 'wavecompany.mysql.pythonanywhere-services.com',
            'PORT': '3306',
                'OPTIONS': {
                'sql_mode': 'traditional',
            }
    }

}


def db_for_read(self, model, **hints):
    """
    Reads go to a randomly-chosen slave.
    """
    if test_connection_to_db('default'):
        return 'default'
    return 'slave'

def db_for_write(self, model, **hints):
    """
    Writes always go to master.
    """
    if test_connection_to_db('default'):
        return 'default'
    return 'slave'

DEBUG = True


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!)^^qd0wp-%y)95no^1^%2&&mhm2z#5#eoxr)4#i*&$m0j*=r='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
'*'
]


# Application definition

INSTALLED_APPS = [
    'lima',
    'dashboard',
    'help',
    'website',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'crispy_tailwind',
    'crispy_forms',
    #custom admin
    'simple_history',
    'import_export',
    'jsignature',
    'django_filters',
    'faicon',
    'tinymce',
    'admin_reorder',
    "django_unicorn",
    'django_mail_admin',
    'django.contrib.humanize',
    'multiselectfield',
    #'subdomains',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]


ROOT_URLCONF = 'limayneon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INTERNAL_IPS = [
    '37.14.105.28',
]


# def custom_show_toolbar(request):
#     return True # Always show toolbar, for example purposes only.

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
# }

WSGI_APPLICATION = 'limayneon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


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




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 #

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#color django admin_interface

X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0
IMPORT_EXPORT_USE_TRANSACTIONS = True
try:
    from .local_settings import *
except ImportError:
    pass

# For Django Email Backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'thewavecompany.app@gmail.com'
# EMAIL_HOST_PASSWORD = 'bworedjxndeiivbw'  # os.environ['password_key'] suggested
# EMAIL_USE_TLS = True

DJANGO_MAIL_ADMIN = {
    'BACKENDS': {
        'default': 'django_mail_admin.backends.CustomEmailBackend',
        'smtp': 'django.core.mail.backends.smtp.EmailBackend',
        'ses': 'django_ses.SESBackend',
    }
}


#firma
JSIGNATURE_WIDTH = 500
JSIGNATURE_HEIGHT = 200

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

DJANGORESIZED_DEFAULT_SIZE = [500, 500]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'PNG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'PNG': ".png"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


ADMIN_REORDER = (



    # models with custom name
    {'app': 'auth', 'models': (
        'auth.Group',
        {'model': 'auth.User', 'label': 'Usuarios'},
        {'model': 'lima.Tecnica', 'label': 'Tecnicas'},
    )},

    #Anuncios
    {'app': 'lima', 'label': 'Anuncios Clínicas',
     'models': ('lima.Anuncios',)
    },
    # Clientes
    {'app': 'lima', 'label': 'Clientes',
     'models': ('lima.Paciente','lima.Tratamientos','lima.Lista', 'lima.Cita', 'lima.ImagenesClientes', 'lima.Tags','lima.EstadosClientes')
    },
        # Centros
    {'app': 'lima', 'label': 'Centros',
     'models': ('lima.Centro',)
    },
     # Ayuda
    {'app': 'help', 'label': 'Ayuda y Tutoriales',
     'models': ('help.HelpClases','help.HelpPost',)
    },
       # Control Horario
    {'app': 'lima', 'label': 'Control de Horarios',
     'models': ('lima.ControlHorario','lima.Turnos')
    },

    #Paneles
    {'app': 'lima', 'label': 'Paneles',
     'models': ('lima.Paneles','lima.Estados','lima.Tareas',)
    },
    #Servicios
    {'app': 'lima', 'label': 'Servicios',
     'models': ('lima.Servicios',)
    },
    #Cajas
    {'app': 'lima', 'label': 'Servicios',
     'models': ('lima.Cajas',)
    },
    #Stock
    {'app': 'lima', 'label': 'Unidades de Stock',
     'models': ('lima.Stock',)
    },
    #WEB
    {'app': 'website', 'label': 'Sitio Web / APP',
     'models': ('website.Blog','website.Conctact','website.Pages')},
     #Email
     {'app': 'django_mail_admin', 'label': 'Emails'},
    # Tema
    {'app': 'admin_interface', 'label': 'Temas del Configurador'},
)




TINYMCE_JS_URL = 'http://debug.example.org/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
   'custom_undo_redo_levels': 20,
   'selector': 'textarea',
   'theme': 'silver',
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "es_ES",  # To force a specific language instead of the Django current language.
}


TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = True



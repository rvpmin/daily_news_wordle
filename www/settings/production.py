from .base import *
import environ

DEBUG = False

#Inicializa environ
env = environ.Env()
environ.Env.read_env() #Lee el archivo .env

# Configuración de la base de datos                                            
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
    'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'db',  # Nombre del servicio en docker-compose                  
    'PORT': '5432',
    }
}

try:
    from .local import *
except ImportError:
    pass

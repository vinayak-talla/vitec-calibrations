# settings/__init__.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# Determine which settings file to use (development/production)
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'Vitec_App.settings.development')

if settings_module == 'Vitec_App.settings.development':
    from .development import *
elif settings_module == 'Vitec_App.settings.production':
    from .production import *
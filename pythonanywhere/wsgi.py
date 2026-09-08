import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/energy-and-gas-us'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DATABASE_URL'] = 'your-database-url'
os.environ['JWT_SECRET'] = 'your-jwt-secret'
os.environ['FRONTEND_URL'] = 'https://yourusername.pythonanywhere.com'

from app import app as application

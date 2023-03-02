import os

from dotenv import load_dotenv

from booking import app


load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY", "something_special")

# Active le debogueur
DEBUG = True
TESTING = True
LIVESERVER_PORT = 8943
LIVESERVER_TIMEOUT = 10

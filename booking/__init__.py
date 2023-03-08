import os

from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY", "something_special")

from booking import views

import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret string")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:////" + os.path.join(app.root_path, "../data.db"),
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from chat.models import db

db.init_app(app)

import chat.handlers
import chat.views

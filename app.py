from flask import Flask
from flask_migrate import Migrate
from config import Configuration
from models import *

app = Flask(__name__)
app.secret_key = '456dsv8/e99vahga0_994hhks'
app.config.from_object(Configuration)
db.init_app(app)

migrate = Migrate(app, db)
from views import *
from admin import admin

if __name__ == '__main__':
    app.run()

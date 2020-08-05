from flask import Flask
from flask_migrate import Migrate
from config import Configuration
from models import *

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
migrate = Migrate(app, db)
from views import *

if __name__ == '__main__':
    app.run()

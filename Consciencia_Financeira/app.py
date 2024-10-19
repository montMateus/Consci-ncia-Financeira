from flask import Flask
from routes.expenses_route import expense_bp
from routes.user_route import user_bp
from routes.home_route import home_bp
from routes.index_route import index_bp
from database.database import db
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True

app.secret_key = 'financial'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(expense_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
app.register_blueprint(index_bp)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()

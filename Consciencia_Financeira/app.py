from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from sqlalchemy import func, distinct
from routes.expenses_route import expenses_bp
from routes.user_route import user_bp
from routes.home_route import home_bp
from routes.index_route import index_bp
from database.database import db
import webview
from functions_aux.expenses_graph import expensesGraph
from models.models import users, expenses

app = Flask(__name__)
app.debug=True

#window = webview.create_window('Financeiro', app)
app.secret_key = 'financial'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial.sqlite3'

db.init_app(app)

app.register_blueprint(expenses_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
app.register_blueprint(index_bp)

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()


if __name__ == '__main__':
    app.run()
        #webview.start()
    

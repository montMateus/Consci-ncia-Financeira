from database.database import db

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100), nullable=False)
    email = db.Column('email', db.String(100), unique=True, nullable=False)
    password = db.Column('password', db.String(20), nullable=False)
    expenses = db.Relationship('expenses', backref='users', lazy=True)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

class expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column('id', db.Integer, primary_key = True)
    expense_name = db.Column('expense_name', db.String(100), nullable=False)
    type = db.Column('type', db.String(50), nullable=False)
    value = db.Column('value', db.Numeric(10,2), nullable=False)
    day = db.Column('day', db.Integer, nullable=False)
    month = db.Column('month', db.String(20), nullable=False)
    year = db.Column('year', db.Integer, nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, expense_name, type, value, user_id, day, month, year):
        self.expense_name = expense_name
        self.type =  type
        self.value = value
        self.user_id = user_id
        self.day = day
        self.month = month
        self.year = year
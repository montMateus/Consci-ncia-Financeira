from database.database import db
from models.models import expenses
from sqlalchemy import func

class Filters:
    def __init__(self, day, month, year):
        self.day = day,
        self.month = month,
        self.year = year

    def filter_day_month_year(self, user_id, pam_day, pam_month, pam_year):
        query_filter = db.session.query(expenses.type, func.sum(expenses.value)).filter_by(user_id=user_id, day=pam_day, month=pam_month, year=pam_year).group_by(expenses.type).all()
        return query_filter
    
    def filter_month(self, user_id, pam_month, pam_year):
        query_filter = db.session.query(expenses.type, func.sum(expenses.value)).filter_by(user_id=user_id, month=pam_month, year=pam_year).group_by(expenses.type).all()
        return query_filter
    
    def filter_year(self, user_id, pam_year):
        query_filter = db.session.query(expenses.type, func.sum(expenses.value)).filter_by(user_id=user_id, year=pam_year).group_by(expenses.type).all()
        return query_filter  

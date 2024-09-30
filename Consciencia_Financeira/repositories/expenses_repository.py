from database.database import db
from models.models import expenses
from sqlalchemy import func

class expenseRepository:

    def add_expense(user_id, name, type, value, day, month, year):
        try:
            value = value.replace(',', '.')
            new_expense = expenses(expense_name=name, type=type, value=float(value), day=int(day), month=month, year=int(year), user_id = user_id)
            db.session.add(new_expense)
            db.session.commit()
            response = {'message': 'success'}
            return response
        except ValueError:
            response = {'message': 'error'}
            return response

    def delete_expense(id):
        expense = expenses.query.get(id)
        if expense is None:
            return 'not found'
        try:
            db.session.delete(expense)
            db.session.commit()
            return 'success'
        except Exception as e:
            db.session.rollback()
            return 'error'
    
    def filter_month(session, user_id, pam_month, pam_year):
        query_filter = db.session.query(expenses.type, func.sum(expenses.value)).filter_by(user_id=user_id, month=pam_month, year=pam_year).group_by(expenses.type).all()
        return query_filter
    
    def filter_year(user_id, pam_year):
        query_filter = db.session.query(expenses.type, func.sum(expenses.value)).filter_by(user_id=user_id, year=pam_year).group_by(expenses.type).all()
        return query_filter  
    
    def filter_day_month_year(user_id, pam_day, pam_month, pam_year):
        query_filter = db.session.query(expenses.type, func.sum(expenses.value)).filter_by(user_id=user_id, day=pam_day, month=pam_month, year=pam_year).group_by(expenses.type).all()
        return query_filter
    
    ###################################################
    
    def filter_total_month(user_id, pam_month, pam_year):
        query_total_filter = db.session.query(func.sum(expenses.value)).filter(expenses.user_id == user_id, expenses.month == pam_month, expenses.year == int(pam_year)).scalar()
        return query_total_filter
    
    def filter_total_year(user_id, pam_year):
        query_total_filter = db.session.query(func.sum(expenses.value)).filter(expenses.user_id == user_id, expenses.year == int(pam_year)).scalar()
        return query_total_filter 
    
    def filter_total_day_month_year(user_id, pam_day, pam_month, pam_year):
        query_total_filter = db.session.query(func.sum(expenses.value)).filter(expenses.user_id == user_id, expenses.day == int(pam_day), expenses.month == pam_month, expenses.year == int(pam_year)).scalar()
        return query_total_filter

    

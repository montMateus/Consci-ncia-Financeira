from models.models import ExpenseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

class ExpenseRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_expense(self, user_id, name, type, value, day, month, year):
        try:
            value = value.replace(',', '.')
            new_expense = ExpenseModel(expense_name=name, type=type, value=float(value), day=int(day), month=month, year=int(year), user_id = user_id)
            self.db_session.add(new_expense)
            self.db_session.commit()
            response = {'message': 'success'}
            return response
        except ValueError:
            response = {'message': 'error'}
            return response

    def delete_expense(self, id):
        expense = ExpenseModel.query.get(id)
        if expense is None:
            return 'not found'
        try:
            self.db_session.delete(expense)
            self.db_session.commit()
            return 'success'
        except Exception as e:
            self.db_session.rollback()
            return 'error'
    
    def filter_month(self, user_id, pam_month, pam_year):
        query_filter = self.db_session.query(ExpenseModel.type, func.sum(ExpenseModel.value)).filter_by(user_id=user_id, month=pam_month, year=pam_year).group_by(ExpenseModel.type).all()
        return query_filter
    
    def filter_year(self, user_id, pam_year):
        query_filter = self.db_session.query(ExpenseModel.type, func.sum(ExpenseModel.value)).filter_by(user_id=user_id, year=pam_year).group_by(ExpenseModel.type).all()
        return query_filter  
    
    def filter_day_month_year(self, user_id, pam_day, pam_month, pam_year):
        query_filter = self.db_session.query(ExpenseModel.type, func.sum(ExpenseModel.value)).filter_by(user_id=user_id, day=pam_day, month=pam_month, year=pam_year).group_by(ExpenseModel.type).all()
        return query_filter
    
    def filter_total_month(self, user_id, pam_month, pam_year):
        query_total_filter = self.db_session.query(func.sum(ExpenseModel.value)).filter(ExpenseModel.user_id == user_id, ExpenseModel.month == pam_month, ExpenseModel.year == int(pam_year)).scalar()
        return query_total_filter
    
    def filter_total_year(self, user_id, pam_year):
        query_total_filter = self.db_session.query(func.sum(ExpenseModel.value)).filter(ExpenseModel.user_id == user_id, ExpenseModel.year == int(pam_year)).scalar()
        return query_total_filter 
    
    def filter_total_day_month_year(self, user_id, pam_day, pam_month, pam_year):
        query_total_filter = self.db_session.query(func.sum(ExpenseModel.value)).filter(ExpenseModel.user_id == user_id, ExpenseModel.day == int(pam_day), ExpenseModel.month == pam_month, ExpenseModel.year == int(pam_year)).scalar()
        return query_total_filter

    

from database.database import db
from models.models import ExpenseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

class Filters:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def filter_day_month_year(self, user_id: int, pam_day: int, pam_month: str, pam_year: int):
        query_filter = self.db_session.query(ExpenseModel.type, func.sum(ExpenseModel.value)).filter_by(user_id=user_id, day=pam_day, month=pam_month, year=pam_year).group_by(ExpenseModel.type).all()
        return query_filter
    
    def filter_month(self, user_id: int, pam_month: str, pam_year: int):
        query_filter = self.db_session.query(ExpenseModel.type, func.sum(ExpenseModel.value)).filter_by(user_id=user_id, month=pam_month, year=pam_year).group_by(ExpenseModel.type).all()
        return query_filter
    
    def filter_year(self, user_id: int, pam_year: int):
        query_filter = self.db_session.query(ExpenseModel.type, func.sum(ExpenseModel.value)).filter_by(user_id=user_id, year=pam_year).group_by(ExpenseModel.type).all()
        return query_filter  

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from models.models import UserModel

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def login(self, email: str, password: str):
        user = self.db_session.query(UserModel).filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return user
            return "incorrect_password"
        return "user_not_found"
        
    def register(self, name: str, email: str, password: str):
        if self.db_session.query(UserModel).filter_by(email=email).first():
            return "email_already_registered"
        
        if len(password) > 20:
            return "password_too_long"
        
        hashed_password = generate_password_hash(password)
        new_UserModel = UserModel(name=name, email=email, password=hashed_password)
        
        self.db_session.add(new_UserModel)
        self.db_session.commit()
        
        return new_UserModel
    
    def delete_user(self, id: int):
        try:
            user = self.db_session.query(UserModel).filter_by(id=id).first()
            if user:
                self.db_session.delete(user)
                self.db_session.commit()
                self.db_session.refresh(user)
            else:
                return 'No user found'
        except Exception as e:
            self.db_session.rollback()
            print(f'Erro: {e}') 

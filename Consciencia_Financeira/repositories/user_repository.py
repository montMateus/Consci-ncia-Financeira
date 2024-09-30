from database.database import db
from models.models import users
from werkzeug.security import generate_password_hash, check_password_hash

class userRepository:

    def login(email, password):
        user = db.session.query(users).filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if len(password) > 20:
                    return "password_length_exceeded"
                return user
            else:
                return "incorrect_password"
        else:
            return "user_not_found"
        
    def register(name, email, password):
        if users.query.filter_by(email=email).first():
            return "email_already_registered"
        
        if len(password) > 20:
            return "password_too_long"
        
        hashed_password = generate_password_hash(password)
        
        new_user = users(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return new_user
    

from flask import Blueprint, session, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import func, distinct
from database.database import db
from models.models import users, expenses
from functions_aux.expenses_graph import expensesGraph
from functions_aux.filters import Filters
from repositories.user_repository import userRepository

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        response = userRepository.login(email, password)

        if isinstance(response, str):
            if response in ["password_length_exceeded", "user_not_found", "incorrect_password"]:
                flash('Erro: Os dados não estão corretos', 'danger')
        else:
            session['email'] = email
            session['name'] = response.name
            session['user_id'] = response.id
            session.permanent = True
            return redirect(url_for('home.home'))
    return render_template('login.html')

@user_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        session.permanent = True
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        response = userRepository.register(name, email, password)

        if response == "email_already_registered":
            flash('Erro: Este email já está vinculado em outra conta', 'danger')
        elif response == "password_too_long":
            flash('Erro: A sua senha não pode conter mais de 20 caracteres', 'info')
        elif isinstance(response, users):
            session['email'] = email
            session['name'] = name
            session['user_id'] = response.id
            return redirect(url_for('home.home'))
        else:
            flash('Erro ao registrar o usuário', 'danger')

    return render_template('register.html')

@user_bp.route('/log-out')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('email', None)
    flash('Você saiu da sua conta', 'info')
    return redirect(url_for('user.login'))

@user_bp.route('/home/delete_user/<int:id>', methods=['DELETE'])
def delete_user(user_id):
    if 'user_id' not in session or session['user_id'] != id:
        return jsonify({'message': 'Não autorizado.'}), 403
    else:
        try:
            expenses_user = expenses.query.filter_by(user_id=user_id).all()
            for expense in expenses_user:
                db.session.delete(expense)
            user = users.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({'message': 'Usuário excluído com sucesso'}), 200
            else:
                return jsonify({'message': 'Usuário não encontrado.'}), 404
        except Exception as e:
            db.session.rollback()
            print(f'Erro: {e}')
            return jsonify({'message': 'Erro ao excluir usuário.'}), 500
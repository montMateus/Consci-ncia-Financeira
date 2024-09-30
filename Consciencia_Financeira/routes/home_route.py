from flask import Blueprint, session, render_template, request, redirect, url_for, flash, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    user_id = session.get('user_id')
    print(user_id)
    user_name = session.get('name')
    print(user_name)

    if not user_id:
        flash('Usuário não logado', 'danger')
        return redirect(url_for('user.login'))
    return render_template('home.html', user_name=user_name, user_id=user_id)
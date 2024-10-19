from flask import Blueprint, session, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import func, distinct
from database.database import db
from models.models import ExpenseModel
from functions_aux.expenses_graph import expensesGraph
from repositories.expenses_repository import ExpenseRepository

expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/expense', methods=['GET', 'POST'])
def list_expense():
    user_id = session.get('user_id')
    user_name = session.get('name')

    if not user_id:
        flash('Usuário não logado', 'danger')
        return redirect(url_for('user.login'))

    page = request.args.get('page', 1, type=int)
    per_page = 5
    graph = None
    filter_day = request.args.get('filter_day_select', '')
    filter_month = request.args.get('filter_month_selectt', '')
    filter_year = request.args.get('filter_year_select', '')
    filter_warning = ''
    total_year = None
    total_espec = None
    total_month = None
    user_years = db.session.query(distinct(ExpenseModel.year)).filter_by(user_id=user_id).all()
    user_years = [year[0] for year in user_years]

    filters = [ExpenseModel.user_id == user_id]

    if request.method == 'POST':
        filter_day = request.form.get('filter_day_select', '')
        filter_month = request.form.get('filter_month_select', '')
        filter_year = request.form.get('filter_year_select', '')

    if filter_day and filter_day != '':
        filters.append(ExpenseModel.day == int(filter_day))
    if filter_month and filter_month != '':
        filters.append(ExpenseModel.month == ExpenseModel.month)
    if filter_year and filter_year != '':
        filters.append(ExpenseModel.year == int(filter_year))

    list_Expense = db.session.query(ExpenseModel).filter(*filters)
    list_Expense_pag = list_Expense.paginate(page=page, per_page=per_page)

    if list_Expense_pag.items:
        if filter_day == '' and filter_month != '' and filter_year != '':
            total_month = ExpenseRepository(db.session).filter_total_month(user_id, filter_month, filter_year)
            query_filter = ExpenseRepository(db.session).filter_month(user_id, filter_month, filter_year)
            graph = expensesGraph(query_filter, filter_day, filter_month, filter_year, user_id)

        elif filter_day != '' and filter_month != '' and filter_year != '':
            total_espec = ExpenseRepository(db.session).filter_total_day_month_year(user_id, filter_day, filter_month, filter_year)
            query_filter = ExpenseRepository(db.session).filter_day_month_year(user_id, filter_day, filter_month, filter_year)
            graph = expensesGraph(query_filter, filter_day, filter_month, filter_year, user_id)

        elif filter_year != '' and filter_day == '' and filter_month == '':
            total_year = ExpenseRepository(db.session).filter_total_year(user_id, filter_year)
            query_filter = ExpenseRepository(db.session).filter_year(user_id, filter_year)
            graph = expensesGraph(query_filter, filter_day, filter_month, filter_year, user_id)
    else:
        filter_warning = f'Nenhuma despesa encontrada com os filtros: day = {filter_day}, month= {filter_month}, Ano = {filter_year}'

    return render_template('expenses.html', 
                           expenses=list_Expense_pag, 
                           total_mes=total_month, 
                           total_espec=total_espec, 
                           total_year=total_year, 
                           filter_day=filter_day, 
                           filter_month=filter_month, 
                           filter_year=filter_year, 
                           user_years=user_years, 
                           user_name=user_name, 
                           filter_warning=filter_warning,
                           graph=graph,
                           user_id=user_id)

@expense_bp.route('/expense/add', methods=['GET', 'POST'])
def add_expense():
    user_id = session.get('user_id')
    if not user_id:
        flash('Usuário não logado', 'danger')
        return redirect(url_for('user.login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        value = request.form.get('value')
        day = request.form.get('day')
        month= request.form.get('month')
        year = request.form.get('year')

        if name and type and value and day and month and year:
            response = ExpenseRepository(db.session).add_expense(user_id, name, type, value, day, month, year)
            if response == 'success':
                return redirect(url_for('ExpenseModel.list_Expense'))
            else:
                flash('Valor inválido para despesa', 'danger')
    return render_template('add_expense.html')

@expense_bp.route('/expense/delete/<int:id>', methods=['DELETE'])
def delete_expense(id):
    response = ExpenseRepository(db.session).delete_expense(id)
    if response == 'not found':
        return jsonify({"message": "Despesa não encontrada"}), 404
    elif response == 'success':
        return jsonify({"message": "Despesa excluída com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao excluir despesa"}), 500


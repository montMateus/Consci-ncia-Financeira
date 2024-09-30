from flask import Blueprint, session, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import func, distinct
from database.database import db
from models.models import expenses
from functions_aux.expenses_graph import expensesGraph
from repositories.expenses_repository import expenseRepository

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses', methods=['GET', 'POST'])
def list_expenses():
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
    user_years = db.session.query(distinct(expenses.year)).filter_by(user_id=user_id).all()
    user_years = [year[0] for year in user_years]

    filters = [expenses.user_id == user_id]

    #RECEBE OS valueES DAS 3 OPÇÕES DE FILTRO

    if request.method == 'POST':
        filter_day = request.form.get('filter_day_select', '')
        filter_month = request.form.get('filter_month_select', '')
        filter_year = request.form.get('filter_year_select', '')
    
    #CASO O USUÁRIO TENHA SELECIONADO O FILTRO, SELE SERÁ ADICIONADO A LISTA 'FILTROS'

    if filter_day and filter_day != '':
        filters.append(expenses.day == int(filter_day))
    if filter_month and filter_month != '':
        filters.append(expenses.month == expenses.month)
    if filter_year and filter_year != '':
        filters.append(expenses.year == int(filter_year))

    #PAGINAÇÃO DAS expenses

    list_expenses = db.session.query(expenses).filter(*filters)
    list_expenses_pag = list_expenses.paginate(page=page, per_page=per_page)

    if list_expenses_pag.items:
        #CASO APENAS O FILTRO DE day NÃO TENHA SIDO SELECIONADO, O FILTRO SERÁ DE UM MÊS E ANO
        if filter_day == '' and filter_month != '' and filter_year != '':
            total_month = expenseRepository.filter_total_month(user_id, filter_month, filter_year)
            query_filter = expenseRepository.filter_month(user_id, filter_month, filter_year)
            graph = expensesGraph(query_filter, filter_day, filter_month, filter_year, user_id)

        #CASO TODOS OS FILTROS TENHAM SIDO SEELCIONADOS, O FILTRO SERÁ DE DIA, MÊS E ANO
        elif filter_day != '' and filter_month != '' and filter_year != '':
            total_espec = expenseRepository.filter_total_day_month_year(user_id, filter_day, filter_month, filter_year)
            query_filter = expenseRepository.filter_day_month_year(user_id, filter_day, filter_month, filter_year)
            graph = expensesGraph(query_filter, filter_day, filter_month, filter_year, user_id)

        #CASO APENAS O FILTRO DE ANO TENHA SIDO SELECIONADO, O FILTRO SERÁ APENAS PELO ANO
        elif filter_year != '' and filter_day == '' and filter_month == '':
            total_year = expenseRepository.filter_total_year(user_id, filter_year)
            query_filter = expenseRepository.filter_year(user_id, filter_year)
            graph = expensesGraph(query_filter, filter_day, filter_month, filter_year, user_id)
    else:
        #CASO NENHUMA expenses FOI ENCONTRADA, O SEGUINTE AVISO SERÁ RETORNADO:
        filter_warning = f'Nenhuma despesa encontrada com os filtros: day = {filter_day}, month= {filter_month}, Ano = {filter_year}'

    return render_template('expenses.html', 
                           expenses=list_expenses_pag, 
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

#EXCLUÍ O USUÁRIO DA SESSÃO ATUAL, ATRAVÉS DO SEU ID NA ROTA

#ADICIONA A DESPESA NO BANCO DE DADOS, RECEBENDO OS valueES DO FORMULÁRIO.
@expenses_bp.route('/expenses/add', methods=['GET', 'POST'])
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
            response = expenseRepository.add_expense(user_id, name, type, value, day, month, year)
            if response == 'success':
                return redirect(url_for('expenses.list_expenses'))
            else:
                flash('Valor inválido para despesa', 'danger')
    return render_template('add_expense.html')

#EXCLUÍ A DESPESA, ATRAVÉS DE SEU ID NA ROTA
@expenses_bp.route('/expenses/delete/<int:id>', methods=['DELETE'])
def delete_expense(id):
    response = expenseRepository.delete_expense(id)
    if response == 'not found':
        return jsonify({"message": "Despesa não encontrada"}), 404
    elif response == 'success':
        return jsonify({"message": "Despesa excluída com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao excluir despesa"}), 500


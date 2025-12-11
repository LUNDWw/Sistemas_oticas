"""
Cash Flow Routes
Handles routes for cash flow management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services import cashflow_service
from app.utils import validate_amount, validate_date, is_safe_redirect
from datetime import datetime, timedelta

cashflow_bp = Blueprint('cashflow', __name__, url_prefix='/cashflow')


def safe_redirect_to(default_route):
    """Helper para redirecionar com segurança contra open redirect"""
    if request.referrer and is_safe_redirect(request.referrer, request.host):
        return redirect(request.referrer)
    return redirect(url_for(default_route))


@cashflow_bp.route('/')
def index():
    """Cash flow main page"""
    # Get filters from query params
    filter_type = request.args.get('type', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    # Build filters
    filters = {}
    if filter_type != 'all':
        filters['type'] = filter_type
    if start_date:
        filters['start_date'] = start_date
    if end_date:
        filters['end_date'] = end_date
    if category:
        filters['category'] = category
    
    # Get data
    balance_data = cashflow_service.calculate_balance()
    movements = cashflow_service.get_movements(filters)
    
    # Get summary for current month
    today = datetime.now()
    month_start = today.replace(day=1).strftime('%Y-%m-%d')
    month_end = today.strftime('%Y-%m-%d')
    monthly_summary = cashflow_service.get_summary(month_start, month_end)
    
    return render_template(
        'cashflow.html',
        balance=balance_data['balance'],
        total_entries=balance_data['total_entries'],
        total_exits=balance_data['total_exits'],
        movements=movements,
        monthly_summary=monthly_summary,
        filter_type=filter_type,
        start_date=start_date,
        end_date=end_date,
        category=category
    )


@cashflow_bp.route('/entry', methods=['POST'])
def add_entry():
    """Add cash entry"""
    try:
        # Validar amount
        valid, amount, error = validate_amount(request.form.get('amount'))
        if not valid:
            flash(f'Erro na validação: {error}', 'error')
            return redirect(url_for('cashflow.index'))
        
        # Validar data se fornecida
        date_str = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        valid_date, date_error = validate_date(date_str)
        if not valid_date:
            flash(f'Erro na validação: {date_error}', 'error')
            return redirect(url_for('cashflow.index'))
        
        data = {
            'date': date_str,
            'category': request.form.get('category', ''),
            'description': request.form.get('description', ''),
            'amount': amount,
            'payment_method': request.form.get('payment_method', ''),
            'order_id': request.form.get('order_id')
        }
        
        cashflow_service.add_entry(data)
        flash('Entrada registrada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao registrar entrada: {str(e)}', 'error')
    
    return redirect(url_for('cashflow.index'))


@cashflow_bp.route('/exit', methods=['POST'])
def add_exit():
    """Add cash exit"""
    try:
        # Validar amount
        valid, amount, error = validate_amount(request.form.get('amount'))
        if not valid:
            flash(f'Erro na validação: {error}', 'error')
            return redirect(url_for('cashflow.index'))
        
        # Validar data se fornecida
        date_str = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        valid_date, date_error = validate_date(date_str)
        if not valid_date:
            flash(f'Erro na validação: {date_error}', 'error')
            return redirect(url_for('cashflow.index'))
        
        data = {
            'date': date_str,
            'category': request.form.get('category', ''),
            'description': request.form.get('description', ''),
            'amount': amount,
            'payment_method': request.form.get('payment_method', '')
        }
        
        cashflow_service.add_exit(data)
        flash('Saída registrada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao registrar saída: {str(e)}', 'error')
    
    return redirect(url_for('cashflow.index'))


@cashflow_bp.route('/edit/<int:movement_id>', methods=['POST'])
def edit_movement(movement_id):
    """Edit a cash flow movement"""
    try:
        from app.models import get_db
        
        # Validar amount
        valid, amount, error = validate_amount(request.form.get('amount'))
        if not valid:
            flash(f'Erro na validação: {error}', 'error')
            return redirect(url_for('cashflow.index'))
        
        # Validar data se fornecida
        date_str = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        valid_date, date_error = validate_date(date_str)
        if not valid_date:
            flash(f'Erro na validação: {date_error}', 'error')
            return redirect(url_for('cashflow.index'))
        
        db = get_db()
        
        # Update the movement
        db.execute("""
            UPDATE cash_flow 
            SET date=?, category=?, description=?, amount=?, payment_method=?
            WHERE id=?
        """, (
            date_str,
            request.form.get('category', ''),
            request.form.get('description', ''),
            amount,
            request.form.get('payment_method', ''),
            movement_id
        ))
        db.commit()
        flash('Movimentação atualizada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar movimentação: {str(e)}', 'error')
    
    return redirect(url_for('cashflow.index'))


@cashflow_bp.route('/partial-payment/<int:order_id>', methods=['POST'])
def add_partial_payment(order_id):
    """Add partial payment for an order"""
    try:
        # Validar amount
        valid, amount, error = validate_amount(request.form.get('amount'))
        if not valid:
            flash(f'Erro na validação: {error}', 'error')
            return redirect(url_for('order.details', order_id=order_id))
        
        # Validar data se fornecida
        date_str = request.form.get('payment_date', datetime.now().strftime('%Y-%m-%d'))
        valid_date, date_error = validate_date(date_str)
        if not valid_date:
            flash(f'Erro na validação: {date_error}', 'error')
            return redirect(url_for('order.details', order_id=order_id))
        
        data = {
            'amount': amount,
            'payment_date': date_str,
            'payment_method': request.form.get('payment_method', ''),
            'notes': request.form.get('notes', '')
        }
        
        cashflow_service.add_partial_payment(order_id, data)
        flash('Pagamento parcial registrado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao registrar pagamento: {str(e)}', 'error')
    
    return redirect(url_for('order.details', order_id=order_id))


@cashflow_bp.route('/partial-payment/edit/<int:payment_id>', methods=['POST'])
def edit_partial_payment(payment_id):
    """Edit a partial payment"""
    try:
        # Validar amount
        valid, amount, error = validate_amount(request.form.get('amount'))
        if not valid:
            flash(f'Erro na validação: {error}', 'error')
            order_id = request.form.get('order_id')
            if order_id:
                return redirect(url_for('order.details', order_id=order_id))
            return safe_redirect_to('main.index')
        
        # Validar data se fornecida
        date_str = request.form.get('payment_date', datetime.now().strftime('%Y-%m-%d'))
        valid_date, date_error = validate_date(date_str)
        if not valid_date:
            flash(f'Erro na validação: {date_error}', 'error')
            order_id = request.form.get('order_id')
            if order_id:
                return redirect(url_for('order.details', order_id=order_id))
            return safe_redirect_to('main.index')
        
        data = {
            'amount': amount,
            'payment_date': date_str,
            'payment_method': request.form.get('payment_method', ''),
            'notes': request.form.get('notes', '')
        }
        
        cashflow_service.edit_partial_payment(payment_id, data)
        flash('Pagamento atualizado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar pagamento: {str(e)}', 'error')
    
    order_id = request.form.get('order_id')
    if order_id:
        return redirect(url_for('order.details', order_id=order_id))
    return safe_redirect_to('main.index')


@cashflow_bp.route('/partial-payment/delete/<int:payment_id>', methods=['POST'])
def delete_partial_payment(payment_id):
    """Delete a partial payment"""
    try:
        cashflow_service.delete_partial_payment(payment_id)
        flash('Pagamento excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir pagamento: {str(e)}', 'error')
    
    order_id = request.form.get('order_id')
    if order_id:
        return redirect(url_for('order.details', order_id=order_id))
    return safe_redirect_to('main.index')


@cashflow_bp.route('/order-balance/<int:order_id>')
def get_order_balance(order_id):
    """Get balance for a specific order (API endpoint)"""
    balance = cashflow_service.get_order_balance(order_id)
    if balance:
        return jsonify(balance)
    return jsonify({'error': 'Order not found'}), 404


@cashflow_bp.route('/balance')
def get_balance():
    """Get current balance (API endpoint)"""
    balance_data = cashflow_service.calculate_balance()
    return jsonify(balance_data)

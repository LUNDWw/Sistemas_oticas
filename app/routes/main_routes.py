import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.models import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    db = get_db()
    q = request.args.get('q', '')
    status = request.args.get('status', 'all')
    filter_store = request.args.get('store', 'all')

    sql = "SELECT * FROM orders WHERE deleted_at IS NULL"
    params = []
    if q:
        sql += " AND (os_number LIKE ? OR client_name LIKE ? OR phone LIKE ?)"
        qv = f"%{q}%"
        params.extend([qv, qv, qv])
    if status and status != 'all':
        if status == 'pago_dinheiro':
            sql += " AND payment_status = 'Pago' AND payment_method = 'Dinheiro'"
        elif status == 'pago_cartao':
            sql += " AND payment_status = 'Pago' AND payment_method LIKE 'Cartão%'"
        else:
            sql += " AND payment_status = ?"
            params.append(status)
    if filter_store and filter_store != 'all':
        sql += " AND store = ?"
        params.append(filter_store)
    sql += " ORDER BY id DESC"

    orders = db.execute(sql, params).fetchall()
    stores = [r[0] for r in db.execute("SELECT DISTINCT store FROM orders WHERE store IS NOT NULL AND deleted_at IS NULL").fetchall()]
    return render_template('index.html', orders=orders, q=q, status=status, stores=stores, filter_store=filter_store)

@main_bp.context_processor
def inject_now():
    return {'now': int(time.time())}

@main_bp.app_errorhandler(500)
def internal_error(e):
    import logging
    logging.exception('Server error')
    flash('Ocorreu um erro interno.', 'danger')
    return render_template('500.html'), 500

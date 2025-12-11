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

@main_bp.route('/debug/static')
def debug_static():
    try:
        files = []
        if os.path.exists(current_app.static_folder):
            for f in os.listdir(current_app.static_folder):
                full_path = os.path.join(current_app.static_folder, f)
                size = os.path.getsize(full_path) if os.path.isfile(full_path) else 'DIR'
                files.append({'name': f, 'size': size})
        
        from app.config import BASE_DIR
        # Proteger import de INTERNAL_DIR que só existe em modo frozen
        try:
            from app.config import INTERNAL_DIR
        except ImportError:
            INTERNAL_DIR = BASE_DIR
        
        return jsonify({
            'static_folder': current_app.static_folder,
            'exists': os.path.exists(current_app.static_folder),
            'files': files,
            'base_dir': BASE_DIR,
            'internal_dir': INTERNAL_DIR
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@main_bp.context_processor
def inject_now():
    return {'now': int(time.time())}

@main_bp.app_errorhandler(500)
def internal_error(e):
    import logging
    logging.exception('Server error')
    flash('Ocorreu um erro interno.', 'danger')
    return render_template('500.html'), 500

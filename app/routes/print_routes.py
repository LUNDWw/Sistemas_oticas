from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import get_db

print_bp = Blueprint('print', __name__)

@print_bp.route('/print/order/<int:order_id>')
def print_order(order_id):
    db = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    
    if not order:
        flash('Ordem não encontrada.', 'danger')
        return redirect(url_for('main.index'))
        
    graus = db.execute('SELECT * FROM graus WHERE order_id = ?', (order_id,)).fetchall()
    
    return render_template('print_order.html', order=order, graus=graus)

"""
Cash Flow Service
Handles business logic for cash flow management
"""
from app.models import get_db
from datetime import datetime


def calculate_balance():
    """Calculate current cash balance (entries - exits)"""
    db = get_db()
    
    # Sum all entries
    entries = db.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM cash_flow WHERE type = 'entrada'"
    ).fetchone()
    
    # Sum all exits
    exits = db.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM cash_flow WHERE type = 'saida'"
    ).fetchone()
    
    balance = entries['total'] - exits['total']
    return {
        'balance': balance,
        'total_entries': entries['total'],
        'total_exits': exits['total']
    }


def get_movements(filters=None):
    """Get cash flow movements with optional filters"""
    db = get_db()
    query = "SELECT * FROM cash_flow"
    params = []
    conditions = []
    
    if filters:
        if filters.get('type'):
            conditions.append("type = ?")
            params.append(filters['type'])
        
        if filters.get('start_date'):
            conditions.append("date >= ?")
            params.append(filters['start_date'])
        
        if filters.get('end_date'):
            conditions.append("date <= ?")
            params.append(filters['end_date'])
        
        if filters.get('category'):
            conditions.append("category = ?")
            params.append(filters['category'])
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY date DESC, created_at DESC"
    
    return db.execute(query, params).fetchall()


def add_entry(data):
    """Add a cash entry"""
    db = get_db()
    cursor = db.execute("""
        INSERT INTO cash_flow (date, type, category, description, amount, payment_method, order_id)
        VALUES (?, 'entrada', ?, ?, ?, ?, ?)
    """, (
        data.get('date', datetime.now().strftime('%Y-%m-%d')),
        data.get('category'),
        data.get('description'),
        data['amount'],
        data.get('payment_method'),
        data.get('order_id')
    ))
    db.commit()
    return cursor.lastrowid


def add_exit(data):
    """Add a cash exit"""
    db = get_db()
    cursor = db.execute("""
        INSERT INTO cash_flow (date, type, category, description, amount, payment_method)
        VALUES (?, 'saida', ?, ?, ?, ?)
    """, (
        data.get('date', datetime.now().strftime('%Y-%m-%d')),
        data.get('category'),
        data.get('description'),
        data['amount'],
        data.get('payment_method')
    ))
    db.commit()
    return cursor.lastrowid


def add_partial_payment(order_id, data):
    """Add a partial payment for an order"""
    db = get_db()
    
    # Insert partial payment
    cursor = db.execute("""
        INSERT INTO partial_payments (order_id, amount, payment_date, payment_method, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        order_id,
        data['amount'],
        data.get('payment_date', datetime.now().strftime('%Y-%m-%d')),
        data.get('payment_method'),
        data.get('notes')
    ))
    
    # Also add to cash_flow as an entry
    cursor_cf = db.execute("""
        INSERT INTO cash_flow (date, type, category, description, amount, payment_method, order_id)
        VALUES (?, 'entrada', 'Pagamento Parcial', ?, ?, ?, ?)
    """, (
        data.get('payment_date', datetime.now().strftime('%Y-%m-%d')),
        f"Pagamento parcial - OS #{order_id}",
        data['amount'],
        data.get('payment_method'),
        order_id
    ))
    cash_flow_id = cursor_cf.lastrowid
    
    # Update partial_payment with cash_flow_id
    db.execute("UPDATE partial_payments SET cash_flow_id = ? WHERE id = ?", (cash_flow_id, cursor.lastrowid))
    
    db.commit()
    return cursor.lastrowid


def edit_partial_payment(payment_id, data):
    """Edit a partial payment"""
    db = get_db()
    
    # Get existing payment to find cash_flow_id
    payment = db.execute("SELECT * FROM partial_payments WHERE id = ?", (payment_id,)).fetchone()
    if not payment:
        raise ValueError("Pagamento não encontrado")
        
    # Update partial payment
    db.execute("""
        UPDATE partial_payments 
        SET amount = ?, payment_date = ?, payment_method = ?, notes = ?
        WHERE id = ?
    """, (
        data['amount'],
        data.get('payment_date'),
        data.get('payment_method'),
        data.get('notes'),
        payment_id
    ))
    
    # Update associated cash flow entry if it exists
    if payment['cash_flow_id']:
        db.execute("""
            UPDATE cash_flow 
            SET date = ?, amount = ?, payment_method = ?
            WHERE id = ?
        """, (
            data.get('payment_date'),
            data['amount'],
            data.get('payment_method'),
            payment['cash_flow_id']
        ))
        
    db.commit()


def delete_partial_payment(payment_id):
    """Delete a partial payment"""
    db = get_db()
    
    # Get existing payment to find cash_flow_id
    payment = db.execute("SELECT * FROM partial_payments WHERE id = ?", (payment_id,)).fetchone()
    if not payment:
        raise ValueError("Pagamento não encontrado")
        
    # Delete associated cash flow entry if it exists
    if payment['cash_flow_id']:
        db.execute("DELETE FROM cash_flow WHERE id = ?", (payment['cash_flow_id'],))
        
    # Delete partial payment
    db.execute("DELETE FROM partial_payments WHERE id = ?", (payment_id,))
    
    db.commit()


def get_order_balance(order_id):
    """Get payment balance for a specific order"""
    db = get_db()
    
    # Get order total (assuming it's stored in valor_pago or similar field)
    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        return None
    
    # Get total partial payments
    payments = db.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM partial_payments WHERE order_id = ?",
        (order_id,)
    ).fetchone()
    
    total_paid = payments['total']
    
    # Calculate remaining (you may need to adjust this based on your order structure)
    # For now, using valor_pago as the total order value
    order_total = order['valor_pago'] or 0
    remaining = order_total - total_paid
    
    return {
        'order_id': order_id,
        'order_total': order_total,
        'total_paid': total_paid,
        'remaining': remaining,
        'payments': get_partial_payments(order_id)
    }


def get_partial_payments(order_id):
    """Get all partial payments for an order"""
    db = get_db()
    return db.execute(
        "SELECT * FROM partial_payments WHERE order_id = ? ORDER BY payment_date DESC",
        (order_id,)
    ).fetchall()


def get_summary(start_date=None, end_date=None):
    """Get summary of cash flow for a period"""
    db = get_db()
    
    conditions = []
    params = []
    
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
    
    # Build WHERE clause for date filters (if any)
    date_where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    # Get entries (with type filter)
    entries_conditions = conditions.copy()
    entries_conditions.append("type = 'entrada'")
    entries_where = " WHERE " + " AND ".join(entries_conditions)
    
    entries = db.execute(
        f"SELECT COALESCE(SUM(amount), 0) as total FROM cash_flow{entries_where}",
        params
    ).fetchone()
    
    # Get exits (with type filter)
    exits_conditions = conditions.copy()
    exits_conditions.append("type = 'saida'")
    exits_where = " WHERE " + " AND ".join(exits_conditions)
    
    exits = db.execute(
        f"SELECT COALESCE(SUM(amount), 0) as total FROM cash_flow{exits_where}",
        params
    ).fetchone()
    
    return {
        'entries': entries['total'],
        'exits': exits['total'],
        'balance': entries['total'] - exits['total']
    }

"""
Order Service
Provide methods for database operations related to Orders and Degrees (Graus)
"""
from datetime import datetime

def get_order_by_id(db, order_id):
    return db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()

def get_graus_for_order(db, order_id):
    return db.execute('SELECT * FROM graus WHERE order_id = ?', (order_id,)).fetchall()

def create_order(db, order_data):
    db.execute('''INSERT INTO orders (
        os_number, client_name, phone, purchase_type, store, lab, payment_status, payment_method, installments, lab_paid, exam_date, delivery_date,
        cpf, receita_fora, nome_doutor_fora, valor_pago, entrada, valor_retirada, nome_doutor_otica, endereco
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', order_data)
    db.commit()

def update_order(db, order_id, order_data):
    db.execute('''UPDATE orders SET
        os_number=?, client_name=?, phone=?, purchase_type=?, store=?, lab=?, payment_status=?, payment_method=?, installments=?, lab_paid=?, exam_date=?, delivery_date=?,
        cpf=?, receita_fora=?, nome_doutor_fora=?, valor_pago=?, entrada=?, valor_retirada=?, nome_doutor_otica=?, endereco=?
        WHERE id=?''', order_data + (order_id,))
    db.commit()

def soft_delete_order(db, order_id):
    try:
        deleted_at = datetime.now().isoformat()
        db.execute("UPDATE orders SET deleted_at = ? WHERE id = ?", (deleted_at, order_id))
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao fazer soft-delete de ordem: {e}")
        return False

def add_grau(db, grau_data):
    db.execute('''INSERT INTO graus (order_id, lens_for, eye, esf, cil, eixo, dnp, indice, lens_type, adicao)
                  VALUES (?,?,?,?,?,?,?,?,?,?)''', grau_data)
    db.commit()

def get_grau_by_id(db, order_id, grau_id):
    return db.execute('SELECT * FROM graus WHERE id = ? AND order_id = ?', (grau_id, order_id)).fetchone()

def update_grau(db, grau_id, grau_data):
    db.execute('''UPDATE graus SET lens_for=?, eye=?, esf=?, cil=?, eixo=?, dnp=?, indice=?, lens_type=?, adicao=?
                  WHERE id=?''', grau_data + (grau_id,))
    db.commit()

def delete_grau(db, order_id, grau_id):
    db.execute('DELETE FROM graus WHERE id = ? AND order_id = ?', (grau_id, order_id))
    db.commit()

def get_partial_payments(db, order_id):
    return db.execute('SELECT * FROM partial_payments WHERE order_id = ? ORDER BY payment_date DESC', (order_id,)).fetchall()

def get_total_paid(db, order_id):
    result = db.execute('SELECT COALESCE(SUM(amount), 0) as total FROM partial_payments WHERE order_id = ?', (order_id,)).fetchone()
    return result['total'] if result else 0

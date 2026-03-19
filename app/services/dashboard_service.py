"""
Dashboard Service
Provide methods to fetch metrics and statistics for the dashboard
"""
import json
from datetime import datetime

def get_dashboard_metrics(db):
    """
    Fetches total orders, revenue, pending orders, sales by month, top labs, and recent orders.
    """
    metrics = {}
    
    # Estatísticas Gerais (apenas ordens não deletadas)
    metrics['total_orders'] = db.execute("SELECT COUNT(*) FROM orders WHERE deleted_at IS NULL").fetchone()[0]
    
    # Receita Total
    revenue_query = """
        SELECT SUM(COALESCE(valor_pago, 0)) 
        FROM orders WHERE deleted_at IS NULL
    """
    metrics['total_revenue'] = db.execute(revenue_query).fetchone()[0] or 0
    
    metrics['pending_orders'] = db.execute("SELECT COUNT(*) FROM orders WHERE payment_status = 'Pendente' AND deleted_at IS NULL").fetchone()[0]
    
    # Vendas por Mês (usando exam_date como proxy)
    orders = db.execute("""
        SELECT exam_date, valor_pago FROM orders 
        WHERE exam_date IS NOT NULL AND exam_date != '' AND valor_pago > 0 AND deleted_at IS NULL
    """).fetchall()
    
    sales_by_month = {}
    for order in orders:
        try:
            date_obj = datetime.strptime(order['exam_date'], '%Y-%m-%d')
            month_key = date_obj.strftime('%Y-%m')
            val = order['valor_pago'] or 0
            sales_by_month[month_key] = sales_by_month.get(month_key, 0) + val
        except ValueError:
            continue
            
    # Ordenar por mês e pegar os últimos 6
    sorted_months = sorted(sales_by_month.keys())[-6:]
    chart_labels = [datetime.strptime(m, '%Y-%m').strftime('%b/%Y') for m in sorted_months]
    chart_data = [sales_by_month[m] for m in sorted_months]
    
    metrics['chart_labels'] = json.dumps(chart_labels)
    metrics['chart_data'] = json.dumps(chart_data)
    
    # Top Laboratórios
    metrics['top_labs'] = db.execute("""
        SELECT lab, COUNT(*) as count 
        FROM orders 
        WHERE lab IS NOT NULL AND lab != '' AND deleted_at IS NULL
        GROUP BY lab 
        ORDER BY count DESC 
        LIMIT 5
    """).fetchall()
    
    # Últimos Pedidos
    metrics['recent_orders'] = db.execute("SELECT * FROM orders WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 5").fetchall()
    
    return metrics

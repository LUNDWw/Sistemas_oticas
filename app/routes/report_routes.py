from flask import Blueprint, render_template, request, send_file
from app.models import get_db
from app.services.report_service import generate_excel_report, generate_pdf_report
from datetime import datetime

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports')
def index():
    return render_template('reports.html')

@report_bp.route('/reports/export')
def export():
    db = get_db()
    
    # Filtros
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    fmt = request.args.get('format', 'excel')
    
    sql = "SELECT * FROM orders WHERE 1=1"
    params = []
    
    if start_date:
        sql += " AND exam_date >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND exam_date <= ?"
        params.append(end_date)
    if status and status != 'all':
        sql += " AND payment_status = ?"
        params.append(status)
        
    orders = db.execute(sql, params).fetchall()
    
    if fmt == 'pdf':
        output = generate_pdf_report(orders)
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    else:
        output = generate_excel_report(orders)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'relatorio_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )

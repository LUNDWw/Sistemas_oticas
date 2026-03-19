from flask import Blueprint, render_template
from app.models import get_db
from app.services.dashboard_service import get_dashboard_metrics

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    db = get_db()
    metrics = get_dashboard_metrics(db)
    
    return render_template('dashboard.html', 
                         total_orders=metrics['total_orders'],
                         total_revenue=metrics['total_revenue'],
                         pending_orders=metrics['pending_orders'],
                         chart_labels=metrics['chart_labels'],
                         chart_data=metrics['chart_data'],
                         top_labs=metrics['top_labs'],
                         recent_orders=metrics['recent_orders'])


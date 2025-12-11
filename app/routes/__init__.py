from .main_routes import main_bp
from .order_routes import order_bp
from .dashboard_routes import dashboard_bp
from .report_routes import report_bp
from .print_routes import print_bp
from .cashflow_routes import cashflow_bp

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(print_bp)
    app.register_blueprint(cashflow_bp)

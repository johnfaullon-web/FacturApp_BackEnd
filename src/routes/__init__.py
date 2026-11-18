from src.routes.v1.products_routes import products_bp
from src.routes.v1.categories_routes import categories_bp
from src.routes.v1.auth_routes import auth_bp
from src.routes.v1.users_routes import users_bp
from src.routes.v1.clients_routes import clients_bp
from src.routes.v1.invoices_routes import invoices_bp
from src.routes.v1.invoice_details_routes import invoice_details_bp


def register_routes(app):
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(invoice_details_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
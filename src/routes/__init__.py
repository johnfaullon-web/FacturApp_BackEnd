from src.routes.v1.products_routes import products_bp
from src.routes.v1.categories_routes import categories_bp
from src.routes.v1.auth_routes import auth_bp
from src.routes.v1.users_routes import users_bp
from src.routes.v1.clients_routes import clients_bp


def register_routes(app):
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
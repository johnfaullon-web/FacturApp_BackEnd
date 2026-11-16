from flask import Flask
from src.models import Base, engine
from src.models.categories import Categories
from src.models.products import Products
from src.models.users import Users
from src.models.clients import Clients

from src.routes import register_routes


app = Flask(__name__)

Base.metadata.create_all(engine)

register_routes(app)  # Register the routes with the Flask app

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'facturapp-adso-25t4-dev-secret-key-change-me'



@app.route('/')
def health():
    return {
        'success': True,
        'message': 'API is running'
    }


if __name__ == '__main__':
    app.run(debug=True)
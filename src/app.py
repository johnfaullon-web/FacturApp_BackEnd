from flask import Flask
from src.models import Base, engine
from src.models.categories import Categories
from src.models.products import Products
from src.routes.products_routes import products_bp

Base.metadata.create_all(engine)

app = Flask(__name__)

app.register_blueprint(products_bp)

@app.route("/")
def hello_word():
    return "Hello Word!"

if __name__ == "__main__":
    app.run(debug=True)
    

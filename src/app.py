from flask import Flask 
from src.models import Base, engine
from src.models.categories import Categories
from src.models.products import Products

Base.metadata.create_all(engine)


app = Flask(__name__)

@app.route("/")
def hello_word():
    return "Hello Word!"

if __name__ == "__main__":
    app.run(debug=True)
    

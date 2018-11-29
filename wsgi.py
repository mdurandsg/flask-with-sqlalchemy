from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/products/<int:id>')
def get(id):
    product_by_id = db.session.query(Product).get(id)
    return products_schema.jsonify(product_by_id)

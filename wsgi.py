from flask import Flask, request, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

admin = Admin(app, name="Back-office", template_mode="bootstrap3")
admin.add_view(ModelView(Product, db.session))

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = db.session.query(Product).all()
        return render_template('home.html', products=products)
    else:
        new_product = Product()
        new_product.name = request.json["name"]
        new_product.description = request.json["description"]
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product)



@app.route('/products/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def product_by_id(id):
    if request.method == 'GET':
        product_by_id = db.session.query(Product).get(id)
        #print(product_by_id)
        return render_template('product.html', product=product_by_id)
    elif request.method == 'DELETE':
        product_by_id = db.session.query(Product).get(id)
        db.session.delete(product_by_id)
        db.session.commit()
        return product_schema.jsonify(product_by_id)
    else:
        product_by_id = db.session.query(Product).get(id)
        dic = request.get_json()
        if "name" in dic:
            product_by_id.name = request.json["name"]
        if "description" in dic:
            product_by_id.description = request.json["description"]
        db.session.commit()
        return product_schema.jsonify(product_by_id)

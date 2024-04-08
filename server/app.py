#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.get("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get('/restaurants')
def get_all_restaurants():
    return [restaurant.to_dict(rules=('-restaurant_pizzas',)) for restaurant in Restaurant.query.all()]

@app.get('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if restaurant:
        return make_response(restaurant.to_dict(), 200)
    else:
        return make_response({'error': 'Restaurant not found'}, 404)

@app.delete('/restaurants/<int:id>')
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({'error': f'No restaurant id {id} exists.'}, 404)
    else:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({}, 204)

@app.get('/pizzas')
def get_all_pizzas():
    return make_response(
        [pizza.to_dict(rules=('-restaurant_pizzas',)) for pizza in Pizza.query.all()],
        200
    )

@app.post('/restaurant_pizzas')
def post_restaurant_pizza():
    json_data = request.get_json()
    try:
        new_restaurant_pizza = RestaurantPizza(price = json_data['price'],
                                               pizza_id = json_data['pizza_id'],
                                               restaurant_id = json_data['restaurant_id'])
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return make_response(new_restaurant_pizza.to_dict(), 201)
    except ValueError as e:
        return make_response({'errors': ['validation errors']}, 400)
        # return make_response( str(e), 400)

if __name__ == "__main__":
    app.run(port=5555, debug=True)

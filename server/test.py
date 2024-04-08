from models import Restaurant, Pizza, RestaurantPizza
from pprint import pprint
from app import app

with app.app_context():
    p1 = Restaurant.query.first()
    print(p1)
    pprint(p1.to_dict())

    test_price = RestaurantPizza(price = 5, pizza_id = 1, restaurant_id = 1)
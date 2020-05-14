from app import db
from products import Product


db.drop_all()
db.create_all()

milch = Product(name='Milch', amount=5)
burger = Product(name='Burger', amount=50)

db.session.add(milch)
db.session.add(burger)
db.session.commit()


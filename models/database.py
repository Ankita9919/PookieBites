from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(20))

    rating = db.Column(db.Float, default=4.5)
    delivery_time = db.Column(db.String(30), default="30-40 min")
    delivery_fee = db.Column(db.Float, default=40.0)

    is_verified = db.Column(db.Boolean, default=False)
    is_open = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)

    restaurant = db.relationship("Restaurant")
    category = db.relationship("Category")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id"),
        nullable=True
    )

    customer_name = db.Column(
        db.String(150),
        nullable=False,
        default="Pookie User"
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    address = db.Column(
        db.String(500),
        nullable=True
    )

    payment_method = db.Column(
        db.String(50),
        default="Cash on Delivery"
    )

    payment_status = db.Column(
        db.String(50),
        default="Pending"
    )

    subtotal = db.Column(
        db.Float,
        default=0
    )

    delivery_charge = db.Column(
        db.Float,
        default=0
    )

    fast_delivery_charge = db.Column(
        db.Float,
        default=0
    )

    packing_charge = db.Column(
        db.Float,
        default=0
    )

    discount = db.Column(
        db.Float,
        default=0
    )

    total = db.Column(
        db.Float,
        default=0
    )

    delivery_type = db.Column(
        db.String(50),
        default="Normal"
    )

    estimated_delivery = db.Column(
        db.String(50),
        default="40-55 minutes"
    )

    status = db.Column(
        db.String(50),
        default="Order Placed"
    )

    order_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref("orders", lazy=True)
    )

    restaurant = db.relationship(
        "Restaurant"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey("menu_items.id")
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    order = db.relationship(
        "Order",
        backref=db.backref("items", lazy=True)
    )

    menu_item = db.relationship(
        "MenuItem"
    )


class DeliveryPartner(db.Model):
    __tablename__ = "delivery_partners"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    vehicle_number = db.Column(
        db.String(50)
    )

    is_available = db.Column(
        db.Boolean,
        default=True
    )

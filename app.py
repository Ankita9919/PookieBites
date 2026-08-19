from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
import random
import os
import requests
import os
import requests
import os
import requests

app = Flask(__name__)
app.secret_key = "pookiebites-secret-key-2026"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foodieexpress.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from models.database import db, User, Restaurant, Category, MenuItem, Order, OrderItem, DeliveryPartner
db.init_app(app)


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper

def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart
    session.modified = True
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
import random
import os
import requests
import os
import requests
import os
import requests

app = Flask(__name__)
app.secret_key = "pookiebites-secret-key-2026"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foodieexpress.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from models.database import db, User, Restaurant, Category, MenuItem, Order, OrderItem, DeliveryPartner
db.init_app(app)


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper

def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart
    session.modified = True
def cart_items():

    cart = get_cart()
    result = []
    subtotal = 0

    for item_id, quantity in cart.items():

        item = db.session.get(MenuItem, int(item_id))

        if item:

            quantity = int(quantity)
            item_total = item.price * quantity

            result.append({
                "item": item,
                "quantity": quantity,
                "total": item_total,
                "subtotal": item_total
            })

            subtotal += item_total

    return result, subtotal

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():

    menu_items = MenuItem.query.order_by(
        MenuItem.id
    ).all()

    cart_count = sum(
        int(x) for x in get_cart().values()
    )

    return render_template(
        "menu.html",
        menu_items=menu_items,
        cart_count=cart_count
    )


@app.route("/add-to-cart/<int:item_id>")
def add_to_cart(item_id):

    item = db.session.get(MenuItem, item_id)

    if not item:

        flash("Food item not found.")

        return redirect(url_for("menu"))

    cart = get_cart()
    key = str(item_id)

    cart[key] = int(
        cart.get(key, 0)
    ) + 1

    save_cart(cart)

    flash(
        f"{item.name} added to your cart ??"
    )

    return redirect(
        request.referrer or url_for("menu")
    )


@app.route("/cart")
def cart():

    items, subtotal = cart_items()

    delivery_charge = (
        0 if subtotal >= 499
        else 49 if subtotal > 0
        else 0
    )

    cart_count = sum(
        int(x) for x in get_cart().values()
    )

    total = subtotal + delivery_charge

    return render_template(
        "cart.html",
        cart_items=items,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        total=total,
        cart_count=cart_count
    )


@app.route("/cart/increase/<int:item_id>")
def increase_quantity(item_id):

    cart = get_cart()
    key = str(item_id)

    if key in cart:
        cart[key] = int(cart[key]) + 1

    save_cart(cart)

    return redirect(url_for("cart"))


@app.route("/cart/decrease/<int:item_id>")
def decrease_quantity(item_id):

    cart = get_cart()
    key = str(item_id)

    if key in cart:

        cart[key] = int(cart[key]) - 1

        if cart[key] <= 0:
            del cart[key]

    save_cart(cart)

    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:item_id>")
def remove_from_cart(item_id):

    cart = get_cart()
    key = str(item_id)

    if key in cart:
        del cart[key]

    save_cart(cart)

    return redirect(url_for("cart"))


@app.route("/cart/clear")
def clear_cart():

    session["cart"] = {}
    session.modified = True

    return redirect(url_for("cart"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        phone = request.form.get(
            "phone",
            ""
        ).strip().replace(" ", "")

        if len(phone) != 10 or not phone.isdigit():

            flash(
                "Please enter a valid 10-digit mobile number."
            )

            return redirect(url_for("login"))

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        session["otp"] = otp
        session["otp_phone"] = phone
        session["demo_otp"] = otp

        authkey = os.getenv("MSG91_AUTHKEY")

        if not authkey:
            flash("MSG91 API key is missing.")
            return redirect(url_for("login"))

        try:

            response = requests.get(
                "https://api.msg91.com/api/sendotp.php",
                params={
                    "authkey": authkey,
                    "mobile": phone,
                    "otp": otp,
                    "otp_length": 6,
                    "otp_expiry": 5
                },
                timeout=20
            )

            print("MSG91 STATUS:", response.status_code)
            print("MSG91 RESPONSE:", response.text)

            if response.status_code != 200:
                flash("Unable to send OTP. Please try again.")
                return redirect(url_for("login"))

        except Exception as e:

            print("MSG91 ERROR:", e)
            flash("OTP service is temporarily unavailable.")
            return redirect(url_for("login"))

        user = User.query.filter_by(
            phone=phone
        ).first()

        if not user:

            user = User(
                phone=phone,
                name="Pookie User",
                email=phone + "@pookiebites.local",
                password="otp-login"
            )

            db.session.add(user)
            db.session.commit()

        return redirect(
            url_for("verify_otp")
        )

    return render_template("login.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if "otp" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        entered = request.form.get(
            "otp",
            ""
        ).strip()

        if entered == session.get("otp"):

            user = User.query.filter_by(
                phone=session.get("otp_phone")
            ).first()

            if user:

                session["user_id"] = user.id
                session["user_name"] = user.name
                session["user_phone"] = user.phone

            session.pop("otp", None)

            return redirect(url_for("menu"))

        flash("Wrong OTP. Please try again.")

    return render_template(
        "verify_otp.html",
        demo_otp=session.get("demo_otp")
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():

    items, subtotal = cart_items()

    if not items:
        return redirect(url_for("cart"))

    if request.method == "POST":

        customer_name = request.form.get(
            "customer_name",
            session.get("user_name", "Pookie User")
        )

        phone = request.form.get(
            "phone",
            session.get("user_phone", "")
        )

        address = request.form.get(
            "address",
            ""
        )

        payment_method = request.form.get(
            "payment_method",
            "Cash on Delivery"
        )

        delivery_type = request.form.get(
            "delivery_type",
            "Normal"
        )

        special_packing = request.form.get(
            "special_packing"
        )

        delivery_charge = (
            0 if subtotal >= 499 else 49
        )

        fast_delivery_charge = (
            79 if delivery_type == "Fast" else 0
        )

        packing_charge = (
            29 if special_packing else 0
        )

        discount = 0

        if subtotal >= 999:

            discount = min(
                200,
                round(subtotal * 0.10)
            )

        total = (
            subtotal
            + delivery_charge
            + fast_delivery_charge
            + packing_charge
            - discount
        )

        estimated_delivery = "25-35 minutes" if delivery_type == "Fast" else "40-55 minutes"

        order = Order(
            user_id=session.get("user_id"),
            customer_name=customer_name,
            phone=phone,
            address=address,
            payment_method=payment_method,
            payment_status="Pending",
            subtotal=subtotal,
            delivery_charge=delivery_charge,
            fast_delivery_charge=fast_delivery_charge,
            packing_charge=packing_charge,
            discount=discount,
            total=total,
            delivery_type=delivery_type,
            estimated_delivery=estimated_delivery
        )

        db.session.add(order)
        db.session.commit()

        session["cart"] = {}
        session.modified = True

        return redirect(
            url_for(
                "order_success",
                order_id=order.id
            )
        )

    delivery_charge = (
        0 if subtotal >= 499 else 49
    )

    gift = subtotal >= 999

    return render_template(
        "checkout.html",
        cart_items=items,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        gift=gift
    )


@app.route("/order-success/<int:order_id>")
@login_required
def order_success(order_id):

    order = db.session.get(
        Order,
        order_id
    )

    if not order:
        return redirect(url_for("menu"))

    gift = order.subtotal >= 999

    return render_template(
        "order_success.html",
        order=order,
        gift=gift
    )


@app.route("/orders")
@login_required
def orders():

    user_orders = Order.query.filter_by(
        user_id=session.get("user_id")
    ).order_by(
        Order.order_date.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)




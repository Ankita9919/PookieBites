from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "foodieexpress_secret_key"


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- MENU ----------------

@app.route("/menu")
def menu():
    return render_template("menu.html")


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        session["user"] = {
            "name": name,
            "email": email,
            "password": password
        }

        return redirect(url_for("menu"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = session.get("user")

        if user and user["email"] == email and user["password"] == password:

            session["logged_in"] = True

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session["logged_in"] = False

    return redirect(url_for("home"))


# ---------------- CART ----------------

@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    total = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# ---------------- ADD TO CART ----------------

@app.route("/add_to_cart/<name>/<int:price>")
def add_to_cart(name, price):

    cart_items = session.get("cart", [])

    for item in cart_items:

        if item["name"] == name:

            item["quantity"] += 1

            break

    else:

        cart_items.append({
            "name": name,
            "price": price,
            "quantity": 1
        })

    session["cart"] = cart_items

    return redirect(url_for("cart"))


# ---------------- REMOVE FROM CART ----------------

@app.route("/remove_from_cart/<name>")
def remove_from_cart(name):

    cart_items = session.get("cart", [])

    cart_items = [
        item for item in cart_items
        if item["name"] != name
    ]

    session["cart"] = cart_items

    return redirect(url_for("cart"))


# ---------------- CHECKOUT ----------------

@app.route("/checkout")
def checkout():

    cart_items = session.get("cart", [])

    total = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )


# ---------------- PLACE ORDER ----------------

@app.route("/place_order", methods=["POST"])
def place_order():

    cart_items = session.get("cart", [])

    if not cart_items:

        return redirect(url_for("menu"))

    customer_name = request.form.get("name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    payment = request.form.get("payment")

    total = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    session["last_order"] = {
        "id": "FE-" + str(int(__import__("time").time())),
        "status": "Confirmed",
        "customer_name": customer_name,
        "address": address,
        "phone": phone,
        "payment": payment,
        "items": cart_items,
        "total": total
    }

    session["cart"] = []

    return render_template(
        "order_success.html",
        order=session["last_order"]
    )


# ---------------- RUN APP ----------------


# ---------------- ORDERS ----------------

@app.route("/orders")
def orders():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    order = session.get("last_order")

    return render_template(
        "orders.html",
        order=order
    )


@app.route("/increase_quantity/<name>")
def increase_quantity(name):
    cart = session.get("cart", [])

    for item in cart:
        if item["name"] == name:
            item["quantity"] += 1
            break

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/decrease_quantity/<name>")
def decrease_quantity(name):
    cart = session.get("cart", [])

    for item in cart:
        if item["name"] == name:
            if item["quantity"] > 1:
                item["quantity"] -= 1
            else:
                cart.remove(item)
            break

    session["cart"] = cart
    return redirect(url_for("cart"))
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, session, redirect, url_for, request
import json

app = Flask(__name__)
app.secret_key = "foodieexpress_secret_key"

OWNER_USERNAME = "admin"
OWNER_PASSWORD = "admin123"

FOODS_FILE = "foods.json"


def load_foods():
    with open(FOODS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_foods(foods):
    with open(FOODS_FILE, "w", encoding="utf-8") as f:
        json.dump(foods, f, indent=4, ensure_ascii=False)


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# MENU
@app.route("/menu")
def menu():
    foods = load_foods()
    return render_template("menu.html", foods=foods)


# CUSTOMER SIGNUP
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


# CUSTOMER LOGIN
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


@app.route("/logout")
def logout():

    session["logged_in"] = False

    return redirect(url_for("home"))


# ---------------- OWNER LOGIN ----------------

@app.route("/owner/login", methods=["GET", "POST"])
def owner_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == OWNER_USERNAME and password == OWNER_PASSWORD:

            session["owner_logged_in"] = True

            return redirect(url_for("owner_dashboard"))

        return render_template(
            "owner_login.html",
            error="Wrong owner username or password."
        )

    return render_template("owner_login.html")


# ---------------- OWNER DASHBOARD ----------------

@app.route("/owner/dashboard")
def owner_dashboard():

    if not session.get("owner_logged_in"):
        return redirect(url_for("owner_login"))

    foods = load_foods()

    return render_template(
        "owner_dashboard.html",
        foods=foods
    )


# ---------------- ADD FOOD ----------------

@app.route("/owner/add-food", methods=["GET", "POST"])
def add_food():

    if not session.get("owner_logged_in"):
        return redirect(url_for("owner_login"))

    if request.method == "POST":

        foods = load_foods()

        new_id = max([food["id"] for food in foods], default=0) + 1

        food = {
            "id": new_id,
            "name": request.form.get("name"),
            "category": request.form.get("category"),
            "description": request.form.get("description"),
            "price": int(request.form.get("price")),
            "icon": request.form.get("icon") or "🍽️"
        }

        foods.append(food)

        save_foods(foods)

        return redirect(url_for("owner_dashboard"))

    return render_template("owner_edit.html", food=None, title="Add New Food")


# ---------------- EDIT FOOD ----------------

@app.route("/owner/edit-food/<int:food_id>", methods=["GET", "POST"])
def edit_food(food_id):

    if not session.get("owner_logged_in"):
        return redirect(url_for("owner_login"))

    foods = load_foods()

    food = next(
        (f for f in foods if f["id"] == food_id),
        None
    )

    if food is None:
        return "Food not found", 404

    if request.method == "POST":

        food["name"] = request.form.get("name")
        food["category"] = request.form.get("category")
        food["description"] = request.form.get("description")
        food["price"] = int(request.form.get("price"))
        food["icon"] = request.form.get("icon") or food["icon"]

        save_foods(foods)

        return redirect(url_for("owner_dashboard"))

    return render_template(
        "owner_edit.html",
        food=food,
        title="Edit Food"
    )


# ---------------- DELETE FOOD ----------------

@app.route("/owner/delete-food/<int:food_id>", methods=["POST"])
def delete_food(food_id):

    if not session.get("owner_logged_in"):
        return redirect(url_for("owner_login"))

    foods = load_foods()

    foods = [
        food for food in foods
        if food["id"] != food_id
    ]

    save_foods(foods)

    return redirect(url_for("owner_dashboard"))


# ---------------- OWNER LOGOUT ----------------

@app.route("/owner/logout")
def owner_logout():

    session["owner_logged_in"] = False

    return redirect(url_for("owner_login"))


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


@app.route("/remove_from_cart/<name>")
def remove_from_cart(name):

    cart_items = session.get("cart", [])

    cart_items = [
        item for item in cart_items
        if item["name"] != name
    ]

    session["cart"] = cart_items

    return redirect(url_for("cart"))


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


@app.route("/orders")
def orders():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    order = session.get("last_order")

    return render_template(
        "orders.html",
        order=order
    )


if __name__ == "__main__":
    app.run(debug=True)

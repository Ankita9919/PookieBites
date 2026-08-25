from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "foodieexpress_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart_items)

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


if __name__ == "__main__":
    app.run(debug=True)

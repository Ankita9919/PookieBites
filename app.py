import resend
from flask import Flask, render_template, session, redirect, url_for, request
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os
from models.database import db, User, Order, OrderItem

app = Flask(__name__)
load_dotenv()
app.secret_key = "foodieexpress_secret_key"
load_dotenv(override=True)
resend.api_key = os.getenv("RESEND_API_KEY")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/foodieexpress.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.instance_path = "/tmp"
db.init_app(app)

OWNER_USERNAME = "admin"
OWNER_PASSWORD = "admin123"

FOODS_FILE = "foods.json"

FOOD_IMAGES = {
    "Chicken Pizza": "chicken_pizza.jpg",
    "Margherita Pizza": "margherita_pizza.jpg",
    "Chicken Burger": "chicken_burger.jpg",
    "Chicken Burger Combo": "chicken_burger_combo.jpg",
    "Chicken Biryani": "chicken_biryani.jpg",
    "Mutton Biryani": "mutton_biryani.jpg",
    "Egg Biryani": "egg_biryani.jpg",
    "Veg Biryani": "veg_biryani.jpg",
    "Kolkata Chicken Biryani": "kolkata_chicken_biryani.jpg",
    "Kolkata Mutton Biryani": "kolkata_mutton_biryani.jpg",
    "Hyderabadi Chicken Biryani": "hyderabadi_chicken_biryani.jpg",
    "Biryani Combo": "biryani_combo.jpg",
    "Chicken Noodles": "chicken_hakka_noodles.jpg",
    "Hakka Noodles": "hakka_noodles.jpg",
    "Egg Noodles": "egg_noodles.jpg",
    "Schezwan Chicken Noodles": "schezwan_chicken_noodles.jpg",
    "Schezwan Veg Noodles": "schezwan_veg_noodles.jpg",
    "Chilli Garlic Noodles": "chilli_garlic_noodles.jpg",
    "Veg Hakka Noodles": "veg_hakka_noodles.jpg",
    "Noodles Combo": "noodles_combo.jpg",
    "Chicken Momos": "chicken_momos.jpg",
    "Momo Combo": "momo_combo.jpg",
    "Chocolate Cake": "chocolate_cake.jpg",
    "Brownie": "brownie.jpg",
    "Cheesecake": "cheesecake.jpg",
    "Chocolate Mousse": "chocolate_mousse.jpg",
    "Rosogolla": "rosogolla.jpg",
    "Sandesh": "sandesh.jpg",
    "Mishti Doi": "mishti_doi.jpg",
    "Rasmalai": "rasmalai.jpg",
    "Cham Cham": "cham_cham.jpg",
    "Kheer Kadam": "kheer_kadam.jpg",
    "Nolen Gur Sandesh": "nolen_gur_sandesh.jpg",
    "Gulab Jamun": "gulab_jamun.jpg",
    "Mango Ice Cream": "mango_ice_cream.jpg",
    "Chocolate Ice Cream": "chocolate_ice_cream.jpg",
    "Vanilla Ice Cream": "vanilla_ice_cream.jpg",
    "Butterscotch Ice Cream": "butterscotch_ice_cream.jpg",
    "Strawberry Ice Cream": "strawberry_ice_cream.jpg",
    "Kesar Pista Ice Cream": "kesar_pista_ice_cream.jpg",
    "Mango Juice": "mango_juice.jpg",
    "Coca Cola": "coca_cola.jpg",
    "Pepsi": "pepsi.jpg",
    "Sprite": "sprite.jpg",
    "Chicken Thali": "chicken_thali.jpg",
    "Mutton Thali": "mutton_thali.jpg",
    "Bengali Fish Thali": "bengali_fish_thali.jpg",
    "Bengali Veg Thali": "bengali_veg_thali.jpg",
    "Special Veg Thali": "special_veg_thali.jpg",
    "Luchi Aloor Dom": "luchi_aloor_dom.jpg",
    "Kosha Mangsho": "kosha_mangsho.jpg",
    "Shorshe Ilish": "shorshe_ilish.jpg",
    "Bhetki Paturi": "bhetki_paturi.jpg",
    "Chingri Malai Curry": "chingri_malai_curry.jpg",
    "Aloo Posto": "aloo_posto.jpg",
    "Dhokar Dalna": "dhokar_dalna.jpg",
    "Doi Katla": "doi_katla.jpg"
}


def get_food_image(food_name):

    image_map = {

        "Chicken Pizza": "margherita_pizza.jpg",

        "Chicken Burger": "chicken_burger.jpg",
        "Chicken Burger Combo": "chicken_burger_combo.jpg",

        "Chicken Biryani": "chicken_biryani.jpg",
        "Mutton Biryani": "mutton_biryani.jpg",
        "Egg Biryani": "egg_biryani.jpg",
        "Veg Biryani": "veg_biryani.jpg",
        "Hyderabadi Chicken Biryani": "hyderabadi_chicken_biryani.jpg",
        "Kolkata Chicken Biryani": "kolkata_chicken_biryani.jpg",
        "Kolkata Mutton Biryani": "kolkata_mutton_biryani.jpg",
        "Biryani Combo": "biryani_combo.jpg",

        "Chicken Noodles": "chicken_hakka_noodles.jpg",
        "Chicken Hakka Noodles": "chicken_hakka_noodles.jpg",
        "Hakka Noodles": "hakka_noodles.jpg",
        "Egg Noodles": "egg_noodles.jpg",
        "Veg Hakka Noodles": "veg_hakka_noodles.jpg",
        "Chilli Garlic Noodles": "chilli_garlic_noodles.jpg",
        "Schezwan Chicken Noodles": "schezwan_chicken_noodles.jpg",
        "Schezwan Veg Noodles": "schezwan_veg_noodles.jpg",
        "Noodles Combo": "noodles_combo.jpg",

        "Chicken Momos": "chicken_momos.jpg",
        "Momo Combo": "momo_combo.jpg",

        "Chicken Thali": "chicken_thali.jpg",
        "Mutton Thali": "mutton_thali.jpg",
        "Bengali Fish Thali": "bengali_fish_thali.jpg",
        "Bengali Veg Thali": "bengali_veg_thali.jpg",
        "Special Veg Thali": "special_veg_thali.jpg",

        "Aloo Posto": "aloo_posto.jpg",
        "Bengali Fish Thali": "bengali_fish_thali.jpg",
        "Bengali Veg Thali": "bengali_veg_thali.jpg",
        "Bhetki Paturi": "bhetki_paturi.jpg",
        "Chingri Malai Curry": "chingri_malai_curry.jpg",
        "Dhokar Dalna": "dhokar_dalna.jpg",
        "Doi Katla": "doi_katla.jpg",
        "Kosha Mangsho": "kosha_mangsho.jpg",
        "Luchi Aloor Dom": "luchi_aloor_dom.jpg",
        "Shorshe Ilish": "shorshe_ilish.jpg",

        "Rosogolla": "rosogolla.jpg",
        "Sandesh": "sandesh.jpg",
        "Nolen Gur Sandesh": "nolen_gur_sandesh.jpg",
        "Cham Cham": "cham_cham.jpg",
        "Kheer Kadam": "kheer_kadam.jpg",
        "Mishti Doi": "mishti_doi.jpg",
        "Gulab Jamun": "gulab_jamun.jpg",
        "Rasmalai": "rasmalai.jpg",

        "Chocolate Cake": "chocolate_cake.jpg",
        "Cheesecake": "cheesecake.jpg",
        "Brownie": "brownie.jpg",
        "Chocolate Mousse": "chocolate_mousse.jpg",

        "Chocolate Ice Cream": "chocolate_ice_cream.jpg",
        "Vanilla Ice Cream": "vanilla_ice_cream.jpg",
        "Mango Ice Cream": "mango_ice_cream.jpg",
        "Strawberry Ice Cream": "strawberry_ice_cream.jpg",
        "Butterscotch Ice Cream": "butterscotch_ice_cream.jpg",
        "Kesar Pista Ice Cream": "kesar_pista_ice_cream.jpg",

        "Mango Juice": "mango_juice.jpg",
        "Mango Lassi": "mango_lassi.jpg",
        "Cold Coffee": "cold_coffee.jpg",
        "Fresh Lime Soda": "fresh_lime_soda.jpg",
        "Coca Cola": "coca_cola.jpg",
        "Pepsi": "pepsi.jpg",
        "Sprite": "sprite.jpg",

        "Family Feast Combo": "family_feast_combo.jpg"
    }

    return image_map.get(food_name, "default_food.jpg")

def load_foods():
    with open(FOODS_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_foods(foods):
    with open(FOODS_FILE, "w", encoding="utf-8-sig") as f:
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

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template(
                "signup.html",
                error="Please fill in all fields."
            )

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template(
                "signup.html",
                error="Email already registered. Please login."
            )

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")


# CUSTOMER LOGIN - EMAIL OTP
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()

        if not email:
            return render_template("login.html",
                                   error="Please enter your email address.")

        if "@" not in email or "." not in email.split("@")[-1]:
            return render_template("login.html",
                                   error="Please enter a valid email address.")

        user = User.query.filter_by(email=email).first()

        otp = str(random.randint(100000, 999999))

        session["otp"] = otp
        session["otp_email"] = email
        session["otp_expiry"] = (
            datetime.utcnow() + timedelta(minutes=5)
        ).timestamp()

        if user:
            session["otp_name"] = user.name
            display_name = user.name
        else:
            session["otp_name"] = "there"
            display_name = "there"

        print("NEW OTP GENERATED:", otp)
        print("OTP EMAIL:", email)

        try:
            response = resend.Emails.send({
                "from": "PookieBites <onboarding@resend.dev>",
                "to": [email],
                "subject": "Your PookieBites Login OTP",
                "html": f"""
                <div style="font-family:Arial,sans-serif;
                            max-width:500px;
                            margin:auto;
                            padding:30px;
                            background:#fff5f9;
                            text-align:center;
                            border-radius:20px;">

                    <h1 style="color:#d94f7d;">PookieBites</h1>

                    <p style="font-size:18px;">
                        Hello {display_name}!
                    </p>

                    <p>Your login OTP is:</p>

                    <div style="font-size:36px;
                                font-weight:bold;
                                letter-spacing:8px;
                                color:#d94f7d;
                                margin:25px 0;">
                        {otp}
                    </div>

                    <p>This OTP is valid for <b>5 minutes</b>.</p>

                    <p style="color:#888;">
                        Please do not share this OTP with anyone.
                    </p>

                    <p>PookieBites Team</p>

                </div>
                """
            })

            print("RESEND OTP SUCCESS:", response)

            return redirect(url_for("verify_otp"))

        except Exception as e:
            print("RESEND OTP ERROR:", repr(e))

            session.pop("otp", None)
            session.pop("otp_email", None)
            session.pop("otp_expiry", None)
            session.pop("otp_name", None)

            return render_template(
                "login.html",
                error="Unable to send OTP. Please try again."
            )

    return render_template("login.html")


@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if "otp" not in session or "otp_email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        entered_otp = request.form.get("otp", "").strip()

        saved_otp = session.get("otp")
        otp_email = session.get("otp_email")
        expiry = session.get("otp_expiry", 0)

        if datetime.utcnow().timestamp() > expiry:

            session.pop("otp", None)
            session.pop("otp_email", None)
            session.pop("otp_expiry", None)
            session.pop("otp_name", None)

            return render_template(
                "verify_otp.html",
                error="OTP expired. Please request a new OTP."
            )

        if entered_otp != saved_otp:

            return render_template(
                "verify_otp.html",
                error="Invalid OTP. Please try again."
            )

        # Existing account
        user = User.query.filter_by(email=otp_email).first()

        if user:

            session["user_id"] = user.id
            session["logged_in"] = True

            session["user"] = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }

        else:

            # Email is not registered yet.
            # Allow OTP verification but don't pretend an account exists.
            session["logged_in"] = True

            session["user"] = {
                "id": None,
                "name": session.get("otp_name", "Guest"),
                "email": otp_email
            }

        # Remove OTP after successful verification
        session.pop("otp", None)
        session.pop("otp_email", None)
        session.pop("otp_expiry", None)
        session.pop("otp_name", None)

        return redirect(url_for("home"))

    return render_template("verify_otp.html")

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

    return render_template("owner_dashboard.html", foods=foods, get_food_image=get_food_image)


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
            "icon": request.form.get("icon") or "ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â½ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¯ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â"
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

    subtotal = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    if subtotal >= 399:
        delivery_charge = 0
    else:
        delivery_charge = 40

    packing_charge = 0

    total = subtotal + delivery_charge + packing_charge

    return render_template(
        "cart.html",
        cart_items=cart_items,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        packing_charge=packing_charge,
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


@app.route("/reset_first_order")
def reset_first_order():
    session.pop("has_ordered_before", None)
    session.pop("tic_tac_toe_won", None)
    return "?? First-order status reset! Go back to checkout."

@app.route("/checkout")
def checkout():

    cart_items = session.get("cart", [])

    if not cart_items:
        return redirect(url_for("menu"))

    subtotal = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    # Logged-in user / first-order check
    user = None
    if session.get("user_id"):
        user = User.query.get(session.get("user_id"))

    is_first_order = not session.get("has_ordered_before", False)

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=subtotal,
        subtotal=subtotal,
        is_first_order=is_first_order,
        user=user
    )


@app.route("/place_order", methods=["POST"])
def place_order():

    cart_items = session.get("cart", [])

    if not cart_items:
        return redirect(url_for("menu"))

    customer_name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    phone = request.form.get("phone", "").strip()
    payment = request.form.get("payment", "").strip()

    delivery_type = request.form.get(
        "delivery_type",
        "Normal Delivery"
    )

    packing = request.form.get(
        "packing",
        "Normal Packing"
    )

    birthday = request.form.get("birthday", "").strip()
    mystery_gift = request.form.get("mystery_gift", "").strip()

    subtotal = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    # -----------------------------
    # DELIVERY CHARGE
    # -----------------------------

    if delivery_type == "Fast Delivery":
        delivery_charge = 40
    elif subtotal >= 399:
        delivery_charge = 0
    else:
        delivery_charge = 40

    # -----------------------------
    # PACKING CHARGE
    # -----------------------------

    if packing == "Cute Gift Packing":
        packing_charge = 30
    else:
        packing_charge = 0

    # -----------------------------
    # FIRST ORDER DISCOUNT
    # -----------------------------

    is_first_order = not session.get(
        "has_ordered_before",
        False
    )

    first_order_discount = 0

    if is_first_order:
        first_order_discount = min(
            round(subtotal * 0.10),
            100
        )

    # -----------------------------
    # ORDER VALUE OFFERS
    # -----------------------------

    order_discount = 0

    if subtotal >= 999:
        order_discount = 100

    elif subtotal >= 799:
        order_discount = 70

    elif subtotal >= 599:
        order_discount = 50

    elif subtotal >= 399:
        order_discount = 30

    # -----------------------------
    # BIRTHDAY OFFER
    # -----------------------------

    birthday_discount = 0

    if birthday:
        try:
            birthday_date = datetime.strptime(
                birthday,
                "%Y-%m-%d"
            )

            today = datetime.now()

            if (
                birthday_date.month == today.month
                and birthday_date.day == today.day
            ):
                birthday_discount = 50

        except ValueError:
            birthday_discount = 0

    # -----------------------------
    # TIC TAC TOE REWARD
    # -----------------------------

    game_discount = 0

    try:
        game_discount = int(request.form.get("game_discount", 0))
    except (ValueError, TypeError):
        game_discount = 0

    game_discount = min(max(game_discount, 0), 20)

    # -----------------------------
    # PAYMENT OFFER
    # -----------------------------

    payment_discount = 0

    if subtotal >= 799 and payment == "UPI":
        payment_discount = 30

    if subtotal >= 999 and payment == "UPI":
        payment_discount = 60

    # -----------------------------
    # COUPON DISCOUNT
    # -----------------------------

    coupon_code = request.form.get("coupon_code", "").strip().upper()
    coupon_discount = 0

    if coupon_code == "POOKIE10":
        coupon_discount = 10

    elif coupon_code == "SWEET20":
        coupon_discount = 20

    elif coupon_code == "WELCOME50" and is_first_order:
        coupon_discount = 50

    # Coupon cannot reduce food subtotal below zero
    coupon_discount = min(coupon_discount, subtotal)

    # -----------------------------
    # TOTAL
    # -----------------------------

    total_discount = (
        first_order_discount
        + order_discount
        + birthday_discount
        + game_discount
        + payment_discount
        + coupon_discount
    )

    discount_limit = subtotal

    total_discount = min(
        total_discount,
        discount_limit
    )

    final_total = (
        subtotal
        + delivery_charge
        + packing_charge
        - total_discount
    )

    final_total = max(final_total, 0)

    order_id = "FE-" + str(
        int(__import__("time").time())
    )

    session["last_order"] = {
        "id": order_id,
        "status": "Confirmed",
        "customer_name": customer_name,
        "address": address,
        "phone": phone,
        "payment": payment,
        "birthday": birthday,
        "mystery_gift": mystery_gift,
        "items": cart_items,

        "subtotal": subtotal,

        "delivery_type": delivery_type,
        "delivery_charge": delivery_charge,

        "packing": packing,
        "packing_charge": packing_charge,

        "first_order_discount": first_order_discount,
        "order_discount": order_discount,
        "birthday_discount": birthday_discount,
        "game_discount": game_discount,
        "payment_discount": payment_discount,
        "coupon_code": coupon_code,
        "coupon_discount": coupon_discount,

        "total_discount": total_discount,
        "total": final_total
    }

    # Mark this customer as having ordered
    session["has_ordered_before"] = True

    # Clear game reward after using it
    session.pop("tic_tac_toe_won", None)

    # Clear cart
    session["cart"] = []

    return render_template(
        "order_success.html",
        order=session["last_order"]
    )


    # -----------------------------
    # SAVE ORDER TO DATABASE
    # -----------------------------

    user_id = session.get("user_id")

    if user_id:
        new_order = Order(
            user_id=user_id,
            customer_name=customer_name,
            phone=phone,
            address=address,
            payment_method=payment,
            payment_status="Pending",
            subtotal=subtotal,
            delivery_charge=delivery_charge,
            packing_charge=packing_charge,
            discount=total_discount,
            total=final_total,
            delivery_type=delivery_type,
            estimated_delivery="25 minutes"
        )

        db.session.add(new_order)
        db.session.flush()

        for item in cart_items:
            menu_item = MenuItem.query.filter_by(
                name=item["name"]
            ).first()

            if menu_item:
                order_item = OrderItem(
                    order_id=new_order.id,
                    menu_item_id=menu_item.id,
                    quantity=item["quantity"],
                    price=item["price"]
                )

                db.session.add(order_item)

        db.session.commit()

@app.route("/orders")
def orders():

    if not session.get("logged_in") or not session.get("customer_verified"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")

    user_orders = []

    if user_id:
        user_orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()

    return render_template("orders.html", orders=user_orders)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
if __name__ == "__main__":
    app.run(debug=True)






































@app.route("/clear_cart")
def clear_cart():

    session["cart"] = []

    return redirect(url_for("cart"))













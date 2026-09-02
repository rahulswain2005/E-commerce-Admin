from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ecommerce-dashboard-secret"

products = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "price": 79.99, "stock": 42, "sales": 1280, "status": "Active"},
    {"id": 2, "name": "Smart Watch Pro", "category": "Electronics", "price": 129.99, "stock": 18, "sales": 965, "status": "Active"},
    {"id": 3, "name": "Running Shoes", "category": "Fashion", "price": 64.50, "stock": 7, "sales": 742, "status": "Low Stock"},
    {"id": 4, "name": "Minimal Backpack", "category": "Fashion", "price": 49.99, "stock": 31, "sales": 618, "status": "Active"},
    {"id": 5, "name": "Mechanical Keyboard", "category": "Electronics", "price": 94.00, "stock": 0, "sales": 531, "status": "Out of Stock"},
]

orders = [
    {"id": "#EC-1048", "customer": "Aarav Sharma", "product": "Wireless Headphones", "amount": 159.98, "date": "02 Sep 2026", "status": "Delivered"},
    {"id": "#EC-1047", "customer": "Priya Das", "product": "Smart Watch Pro", "amount": 129.99, "date": "02 Sep 2026", "status": "Processing"},
    {"id": "#EC-1046", "customer": "Rohan Patel", "product": "Running Shoes", "amount": 64.50, "date": "01 Sep 2026", "status": "Shipped"},
    {"id": "#EC-1045", "customer": "Ananya Roy", "product": "Minimal Backpack", "amount": 49.99, "date": "01 Sep 2026", "status": "Delivered"},
    {"id": "#EC-1044", "customer": "Kabir Singh", "product": "Mechanical Keyboard", "amount": 94.00, "date": "31 Aug 2026", "status": "Cancelled"},
]

@app.route("/")
def dashboard():
    total_sales = sum(p["sales"] for p in products)
    revenue = sum(o["amount"] for o in orders if o["status"] != "Cancelled")
    return render_template(
        "dashboard.html",
        products=products,
        orders=orders,
        total_sales=total_sales,
        revenue=revenue,
        now=datetime.now().strftime("%d %b %Y")
    )

@app.route("/products", methods=["GET", "POST"])
def product_page():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "Other")
        price = float(request.form.get("price", 0) or 0)
        stock = int(request.form.get("stock", 0) or 0)
        if name:
            products.append({
                "id": len(products) + 1,
                "name": name,
                "category": category,
                "price": price,
                "stock": stock,
                "sales": 0,
                "status": "Active" if stock > 0 else "Out of Stock"
            })
            flash("Product added successfully.", "success")
        return redirect(url_for("product_page"))
    return render_template("products.html", products=products)

@app.route("/orders")
def order_page():
    return render_template("orders.html", orders=orders)

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)

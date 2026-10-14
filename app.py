import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory database simulation for prototype
inventory = [
    {"id": 1, "item": "Organic Milk", "category": "Dairy", "expiry": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), "quantity": "1 Liter", "status": "Expiring Soon"},
    {"id": 2, "item": "Ripe Tomatoes", "category": "Produce", "expiry": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), "quantity": "500g", "status": "Good"},
    {"id": 3, "item": "Whole Wheat Bread", "category": "Bakery", "expiry": (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'), "quantity": "1 Loaf", "status": "Good"},
    {"id": 4, "item": "Greek Yogurt", "category": "Dairy", "expiry": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), "quantity": "2 Cups", "status": "Expiring Soon"}
]

donations = [
    {"id": 1, "donor": "GreenCafé Downtown", "item": "Prepared Veggie Sandwiches (x5)", "location": "Sector 4 Hub", "time": "Available till 8 PM"},
    {"id": 2, "donor": "FreshBake Bakery", "item": "Assorted Pastries (x8)", "location": "Campus Gate 2", "time": "Immediate Pickup"}
]

@app.route('/')
def index():
    return render_template('index.html', inventory=inventory, donations=donations)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form.get('item_name')
    category = request.form.get('category')
    expiry_date = request.form.get('expiry_date')
    quantity = request.form.get('quantity')
    
    if item_name and expiry_date:
        # Calculate status
        exp_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        days_left = (exp_date - datetime.now().date()).days
        status = "Expiring Soon" if days_left <= 2 else "Good"
        
        new_id = len(inventory) + 1
        inventory.append({
            "id": new_id,
            "item": item_name,
            "category": category,
            "expiry": expiry_date,
            "quantity": quantity,
            "status": status
        })
    return redirect(url_for('index'))

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    selected_items = data.get('items', [])
    
    if not selected_items:
        return jsonify({"recipe": "Please select at least one ingredient to generate a zero-waste recipe."})
    
    recipe_html = f"""
    <div class='recipe-card'>
        <h4 class='text-success mb-2'><i class='fas fa-utensils me-2'></i>Smart Zero-Waste Rescue Bowl</h4>
        <p class='text-muted mb-2'><strong>Utilizing:</strong> {', '.join(selected_items)}</p>
        <hr>
        <ol class='ps-3 mb-0'>
            <li class='mb-1'>Chop all selected items into uniform bite-sized portions.</li>
            <li class='mb-1'>Heat 1 tbsp of olive oil in a skillet over medium-high heat.</li>
            <li class='mb-1'>Sauté firm items first for 3-4 minutes, then fold in leafy or delicate items.</li>
            <li>Season with sea salt, black pepper, and herbs. Serve hot immediately!</li>
        </ol>
    </div>
    """
    return jsonify({"recipe": recipe_html})

@app.route('/add_donation', methods=['POST'])
def add_donation():
    donor = request.form.get('donor')
    item = request.form.get('item')
    location = request.form.get('location')
    time_slot = request.form.get('time_slot')
    
    if donor and item:
        donations.append({
            "id": len(donations) + 1,
            "donor": donor,
            "item": item,
            "location": location or "Main Hall",
            "time_slot": time_slot or "Available Today"
        })
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

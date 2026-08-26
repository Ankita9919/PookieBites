from pathlib import Path

p = Path("templates/menu.html")
s = p.read_text(encoding="utf-8-sig")

old = '''    <div class="menu-food-image">
        {{ food.icon }}
    </div>'''

new = '''    <div class="menu-food-image">
        <img src="{{ url_for('static', filename='images/' + food.image) }}"
             alt="{{ food.name }}"
             onerror="this.src='{{ url_for('static', filename='images/default_food.jpg') }}'">
    </div>'''

if old in s:
    s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print("DONE - Pookie menu restored with food images")
else:
    print("IMAGE SECTION NOT FOUND")

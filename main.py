from flask import Flask, render_template

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # Remove in final version
app.jinja_env.auto_reload = True  # Remove in final version

@app.route('/')
def main():
    # List of insurance types to pass to the template
    insurance_types = ["Краткосрочное", "Долгосрочное", "Полное", "Минимальное"]
    return render_template("main.html", insurance_types=insurance_types)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/editor')
def edit():
    return render_template("edit.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # Remove in final version
app.jinja_env.auto_reload = True  # Remove in final version

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/main_page')
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
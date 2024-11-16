from flask import Flask, url_for, redirect
from flask_login import LoginManager, login_required, logout_user
from login import app_login, User
from dbloader import connect_to_db

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # Remove in final version
app.jinja_env.auto_reload = True  # Remove in final version
conn, cur = connect_to_db()
login_manager = LoginManager(app)
login_manager.login_view = 'app_login.login'
app.register_blueprint(app_login)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    pass


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

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

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database based on the user ID.

    This function is called by Flask-Login to retrieve a user's
    information from the database when the user is authenticated.
    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User or None:
            - Returns an instance of the User class with the user's details
              if the user is found.
            - Returns None if the user does not exist.

    Raises:
        Exception: May raise an exception if the database query fails.
    """
    cur.execute("SELECT id, name, password, email FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
        return User(*user_data)
    return None


@app.route('/logout')
@login_required
def logout():
    """Logs the user out and redirects them to the login page."""
    logout_user()
    return redirect(url_for('app_login.login'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    pass


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

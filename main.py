from flask import Flask, url_for, redirect, request, render_template
from flask_login import LoginManager, login_required, logout_user, current_user
from login import app_login, User, load_user
from dbloader import connect_to_db
import json
import psycopg2

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # Remove in final version
app.config['SECRET_KEY'] = 'bruh'
app.jinja_env.auto_reload = True  # Remove in final version

conn, cur = connect_to_db()

app.register_blueprint(app_login)

login_manager = LoginManager(app)
login_manager.login_view = 'app_login.login'


@login_manager.user_loader
def _load_user(uid):
    return load_user(uid)


@app.route("/")
#@login_required
def main_page():
    if len(request.args) == 0:
        cur.execute('''SELECT 
    ipc.name AS insurance_category_name,
    ip.id AS insurance_product_id,
    ip.name AS insurance_product_name,
    ip.description AS insurance_product_description
FROM 
    insurance_product_categories ipc
JOIN 
    insurance_product_categories_connections ipcc 
    ON ipc.id = ipcc.insurance_product_category_id
JOIN 
    insurance_products ip 
    ON ipcc.insurance_product_id = ip.id;''')
        data = cur.fetchall()
        for item in data:
            print(item)
        return 'a'  # render_template('main.html', data=data)

#GUYS PLEASE DONT FORGET TO ADD IMG LOADER FOR SIGNATURES. IT"S OPTIONAL BUT WILL BE A GOOD FEATURE. I"VE MADE ALL FUNCS NEEDED TO STORE IT BD. 
#MID WAY OF PIC SAVING IN static/signatures. IT HAS A DEFOULT OPTION IF USER WONT LOAD HIS SIGNATURE.
@app.route("/contract_editor")
@login_required
def contract_editor():
    if request.method == 'GET':
        try:
            cont_id = request.form['contract_id']
            cur.execute('SELECT * FROM contracts WHERE id = %s', (cont_id, ))
            cont = cur.fetchall()     
            if not cont:
                print(f"No contract found with id {cont_id}")
                return

            user_id, insurance_product_id, insurance_product_data, created_at = \
            cont[1], cont[2], cont[3], cont[4]

            parsed_data = json.loads(insurance_product_data)

            # Создать копию контракта с новым id
            cur.execute("""
                INSERT INTO contracts (user_id, insurance_product_id, insurance_product_data, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (user_id, insurance_product_id, json.dumps(insurance_product_data), created_at))
            
            new_id = cur.fetchone()[0]
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            cur.close()
        return render_template("editor.html")
    if request.method == 'POST':
        pass

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

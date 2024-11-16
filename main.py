from flask import Flask, request, render_template
from flask_login import LoginManager, login_required, current_user
from login import app_login, load_user
from dbloader import connect_to_db
import json
from collections import defaultdict
from db_funcs import create_contract

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
# @login_required
def main_page():
    """Main page, here you select which contract a user will sign. Returns the main template."""
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
        grouped_results = defaultdict(list)

        for catname, productid, productname, productdesc in data:
            grouped_results[catname].append([productid, productname, productdesc])
        print(dict(grouped_results))
        return 'a'  # render_template('main.html', data=data)


@app.route('/new_contract')
def new_contract():
    """
    Once a user has selected the contract they fill in the data here.
    Args:
        - id (int): id of the contract
    Returns:
        new_contract template
    """
    cid = request.args.get('id', -1, type=int)
    assert cid != -1
    cur.execute("""SELECT f.id, f.description, f.variable_type, f.editable, f.default_value
FROM insurance_product_fields ipf
JOIN fields f ON ipf.field_id = f.id
WHERE ipf.insurance_product_id = %s;""", (cid, ))
    data = cur.fetchall()
    print(data)
    return 'a'


@app.route('/submit_contract')
def submit_contract():  # TODO: signature
    """
    Once a user has selected the contract they fill in the data here.
    Args:
        - id (int): id of the contract
        - request form (dict): field-value pairs
    Returns:
        string: success or error {e}
    """
    data = request.form.to_dict()
    productid = request.args.get('id', -1, type=int)
    assert productid != -1
    userid = current_user.id
    try:
        create_contract(user_id=userid, insurance_product_id=productid, fields=data)
        return 'success'
    except Exception as e:
        return f'error: {e}'


@app.route('/account')
def account():
    """Shows all the active contracts for a user"""

    cur.execute('''SELECT ip.name, ip.description, c.created_at
FROM contracts c 
JOIN insurance_products ip ON ip.id = c.insurance_product_id
WHERE user_id = %s;''', (current_user.id, ))
    data = cur.fetchall()
    print(data)
    return 'a'



# GUYS PLEASE DONT FORGET TO ADD IMG LOADER FOR SIGNATURES. IT"S OPTIONAL BUT WILL BE A GOOD FEATURE.
# I"VE MADE ALL FUNCS NEEDED TO STORE IT BD.
# MID WAY OF PIC SAVING IN static/signatures. IT HAS A DEFOULT OPTION IF USER WONT LOAD HIS SIGNATURE.
@app.route("/product_creator")
@login_required
def product_creator():
    if request.method == 'GET':
        try:
            prod_id = request.form['prodract_id']
            cur.execute('SELECT * FROM insurance_products WHERE id = %s', (prod_id, ))
            prod = cur.fetchall()

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            cur.close()
        return render_template("editor.html")

    if request.method == 'POST':
        try:
            prod_id = request.form['prodract_id']
            cur.execute('SELECT * FROM prodracts WHERE id = %s', (prod_id, ))
            prod = cur.fetchall()

            user_id, insurance_product_id, insurance_product_data, created_at = \
                prod[1], prod[2], prod[3], prod[4]

            parsed_data = json.loads(insurance_product_data)

            # Создать копию контракта с новым id
            cur.execute("""
                INSERT INTO prodracts (user_id, insurance_product_id, insurance_product_data, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (user_id, insurance_product_id, json.dumps(insurance_product_data), created_at))
            conn.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            cur.close()
        return render_template("editor.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
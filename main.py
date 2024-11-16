from flask import Flask, render_template, redirect, request

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

@app.route('/new_contract', methods=['GET', 'POST'])
def new_contract():
    # Mock data for fields
    contract_id = request.args.get('id')  # Ensure ID is fetched correctly
    fields = [
        [1, "Имя клиента", "text", True, ""],
        [2, "Возраст клиента", "number", True, ""],
        [3, "Номер договора", "text", False, "123456"]
    ]
    
    return render_template('new_contract.html', fields=fields, contract_id=contract_id)

@app.route('/submit_contract', methods=['POST'])
def submit_contract():
    contract_id = request.args.get('id')
    field_data = request.form.to_dict()
    
    # Logic for handling form data
    print(f"Contract ID: {contract_id}")
    print(f"Field Data: {field_data}")
    
    return redirect('/success')  # Redirect after successful submission

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/editor')
def edit():
    return render_template("edit.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
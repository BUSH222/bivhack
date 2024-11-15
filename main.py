from flask import Flask

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # Remove in final version
app.jinja_env.auto_reload = True  # Remove in final version


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

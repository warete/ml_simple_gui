from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='./frontend/dist', template_folder='./frontend/dist')
app.debug = True
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=app.debug)

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='', static_folder='./frontend/dist', template_folder='./frontend/dist')
app.debug = True
app.config['UPLOAD_FOLDER'] = os.path.join('upload')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_data/', methods=['POST'])
def upload_data():
    file = request.files['file']
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({
            'status': 'success',
            'result': {
                'file_path': file_path
            }
        })
    else:
        return jsonify({
            'status': 'error',
            'result': {
                'message': 'Неподходящий тип файла'
            }
        })


if __name__ == '__main__':
    app.run(debug=app.debug)

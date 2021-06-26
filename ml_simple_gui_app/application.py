from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os


class Application:
    model = None
    upload_path = '/upload'
    server_port = 5000

    def __init__(self, model, upload_path, server_port=5000):
        self.model = model
        self.upload_path = upload_path
        self.server_port = server_port

    def set_model(self, model):
        self.model = model
        return self

    def set_upload_path(self, upload_path):
        self.upload_path = upload_path
        return self

    def set_server_port(self, port):
        self.server_port = port
        return self

    def run(self):

        flask_app = Flask(
            __name__,
            static_url_path='',
            static_folder='./frontend/dist',
            template_folder='./frontend/dist'
        )
        flask_app.debug = True
        flask_app.config['UPLOAD_FOLDER'] = self.upload_path
        CORS(flask_app)

        self.set_routes(flask_app)

        flask_app.run(debug=True, port=self.server_port)

    def set_routes(self, app):
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
                        'file_path': file.filename
                    }
                })
            else:
                return jsonify({
                    'status': 'error',
                    'result': {
                        'message': 'Неподходящий тип файла'
                    }
                })

        @app.route('/fit_predict/', methods=['POST'])
        def fit_predict():
            return jsonify({
                'status': 'success',
                'result': {
                    'accuracy': 0,
                    'sensitivity': 0,
                    'specificity': 0,
                }
            })

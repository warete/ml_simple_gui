from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from .utils import check_model, calculate_sensitivity, calculate_specificity, get_data_from_csv
import os
import json
import glob

import pandas as pd
import time
import urllib.parse

class Application:
    model = None
    model_constructor = None
    upload_path = '/upload'
    server_port = 5000
    csv_delimiter = ','
    model_params = [
        {
            'code': 'testPercent',
            'name': 'Процент тестовой выборки',
            'defaultValue': 25,
        }
    ]
    metrics = []

    def __init__(self, model, upload_path, csv_delimiter, model_params=None, server_port=5000, metrics=None):
        if model_params is None:
            model_params = []
        if callable(model):
            self.model_constructor = model
        else:
            self.model = model
        self.upload_path = upload_path
        self.csv_delimiter = csv_delimiter
        self.server_port = server_port
        self.model_params += model_params
        self.process_model_params()
        if metrics:
            self.metrics = metrics

    def set_model(self, model):
        self.model = model
        return self

    def set_upload_path(self, upload_path):
        self.upload_path = upload_path
        return self

    def set_server_port(self, port):
        self.server_port = port
        return self

    def set_csv_delimiter(self, csv_delimiter):
        self.csv_delimiter = csv_delimiter
        return self

    def run(self):
        flask_app = Flask(
            __name__,
            static_url_path='',
            static_folder='./frontend/dist',
            template_folder='./frontend/dist'
        )
        flask_app.debug = True
        flask_app.config['UPLOAD_FOLDER'] = os.path.abspath(self.upload_path)
        CORS(flask_app)

        self.set_routes(flask_app)

        flask_app.run(port=self.server_port)

    def process_model_params(self):
        for k in range(len(self.model_params)):
            if 'value' not in self.model_params[k]:
                self.model_params[k]['value'] = self.model_params[k]['defaultValue']

    def set_routes(self, app):
        @app.route('/')
        def index():
            return render_template('index.html')
        
        @app.route('/' + self.upload_path + '/<path:path>')
        def send_upload(path):
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], path))

        @app.route('/model_params')
        def model_params():
            return jsonify({
                'status': 'success',
                'result': {
                    'params': self.model_params
                }
            })

        @app.route('/get_files/', methods=['GET'])
        def get_files():
            return jsonify({
                'status': 'success',
                'result': [os.path.basename(file) for file in
                           glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.csv'))]
            })

        @app.route('/upload_data/', methods=['POST'])
        def upload_data():
            file = request.files['file']
            if file:
                file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename)
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
        def fit_predict_handler():
            # {'file': {'file_path': 'test.csv'}, 'modelParams': {}}
            req_params = json.loads(request.get_data())
            if len(req_params['file']['file_path']) == 0 or not os.path.isfile(
                    os.path.join(self.upload_path, req_params['file']['file_path'])):
                return jsonify({
                    'status': 'error',
                    'result': {
                        'message': 'Файл не существует'
                    }
                })
            if self.model_constructor:
                params = {}
                for paramCode in req_params['modelParams']:
                    if paramCode == 'testPercent':
                        continue
                    params[paramCode] = req_params['modelParams'][paramCode]['value']
                self.model = self.model_constructor(**params)
            if not check_model(self.model):
                return jsonify({
                    'status': 'error',
                    'result': {
                        'message': 'Ошибка при использовании модели. Проверьте наличие необходимых методов'
                    }
                })
            data_from_file = get_data_from_csv(
                os.path.join(self.upload_path, req_params['file']['file_path']), self.csv_delimiter)
            x = data_from_file.iloc[:, :-1]
            y = data_from_file.iloc[:, -1:]

            on_before_split_method = getattr(
                self.model, 'on_before_split', None)
            if callable(on_before_split_method):
                x, y = self.model.on_before_split(data_from_file)

            x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                                test_size=int(req_params['modelParams']['testPercent'][
                                                                    'value']) / 100
                                                                )

            on_after_split_method = getattr(self.model, 'on_after_split', None)
            if callable(on_after_split_method):
                x_train, x_test, y_train, y_test = self.model.on_after_split(
                    x_train, x_test, y_train, y_test)

            self.model.fit(x_train, y_train)
            print(x_test.shape)
            y_pred = self.model.predict(x_test)

            metrics_result = {}
            for metric in self.metrics:
                f_metric_func = metric['func']
                metric_result = None
                if callable(f_metric_func):
                    metric_result = f_metric_func(
                        y_test, y_pred, y_train, x_train, x_test)
                else:
                    metric_method = getattr(self.model, f_metric_func, None)
                    if metric_method:
                        metric_result = metric_method(
                            y_test, y_pred, y_train, x_train, x_test)

                if metric_result:
                    metrics_result[metric['code']] = {
                        'code': metric['code'],
                        'name': metric['name'],
                        'result': metric_result,
                        'result_type': metric['result_type']
                    }

            # accuracy = accuracy_score(y_test, y_pred)
            # sensitivity = calculate_sensitivity(y_test, y_pred) * 100
            # specificity = calculate_specificity(y_test, y_pred) * 100

            return jsonify({
                'status': 'success',
                'result': metrics_result
            })

        @app.route('/predict/', methods=['POST'])
        def predict_handler():
            req_params = json.loads(request.get_data())
            if len(req_params['file']['file_path']) == 0 or not os.path.isfile(
                    os.path.join(self.upload_path, req_params['file']['file_path'])):
                return jsonify({
                    'status': 'error',
                    'result': {
                        'message': 'Файл не существует'
                    }
                })
            if not check_model(self.model):
                return jsonify({
                    'status': 'error',
                    'result': {
                        'message': 'Ошибка при использовании модели. Проверьте наличие необходимых методов'
                    }
                })
            data_from_file = get_data_from_csv(
                os.path.join(self.upload_path, req_params['file']['file_path']), self.csv_delimiter)
            x = data_from_file.iloc[:, :-1]
            y = data_from_file.iloc[:, -1:]

            on_before_split_method = getattr(
                self.model, 'on_before_split_for_predict', None)
            if callable(on_before_split_method):
                x_test = on_before_split_method(data_from_file)

            print(x_test.shape)
            y_pred = self.model.predict(x_test)
            print(y_pred.shape)
            on_after_real_predict_method = getattr(
                self.model, 'on_after_real_predict', None)
            if callable(on_after_real_predict_method):
                y_pred = on_after_real_predict_method(y_pred)

            new_data_frame = pd.DataFrame(y_pred)
            predict_data_file_name, _ = os.path.splitext(
                req_params['file']['file_path'])
            result_file_path = os.path.join(
                self.upload_path, predict_data_file_name + '_result_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.csv')
            new_data_frame.to_csv(result_file_path, sep=',',
                                  encoding='utf-8', index=False)

            return jsonify({
                'status': 'success',
                'result': {
                    'filePath': self.upload_path + '/' + predict_data_file_name + '_result_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.csv'
                }
            })

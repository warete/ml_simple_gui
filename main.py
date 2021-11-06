from ml_simple_gui import Application
import os
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time


class CustomModel:
    model = None
    train_dataset = None
    test_dataset = None
    epochs = 1000
    main_scaler = None
    columns = []
    last_fit_history = {}

    def __init__(self, optimizer_learning_speed=0.01, epochs=1000):
        inputs = tf.keras.layers.Input(name='values18', shape=(19,), dtype='float32')
        outputs = tf.keras.layers.Dropout(0.1)(inputs)

        outputs = tf.keras.layers.Dense(37, activation='sigmoid')(outputs)
        outputs = tf.keras.layers.Dropout(0.1)(outputs)

        outputs = tf.keras.layers.Dense(18)(outputs)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=tf.keras.optimizers.SGD(float(optimizer_learning_speed)), loss='MSE')

        self.epochs = int(epochs)
        self.model = model

    def fit(self, x_train, y_train):
        start_t = time.time()
        history = self.model.fit(self.train_dataset, validation_data=self.test_dataset, epochs=self.epochs,
                       callbacks=[tf.keras.callbacks.TensorBoard(log_dir='logs')])

        self.last_fit_history['loss'] = history.history['loss']
        self.last_fit_history['val_loss'] = history.history['val_loss']

        end_t = time.time()
        print('Finish time: ', end_t - start_t)

    def predict(self, x_test):
        pred_test_X = self.model.predict(x_test)
        return pred_test_X

    def on_before_split(self, data_from_file):
        df = data_from_file
        cols = df.columns.tolist()
        diameter_data = df['diameter'].values
        df = df[cols[:-1]]
        self.columns = df.columns

        source_values = df.values

        # data preprocessing
        scaler = StandardScaler()
        scaler.fit(source_values)

        source_values = scaler.transform(source_values)

        d_scaler = StandardScaler()
        d_scaled = d_scaler.fit_transform([[x] for x in diameter_data])
        diameter_data = [x[0] for x in d_scaled]

        a = []
        for i in range(len(source_values)):
            a.append(np.insert(source_values[i], 0, diameter_data[i]))
        source_values = np.array(a)

        np.random.shuffle(source_values)

        self.main_scaler = scaler

        return source_values[:, :19], source_values[:, 19:]

    def on_after_split(self, x_train, x_test, y_train, y_test):
        self.train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(1000)
        self.test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(1000)
        return x_train, x_test, y_train, y_test

    def prepare_data_for_error_metrics(self, y_test, y_pred, x_test):
        test_x_without_d = x_test[:, 1:]
        real_data = pd.DataFrame(self.main_scaler.inverse_transform(np.hstack((test_x_without_d, y_test))),
                                 columns=self.columns)
        predict_data = pd.DataFrame(self.main_scaler.inverse_transform(np.hstack((test_x_without_d, y_pred))),
                                    columns=self.columns)
        left_columns = ['t' + str(i) for i in range(18, 36)]
        left_real = real_data[left_columns]
        left_predict = predict_data[left_columns]
        left_real.columns = ['mw' + str(i) for i in range(9)] + ['ir' + str(i) for i in range(9)]
        left_predict.columns = ['mw' + str(i) for i in range(9)] + ['ir' + str(i) for i in range(9)]

        return left_predict, left_real

    def calc_rel_error(self, y_test, y_pred, y_train, x_train, x_test):
        '''
        Метод для расчета относительной ошибки
        '''
        left_predict, left_real = self.prepare_data_for_error_metrics(y_test, y_pred, x_test)
        rel_error = left_real.sub(left_predict).div(left_real).abs().sum().mul(100).div(len(left_real)).to_frame()

        result = {}
        for item_k in rel_error.to_dict()[0].keys():
            result[item_k] = float('{:.3f}'.format(rel_error.to_dict()[0][item_k]))
        return result

    def calc_mae_error(self, y_test, y_pred, y_train, x_train, x_test):
        '''
        Метод для расчета средней абсолютной ошибки
        '''
        left_predict, left_real = self.prepare_data_for_error_metrics(y_test, y_pred, x_test)
        mae_error = left_real.sub(left_predict).abs().sum().div(len(left_real)).to_frame()

        result = {}
        for item_k in mae_error.to_dict()[0].keys():
            result[item_k] = float('{:.3f}'.format(mae_error.to_dict()[0][item_k]))
        return result
    
    def get_fit_mse(self, y_test, y_pred, y_train, x_train, x_test):
        return float('{:.3f}'.format(self.last_fit_history['val_loss'][-1]))
    
    def get_loss_graph(self, y_test, y_pred, y_train, x_train, x_tests):
        import matplotlib.pyplot as plt
        import io
        import base64

        plt.xlabel('epochs')
        plt.ylabel('loss')
        plt.plot(list(range(self.epochs)), self.last_fit_history['loss'], label='loss')
        plt.plot(list(range(self.epochs)), self.last_fit_history['val_loss'], label='val_loss')
        plt.legend()
        plt.grid(True)
        

        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        return 'data:image/png;base64, ' + s


def model(**args):
    return CustomModel(**args)


def accuracy_score_custom(y_test, y_pred, y_train, x_train, x_test):
    return accuracy_score(y_test, y_pred)


app = Application(
    model=model,
    upload_path=os.path.join('upload'),
    csv_delimiter=',',
    model_params=[
        {
            'code': 'optimizer_learning_speed',
            'name': 'Скорость обучения',
            'defaultValue': '0.01',
        },
        {
            'code': 'epochs',
            'name': 'Количество эпох',
            'defaultValue': '50',
        }
    ],
    server_port=5000,
    metrics=[
        {
            'code': 'rel_error',
            'name': 'Относительная ошибка',
            'func': 'calc_rel_error',
            'result_type': 'table'
        },
        {
            'code': 'mae_error',
            'name': 'Средняя абсолютная ошибка',
            'func': 'calc_mae_error',
            'result_type': 'table'
        },
        {
            'code': 'mse',
            'name': 'Среднеквадратичная ошибка',
            'func': 'get_fit_mse',
            'result_type': 'scalar'
        },
        {
            'code': 'loss',
            'name': 'График изменения среднеквадратичной ошибки',
            'func': 'get_loss_graph',
            'result_type': 'image'
        }

    ]
)

app.run()

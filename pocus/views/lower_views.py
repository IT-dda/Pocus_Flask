from flask import Blueprint, request
import joblib
import numpy as np
import json

bp = Blueprint('lower', __name__, url_prefix='/lower')
model = joblib.load('./pocus/static/models/sensor.pkl')


@bp.route('/')
def lower_get():
    X_new = np.array([[790, 880, 870, 880]])
    print(X_new.shape)
    prediction = model.predict(X_new)
    return "예측: {}".format(prediction)


@bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        res = request.get_json()
        nums = res['values']
        sensor_value = np.array(list(map(int, nums.split(','))))
        sensor_value = sensor_value.reshape((1, -1))
        prediction = model.predict(sensor_value)
        return json.dumps({'prediction': int(prediction[0]), 'params': nums})
    else:  # GET
        return '성공!!!!!!!!!!!'

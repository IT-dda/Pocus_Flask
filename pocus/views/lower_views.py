from flask import Blueprint, request
import joblib
import numpy as np
import json
from ..save_noti import table_log, table_ss

bp = Blueprint('lower', __name__, url_prefix='/lower')
model = joblib.load('./pocus/static/models/sensor.pkl')
LOWER = ['바른 자세', '왼쪽 다리 꼰 자세', '오른쪽 다리 꼰 자세', '양반다리', '잘못된 자세']


@bp.route('/')
def lower_get():
    X_new = np.array([[790, 880, 870, 880]])
    print(X_new.shape)
    prediction = model.predict(X_new)
    return "예측: {}".format(prediction)


@bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        req = request.get_json()
        nums = req['values']
        user_id = req['userid']
        values = list(map(int, nums.split(',')))
        # print(f'values are {values}')
        # print(f'userid is {user_id}')

        # predict
        sensor_value = np.array(values)
        sensor_value = sensor_value.reshape((1, -1))
        prediction = model.predict(sensor_value) # int64

        # save at db
        if int(prediction[0]):
            log_id = table_log(user_id, LOWER[int(prediction[0])], 0)
            table_ss(log_id, values[0], values[1], values[2], values[3])

        return json.dumps({'prediction': int(prediction[0]), 'params': nums})
    else:  # GET
        return '성공!!!!!!!!!!!'

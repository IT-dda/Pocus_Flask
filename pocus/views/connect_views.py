import io
from ..database import Database
from flask import Blueprint, request, jsonify
import requests
from io import BytesIO
from PIL import Image
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

bp = Blueprint('conn', __name__, url_prefix='/conn')


@bp.route('/image', methods=['GET', 'POST'])
def image_test():
    if request.method == 'POST':
        res = request.get_json()
        img = res['url']
        return f'{img}'
    else: # GET
        ## base 64 사용
        # url.encode('utf-8')
        # img = base64.b64decode(url)
        # img = BytesIO(img)
        # img = Image.open(img)
        # img.save('test.jpg')
        # #
        # # # plt.imshow(img)
        # # # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        # # # cv2.imshow('test', img)
        # return 'done'
        # #
        # # # im_bytes = base64.b16decode(url)
        # # # im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        # # # img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        # # # cv2.imshow(img)
        # # # return 'ss'

        # file_path = 'C:/Users/jyj24/Desktop/test.jpg'
        # with open(file_path, 'rb') as img:
        #     base64_string = base64.b64encode(img.read())
        # img = Image.open(BytesIO(base64.b64decode(base64_string)))
        # plt.imshow(img)
        # return img

        print('요청성공얼마널넝라ㅓㄴ이럼;럼;ㅏ러')
        # return 'test image get'
        return json.dumps({'message': 'test image get done'})

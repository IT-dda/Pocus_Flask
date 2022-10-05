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

def stringToRGB(base64_string):
    imgdata = base64.b64decode(base64_string)
    dataBytesIO = io.BytesIO(imgdata)
    image = Image.open(dataBytesIO)
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


@bp.route('/image', methods=['GET', 'POST'])
def image_test():
    if request.method == 'GET':
        # res = request.get_json()
        # img = res['url']
        # return f'{img}'
        print('GET 요청성공얼마널넝라ㅓㄴ이럼;럼;ㅏ러')
        return json.dumps({'message': 'test image get done'})
    else: # POST
        res = request.get_json()
        url = res['values'][22:]
        # print('+++++++++++++++++++++++++++++++++++++++++++++START+++++++++++++++++++++++++++++++++++')
        # print(url)
        # print('--------------------------------------END-----------------------------------------')

        ## base 64 사용
        # url.encode('utf-8')
        img = base64.b64decode(url)
        img = BytesIO(img)
        img = Image.open(img)
        img = img.convert("RGB")
        img.save('test.jpg')
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

        # print('POST 요청성공얼마널넝라ㅓㄴ이럼;럼;ㅏ러')
        return json.dumps({'message': 'test image post done'})


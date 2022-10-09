from flask import Blueprint, request
import tensorflow as tf
import mediapipe as mp
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
import json
from ..database import Database

bp = Blueprint('upper', __name__, url_prefix='/upper')

model = tf.keras.models.load_model('./pocus/static/models/4-holistic-ldmk-1-binary-sigmoid-epo20.h5')

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

CLASSES = ["correct", "turtle", "shoulder-left", "shoulder-right", "head-left", "head-right", "chin-left", "chin-right"]
# CLASSES = ["correct", "wrong"]


# image preprocessing : numpy 배열로 바꾸는거까지
def preprocess(img):
    img = np.array(img) # <class 'PIL.Image.Image'> -> np array

    # gray scale
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # padding
    # h, w = img_gray.shape
    h, w, c = img_rgb.shape
    dif = w - h
    # img_padding = cv2.copyMakeBorder(img_gray, dif // 2, dif // 2, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    image = cv2.copyMakeBorder(img_rgb, dif // 2, dif // 2, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    # image = cv2.cvtColor(img_padding, cv2.COLOR_GRAY2RGB)

    with mp_holistic.Holistic(static_image_mode=True, model_complexity=2, enable_segmentation=True,
                              refine_face_landmarks=True) as holistic:
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not results.pose_landmarks and not results.face_landmarks:
            return None

        # background
        annotated_image = image.copy()
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = (0, 0, 0)
        annotated_image = np.where(condition, annotated_image, bg_image)
        # annotated_image[:] = (0, 0, 0)

        # draw
        mp_drawing.draw_landmarks(annotated_image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                  landmark_drawing_spec=None,
                                  connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(), )
        mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(), )  # (1920, 1920, 3)

    # annotated_image = cv2.resize(annotated_image, (192, 192))  # (192, 192, 3)
    annotated_image = cv2.resize(img, (192, 192))  # (192, 192, 3)
    annotated_image = np.expand_dims(annotated_image, axis=0)

    return annotated_image


@bp.route('/', methods=['GET'])
def upper_get():
    return 'Upper'


@bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        req = request.get_json()
        url = req['values'][22:]  # "data:image/png;base64," 제거

        # base64 to image
        img = base64.b64decode(url)
        img = BytesIO(img)
        img = Image.open(img)
        img = img.convert("RGB")

        # if not img.any():
        #     return json.dumps({'message': 'cannot read image'})

        annotated_image = preprocess(img)

        if annotated_image is None:
            return json.dumps({'message': 'cannot get landmarks'})

        prediction = model.predict(annotated_image)  # <class 'numpy.ndarray'>
        label = prediction.argmax()

        print(prediction)

        return json.dumps({'message': int(label), 'pose': CLASSES[label]})
        # return json.dumps({'message': CLASSES[label]})
    else:  # GET
        return f'upper predict test'

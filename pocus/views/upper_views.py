from flask import Blueprint, request
import numpy as np
import tensorflow as tf
import cv2
import mediapipe as mp
import os

bp = Blueprint('upper', __name__, url_prefix='/upper')
model = tf.keras.models.load_model('./pocus/static/cnn/220821-1-epo12.h5')
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
CLASSES = ["correct", "turtle", "shoulder-left", "shoulder-right", "head-left", "head-right", "chin-left", "chin-right"]


@bp.route('/', methods=['GET'])
def upper_get():
    return 'Upper'


@bp.route('/predict', methods=['GET'])
def predict():
    # if request.method == 'POST':
    # img = request.files['image']
    res = []
    BASE_DIR = './pocus/static/images'
    images = os.listdir(BASE_DIR)
    for i in range(len(images)):
        img = cv2.imread(f'{BASE_DIR}/{images[i]}')
        if not img.any():
            return 'nothing to predict'

        # image preprocessing : numpy 배열로 바꾸는거까지
        with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True,
                          min_detection_confidence=0.5) as pose:
            # gray scale
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # padding
            h, w = img_gray.shape
            dif = w - h
            img_padding = cv2.copyMakeBorder(img_gray, dif // 2, dif // 2, 0, 0, cv2.BORDER_CONSTANT, value=[192, 192, 192])
            image = cv2.cvtColor(img_padding, cv2.COLOR_GRAY2RGB)
            results = pose.process(image)

            if not results.pose_landmarks:
                res.append('판단 불가')
                continue

            # background
            annotated_image = image.copy()
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = (192, 192, 192)
            annotated_image = np.where(condition, annotated_image, bg_image)

            # draw
            mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(), )  # (1920, 1920, 3)

            annotated_image = cv2.resize(annotated_image, (192, 192))  # (192, 192, 3)
            target = annotated_image.astype(np.float32) / 255. # (192, 192, 3)
            annotated_image = np.expand_dims(annotated_image, axis=0)

        prediction = model.predict(annotated_image)  # <class 'numpy.ndarray'>
        label = CLASSES[prediction.argmax()]
        res.append(label)

    # 방법1) 라벨을 숫자로 리턴 -> node에서 변환
    # 방법2) 라벨을 클래스명으로 바꿔서 리턴
    return f'{res}'

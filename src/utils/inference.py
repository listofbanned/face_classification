import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image

import face_recognition

def load_image(image_path, grayscale=False, color_mode='rgb', target_size=None):
    pil_image = image.load_img(image_path, grayscale, color_mode, target_size)
    return image.img_to_array(pil_image)

def load_detection_model(model_path):
    detection_model = cv2.CascadeClassifier(model_path)
    return detection_model

def detect_faces(detection_model, gray_image_array):
    return detection_model.detectMultiScale(gray_image_array, 1.3, 5)

###
def reorder_coordinates(detected_faces):
    faces = []
    for top, right, bottom, left in detected_faces:
        x1, x2, y1, y2 = left, right, top, bottom
        x, y, w, h = x1, y1, x2 - x1, y2 - y1
        faces.append([x, y, w, h])

    return np.asarray(faces)

def detect_rgb_faces(image):
    detect_faces = face_recognition.face_locations(image)
    return reorder_coordinates(detect_faces)
###

def draw_bounding_box(face_coordinates, image_array, color):
    x, y, w, h = face_coordinates
    cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)

def apply_offsets(face_coordinates, offsets):
    x, y, width, height = face_coordinates
    x_off, y_off = offsets
    return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)

def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0,
                                                font_scale=2, thickness=2):
    x, y = coordinates[:2]
    cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA)

def get_colors(num_classes):
    colors = plt.cm.hsv(np.linspace(0, 1, num_classes)).tolist()
    colors = np.asarray(colors) * 255
    return colors


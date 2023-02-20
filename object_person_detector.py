# import the packages and modules needed
import streamlit as st
import pandas as pd
import cv2 as cv
import cvlib
from cvlib.object_detection import draw_bbox

# Title of the website
st.markdown("<h1 style='text-align: center; color: white;'>Object-Person Detector</h1>",
            unsafe_allow_html=True)

if 'detector' not in st.session_state:
    st.session_state['detector'] = 0

# Make a list for the objects that can be detected (Source: https://github.com/leggedrobotics/darknet_ros/blob/master/README.md)
list_of_objects = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                   'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

# Define a function for the webcam picture processing


def picture_process(img_file):
    with open("temp.png", "wb") as f:
        f.write(img_file.getbuffer())

    img = cv.imread("temp.png")
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    bbox, label, conf = cvlib.detect_common_objects(img)

    for i in range(len(label)):
        if label[i] not in list_of_objects:
            bbox.pop(i)
            label.pop(i)
            conf.pop(i)
    output_image = draw_bbox(img, bbox, label, conf)
    st.session_state.detector = len(label)

    # Making a list to store the name of the labels that was detected
    detected_things_label = []
    detected_things_confidence_level = []

    # looping through the labels and confidence level
    for l, c in zip(label, conf):
        detected_things_label.append(l)
        detected_things_confidence_level.append(c)

    # store the labels and confidence level in the session
    st.session_state.store_label = detected_things_label
    st.session_state.store_confidence_level = (
        detected_things_confidence_level)

    # returning the image back at the bottom after the image is processed
    return output_image


# For uploading picture
file_upload = st.file_uploader("Upload a file", type=['png'])
if file_upload:
    with open("picture.jpg", "wb") as f:
        f.write(file_upload.getbuffer())
    img = cv.imread("picture.jpg")
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    bbox, label, conf = cvlib.detect_common_objects(img)
    for i in range(len(label)):
        if label[i] not in list_of_objects:
            bbox.pop(i)
            label.pop(i)
            conf.pop(i)
    output_image = draw_bbox(img, bbox, label, conf)
    st.image(output_image)
    st.session_state.detector = len(label)

    # Making a list to store the name of the labels that was detected
    detected_things_label = []
    detected_things_confidence_level = []

    # looping through the labels and confidence level
    for l, c in zip(label, conf):
        detected_things_label.append(l)
        detected_things_confidence_level.append(c)

     # store the labels and confidence level in the session
    st.session_state.store_label = detected_things_label
    st.session_state.store_confidence_level = (
        detected_things_confidence_level)

    # Displaying the results in a table form by using panda DataFrame
    st.write(pd.DataFrame({
        'Things Detected': st.session_state.store_label,
        'Confidence Level': st.session_state.store_confidence_level,
    }))

# make a horizontal line to separate the file uploader and the webcam
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True)

# For webcam
picture = st.camera_input('Webcam')
if picture:
    st.image(picture_process(picture))

    # Displaying the results in a table form by using panda DataFrame
    st.write(pd.DataFrame({
        'Things Detected': st.session_state.store_label,
        'Confidence Level': st.session_state.store_confidence_level,
    }))

import os
from flask import Flask, request, send_file
import face_recognition
import json
import util

app = Flask(__name__)

temp_filepath = os.path.abspath('temp')

# home
@app.route('/')
def index():
    return 'Welcome to FaceLockerAPI'

# create a face landmark
@app.route('/landmark', methods=['POST'])
def create_face_landmarks():
    if request.method == 'POST':

        f = request.files['image']
        f.save(os.path.join(temp_filepath, f.filename))
        img_list = os.listdir(temp_filepath)

        image = face_recognition.load_image_file(
            os.path.join(temp_filepath, img_list[0]))
        face_landmarks_list = face_recognition.face_landmarks(image)

        util.draw_landmarks(image, face_landmarks_list)

        util.flush_files('temp')

        return send_file(os.path.join(os.path.abspath('out'), 'out.png'), mimetype='image/jpg')


@app.route('/face',methods=['POST','DELETE','GET'])
def register_a_face():
    if request.method == 'POST':

        name = request.form.get('name')

        f = request.files['image']
        f.save(os.path.join(temp_filepath, f.filename))
        img_list = os.listdir(temp_filepath)

        image = face_recognition.load_image_file(
            os.path.join(temp_filepath, img_list[0]))

        encoded_image = face_recognition.face_encodings(image)[0]

        encoded_image_list = util.load_list()
        encoded_image_list.append({'name':name,'encoded_image':encoded_image})
        util.save_list(encoded_image_list)
        
        return "registered"

    if request.method == 'GET':
        encoded_image_list = util.load_list()
        return {'faces':encoded_image_list}

    if request.method == 'DELETE':
        util.save_list([])
        
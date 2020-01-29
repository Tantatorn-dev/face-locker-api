from PIL import Image, ImageDraw
import os
import shutil
import json

out_filepath = os.path.abspath('out')


def draw_landmarks(image, landmarks_list):
    pil_image = Image.fromarray(image)
    for landmark in landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Make the eyebrows into a nightmare
        d.polygon(landmark['left_eyebrow'], fill=(68, 54, 39, 128))
        d.polygon(landmark['right_eyebrow'], fill=(68, 54, 39, 128))
        d.line(landmark['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
        d.line(landmark['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

        # Gloss the lips
        d.polygon(landmark['top_lip'], fill=(150, 0, 0, 128))
        d.polygon(landmark['bottom_lip'], fill=(150, 0, 0, 128))
        d.line(landmark['top_lip'], fill=(150, 0, 0, 64), width=8)
        d.line(landmark['bottom_lip'], fill=(150, 0, 0, 64), width=8)

        # Sparkle the eyes
        d.polygon(landmark['left_eye'], fill=(255, 255, 255, 30))
        d.polygon(landmark['right_eye'], fill=(255, 255, 255, 30))

        # Apply some eyeliner
        d.line(landmark['left_eye'] + [landmark['left_eye'][0]],
               fill=(0, 0, 0, 110), width=6)
        d.line(landmark['right_eye'] + [landmark['right_eye']
                                        [0]], fill=(0, 0, 0, 110), width=6)
    pil_image.save(os.path.join(os.path.join(out_filepath), "out.png"))


def flush_files(folder):
    folder = os.path.abspath(folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def save_list(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


def load_list():
    with open('data.json', 'r') as f:
        data= json.load(f)
    return data
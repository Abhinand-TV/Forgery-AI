from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('certificate_forgery_model.h5')

def analyze_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0][0]

        if prediction > 0.7:
            return "Forged"
        elif prediction > 0.4:
            return "Suspicious"
        else:
            return "Authentic"

    except Exception as e:
        print(f"[CNN ERROR]: {e}")
        return "Suspicious"

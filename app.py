from flask import Flask, render_template, request
import os
import uuid
import magic
import shutil
from utils.ela import perform_ela
from utils.copy_move import detect_copy_move
from utils.ocr import extract_text
from utils.text_check import analyze_text
from utils.pdf_extract import convert_pdf_to_image
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_valid_image(file_path):
    try:
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type.startswith("image/")
    except Exception as e:
        print(f"[MIME Check Error]: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if not uploaded_file or uploaded_file.filename == '':
            return "No file uploaded", 400

        session_id = str(uuid.uuid4())[:8]
        session_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_path, exist_ok=True)

        filename = uploaded_file.filename
        ext = os.path.splitext(filename)[1]
        saved_file_path = os.path.join(session_path, 'original' + ext)
        uploaded_file.save(saved_file_path)

        try:
            # Convert PDF to image
            if filename.lower().endswith('.pdf'):
                try:
                    converted_image_path = convert_pdf_to_image(saved_file_path, output_folder=session_path)
                    saved_file_path = converted_image_path  # use image path for analysis
                except Exception as e:
                    print(f"[PDF Conversion Error]: {e}")
                    shutil.rmtree(session_path)
                    return "Failed to convert PDF to image. Please use a different file.", 400

            if not is_valid_image(saved_file_path):
                shutil.rmtree(session_path)
                return "Unsupported file type. Please upload a valid image or PDF.", 400

            try:
                with Image.open(saved_file_path) as img:
                    img.verify()
            except UnidentifiedImageError:
                shutil.rmtree(session_path)
                return "Invalid or corrupted image file.", 400

            # Run Analysis Modules
            ela_result, ela_image_path = perform_ela(saved_file_path, session_path)
            cm_result, cm_image_path = detect_copy_move(saved_file_path, session_path)
            text = extract_text(saved_file_path)
            cnn_result = analyze_text(text)

            # Final verdict logic
            votes = [ela_result, cm_result, cnn_result]
            if votes.count("Forged") >= 2:
                final = "Forged"
            elif votes.count("Suspicious") >= 2:
                final = "Suspicious"
            else:
                final = "Authentic"

            return render_template(
                'index.html',
                ela_result=ela_result,
                cm_result=cm_result,
                cnn_result=cnn_result,
                final=final,
                ela_img=ela_image_path.replace('static/', ''),
                cm_img=cm_image_path.replace('static/', ''),
                user_img=saved_file_path.replace('static/', '')
            )

        except Exception as e:
            print(f"[ERROR during analysis]: {e}")
            shutil.rmtree(session_path)
            return "An error occurred during analysis. Please try again with another file.", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

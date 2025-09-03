import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from ocr.ocr_utils import extract_text, extract_boxes, draw_boxes

ALLOWED_EXT = {"png", "jpg", "jpeg", "tiff", "bmp"}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER
app.secret_key = "replace-with-env-secret"  # for production, set as env var

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            saved_name = f"{ts}_{filename}"
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_name)
            file.save(saved_path)

            # Extract text
            text = extract_text(saved_path)
            txt_name = saved_name + ".txt"
            txt_path = os.path.join(app.config['DATA_FOLDER'], txt_name)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            # Get boxes & annotated image
            boxes = extract_boxes(saved_path)
            annotated_name = "annot_" + saved_name
            annotated_path = os.path.join(app.config['UPLOAD_FOLDER'], annotated_name)
            draw_boxes(saved_path, boxes, annotated_path)

            return render_template("result.html",
                                   image_url=url_for("uploaded_file", filename=saved_name),
                                   annotated_url=url_for("uploaded_file", filename=annotated_name),
                                   text=text,
                                   txt_download=url_for("download_text", filename=txt_name))
    return render_template("index.html")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/download/<path:filename>")
def download_text(filename):
    return send_from_directory(app.config['DATA_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

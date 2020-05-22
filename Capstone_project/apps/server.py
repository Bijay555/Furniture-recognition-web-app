from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from utils import classify_image
import os
from flask_wtf.csrf import CSRFProtect
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 5000
port = int (os.getenv("VCAP_APP_PORT", 5000))

@app.route('/', methods=["GET", "POST"])
def root():
    if request.method == "GET":
        return render_template("index.html")
    else:
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            f = request.files["file"]
            if f.filename == "":
                flash("No selected file")
                return redirect(request.url)
            if f:
                filename = secure_filename(f.filename)
                
                # before saving this file, delete the old files in the sub-folder
                
                img_path = "image-file"
                img_path_images = os.getcwd() + "/" + img_path
                test_file_names=[os.path.join(img_path_images, f) for f in os.listdir(img_path_images) if f.endswith(".jpg") or f.endswith(".png")]
        
                for file_path in test_file_names:
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
                
                f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                api_key_user = app.config["API_KEY"]
                classifier_id = app.config["CLASSIFIER_ID"]
                results = classify_image(api_key_user, classifier_id)
                return render_template("classfied_results.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
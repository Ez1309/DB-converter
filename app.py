from flask import Flask, render_template, request, redirect, send_file, session
from werkzeug.utils import secure_filename 
from helpers import create_db, create_table, clean_files
import os
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./files/plans/"
app.secret_key = 'supersecretkey'

# Generate a unique ID for the session
unique_id = uuid.uuid4()

@app.route("/", methods=["GET", "POST"])
def index():
    # Clean up any existing files for the session and reset the session
    clean_files(session.get("id", None))
    session.pop("db_name", None)
    return redirect("/upload")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    # Upload session id and db_name
    session["id"] = unique_id
    db_name = session.pop("db_name", None)
    
    if request.method == "POST":
        file = request.files.get("file")
        view_file = request.files.get("table_file")
        db_name = request.form.get("db_name")
        
        # Create the db file from the first tab form
        if file:
            filename = f"{unique_id}_{secure_filename(file.filename)}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db_name = f"{unique_id}_{db_name}"
            create_db(filename, db_name)
            session["db_name"] = db_name

        # Create the html table data from the second tab form
        if view_file:
            filename = f"{unique_id}_{secure_filename(view_file.filename)}"
            view_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = create_table(filename)
            if isinstance(data, list):
                return render_template("table.html", data=data)
            elif isinstance(data, dict):
                return render_template("sheets.html", data=data)
    
    return render_template("index.html", db_name=db_name)

@app.route("/download/<db_name>", methods=["GET"])
def download_file(db_name):
    # Remove the user id from the .db file name and send it to download
    file_name = db_name.removeprefix(f"{unique_id}_") + ".db"
    file = f"./files/databases/{db_name}.db"
    return send_file(file, as_attachment=True, download_name=file_name)


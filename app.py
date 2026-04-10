# from flask import Flask, request, render_template
# import os

# app = Flask(__name__)

# # Folder to save images
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     name = request.form['name']
#     email = request.form['email']
#     file = request.files['image']

#     # Save file locally
#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)

#     return f"Uploaded Successfully! Name: {name}, Email: {email}, File: {file.filename}"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)





from flask import Flask, request, render_template
import boto3
import pymysql
import os

app = Flask(__name__)

# AWS S3 Config
S3_BUCKET = "your-bucket-name"
s3 = boto3.client('s3')

# RDS Config
db = pymysql.connect(
    host="your-rds-endpoint",
    user="admin",
    password="password",
    database="mydb"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    email = request.form['email']
    file = request.files['image']

    # Upload to S3
    s3.upload_fileobj(file, S3_BUCKET, file.filename)

    # Save to RDS
    cursor = db.cursor()
    sql = "INSERT INTO users (name, email, image) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, file.filename))
    db.commit()

    return "Uploaded Successfully!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory

app = Flask(__name__)

# Define exact folder structures
UPLOAD_FOLDER = 'uploads'
COMIC_FOLDER = os.path.join(UPLOAD_FOLDER, 'comics')
GALLERY_FOLDER = os.path.join(UPLOAD_FOLDER, 'gallery')
LINKS_FOLDER = os.path.join(UPLOAD_FOLDER, 'links')

# Ensure directories exist locally
for folder in [COMIC_FOLDER, GALLERY_FOLDER, LINKS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['SECRET_KEY'] = 'fazbear_secret_security_key'

# Serve uploaded files safely
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Main Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Admin Panel Page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# API Endpoints to let JavaScript fetch uploaded contents dynamically
@app.route('/api/data')
def get_data():
    comics = os.listdir(COMIC_FOLDER)
    gallery = os.listdir(GALLERY_FOLDER)
    
    # Read text files in links folder and combine text content
    links = []
    for file in os.listdir(LINKS_FOLDER):
        if file.endswith('.txt'):
            with open(os.path.join(LINKS_FOLDER, file), 'r', encoding='utf-8') as f:
                links.extend([line.strip() for line in f.readlines() if line.strip()])
                
    return jsonify({'comics': comics, 'gallery': gallery, 'links': links})

# Route for Admin Upload Processing
@app.route('/upload', methods=['POST'])
def handle_upload():
    upload_type = request.form.get('type')
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        if upload_type == 'comic' and file.filename.endswith('.pdf'):
            file.save(os.path.join(COMIC_FOLDER, file.filename))
        elif upload_type == 'gallery' and (file.filename.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif'))):
            file.save(os.path.join(GALLERY_FOLDER, file.filename))
        elif upload_type == 'link' and file.filename.endswith('.txt'):
            file.save(os.path.join(LINKS_FOLDER, file.filename))
        else:
            return "Invalid file format for this section!", 400
            
        return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
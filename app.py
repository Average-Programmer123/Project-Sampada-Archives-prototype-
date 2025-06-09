from flask import Flask, render_template, request, jsonify, url_for, redirect
import os
import json
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATA_FILE = 'main.json'
pic = "https://png.pngtree.com/png-vector/20190729/ourmid/pngtree-files-archive-data-database-documents-folders-abstract-circ-png-image_1622661.jpg"

# Sample data for tools
TOOLS = [
    {
        'id': 1,
        'name': 'Oral History Digitization Guide',
        'category': 'Documentation',
        'description': 'Step-by-step guide for recording and preserving oral histories',
        'link': '#'
    },
    {
        'id': 2,
        'name': '3D Scanning Best Practices',
        'category': 'Documentation',
        'description': 'Recommendations for 3D scanning of artifacts and monuments',
        'link': '#'
    },
    {
        'id': 3,
        'name': 'Community Engagement Toolkit',
        'category': 'Engagement',
        'description': 'Methods for involving local communities in preservation efforts',
        'link': '#'
    },
    {
        'id': 4,
        'name': 'Metadata Standards Handbook',
        'category': 'Standards',
        'description': 'UNESCO-approved metadata standards for heritage documentation',
        'link': '#'
    },
    {
        'id': 5,
        'name': 'Audio Archive',
        'category': 'Archive',
        'description': 'Archives of many Nepali music, books, languages etc.',
        'link': '/audio_kit'
    },
    {
        'id': 6,
        'name': 'Photo Archive',
        'category': 'Archive',
        'description': 'Archives of many old Photos and paintings of the past.',
        'link': '/photo_kit'
    }
]

# Sample case studies
CASE_STUDIES = [
    {
        'title': 'Immersive Digital Preservation of Mustang Architectural Caves',
        'location': 'Nepal',
        'description': 'This initiative proposes a scalable AR/VR platform to digitally preserve and showcase over 10,000 architectural caves in Mustang, Nepal, starting with 3D virtual tours using drone photogrammetry and LiDAR. It supports future expansions like AR apps, VR modules for education, and integration with global heritage platforms. By enabling continuous updates and open collaboration, the project ensures long-term conservation while positioning Nepal as a leader in digital heritage innovation.',
        'image': 'cave.jpg'
    },
    {
        'title': '3D Documentation of Angkor Wat',
        'location': 'Cambodia',
        'description': 'Using laser scanning to create detailed records of the temple complex',
        'image': '3d.jpg'
    },
    {
        'title': 'Community Archives of Intangible Heritage',
        'location': 'Brazil',
        'description': 'Empowering local communities to document their cultural practices',
        'image': 'brazil.jpg'
    }
]

def read():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            f.write('[]')

    with open(DATA_FILE, 'r') as f:
        content = f.read().strip()
        if not content:
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []

def write_audio_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tools')
def tools():
    return render_template('tools.html', tools=TOOLS)

@app.route('/best-practices')
def best_practices():
    return render_template('best-practices.html')

@app.route('/case-studies')
def case_studies():
    return render_template('case-studies.html', case_studies=CASE_STUDIES)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you would typically save this data or send an email
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

@app.route('/audio_kit', methods=['GET', 'POST'])
def audio_temp():
        audio_items = read()
        return render_template('audio_kit.html', audio_items=audio_items)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
     if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        sell = request.form.get('sel')
        file = request.files['imgg']
        audd = request.files['aud']
        date_created = time.strftime("%m/%d/%Y")

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)  # ✅ Ensure folder exists
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            img_url = url_for('static', filename='uploads/' + filename)
        else:
            img_url = pic  # fallback image
        
        if audd and audd.filename != '':
            audio_filename = secure_filename(audd.filename)
            audio_path = os.path.join('static', 'uploads', audio_filename)
            audd.save(audio_path)
            audio_url = url_for('static', filename='uploads/' + audio_filename)
        else:
            audio_url = None  # or a default/fallback audio file if you want

        audio_items = read()
        new_id = max([item['id'] for item in audio_items], default=0) + 1

        audio_items.append({
            'id': new_id,
            'name': name,
            'desc': desc,
            'date': date_created,
            'picture': img_url,
            'audio' : audio_url,
            'genre' : sell
        })
        print(sell)
        write_audio_data(audio_items)
        return redirect(url_for('upload'))

     audio_items = read()
    
     html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Audio</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                form {
                    margin-bottom: 20px;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 8px;
                    margin: 8px 0;
                    box-sizing: border-box;
                }
                input[type="submit"], .delete-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    margin-top: 8px;
                }
                input[type="submit"]:hover, .delete-btn:hover {
                    background-color: #45a049;
                }
                .audio-item {
                    margin-bottom: 15px;
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }
                .back-link {
                    display: inline-block;
                    margin-bottom: 20px;
                    color: #007BFF;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
        <div class="container">
            <h2>Upload Audio</h2>
            <form method="post" enctype="multipart/form-data">
                <label>Name:</label>
                <input type="text" name="name" required>
                <label>Description:</label>
                <input type="text" name="desc" required>
                <label>Image:</label>
                <input type="file" name="imgg" accept="image/*"><br>
                <label>Audio:</label>
                <input type="file" name="aud" accept="audio/*" ><br>
                <label>Audio genre:</label><br>
                <select id="sel" class="sel" name="sel">
                <option value="music">Music</option>
                <option value="music">Language</option>
                <option value="music">Book</option>
                </select><br>
                <input type="submit" value="Upload">
            </form>
            <a href="/" class="back-link">← Back to Home</a>
            <hr>
            <h3>Existing Audio Items</h3>
        '''

     for item in audio_items:
            html += f'''
            <div class="audio-item">
                <strong>{item["name"]}</strong> - {item["desc"]}
                <em>(Uploaded on {item.get("date", "Unknown")})</em>
                <form action="/delete/{item["id"]}" method="post" style="display:inline;">
                    <button type="submit" class="delete-btn">Delete</button>
                </form>
            </div>
            '''

     html += '''
            </div>
        </body>
        </html>
        '''
     return html

@app.route('/delete/<int:audio_id>', methods=['POST'])
def delete_audio(audio_id):
    audio_items = read()
    audio_items = [item for item in audio_items if item['id'] != audio_id]
    write_audio_data(audio_items)
    return redirect(url_for('audio_temp'))

@app.route('/api/tools')
def api_tools():
    return jsonify(TOOLS)

@app.route('/api/tools/<int:tool_id>')
def api_tool(tool_id):
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    return jsonify(tool) if tool else ('', 404)
@app.route('/photo_kit')
def show():
    return render_template('pic.html')
if __name__ == '__main__':
    app.run(debug=True)
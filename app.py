from flask import Flask, render_template, request, jsonify, url_for, redirect
import os
import json
import time
from werkzeug.utils import secure_filename
from datetime import datetime
import folium

app = Flask(__name__)
DATA_FILE = 'main.json'
pic = "https://png.pngtree.com/png-vector/20190729/ourmid/pngtree-files-archive-data-database-documents-folders-abstract-circ-png-image_1622661.jpg"
not1 = [{
    'name' : 'Khaptad National Park',
    'teaser':"A beautiful place in western Nepal known for it's scenic beauty and religious significance." ,
    'loc' : 'Doti, Accham, Bajura, Bajhang',
    'lat' : 29.382451,
    'lon' : 81.126995
},
       {
    'name' : 'Shuklaphanta National Park',
    'teaser':"A beautiful place in western Nepal with many species of animals and plants present." ,
    'loc' : 'Kanchanpur',
    'lat' : 28.858301,
    'lon' : 80.252842
    #more coming soon
}]
venues = [
    {
        'id': 1,
        'name': 'Syoyambhunath',
        'teaser': 'A major Buddhist Pilgrimage site in Kathmandu Metropolitan City.',
        'link': '/syoyambhunath',
        'image': '/static/images/content/syonath.jpeg',
        'unesco': 'UNESCO Listed',
        'loc': 'Kathmandu',
        'lat': 27.714709,
        'long': 85.290423
    },
    {
        'id': 2,
        'name': 'Pashupatinath',
        'teaser': 'A major ancient Hindu Pilgrimage site in Kathmandu metropolitan city.',
        'link': '/pashupatinath',
        'image': '/static/images/content/pashupati.jpeg',
        'unesco': 'UNESCO Listed',
        'loc': 'Kathmandu',
        'lat': 27.710068,
        'long': 85.348593
    },
    {
        'id': 3,
        'name': 'Basantapur Durbar Square',
        'teaser': 'A major religious and Pilgrimage site in Kathmandu Metropolitan City. It is also known as Kathmandu Durbar Square and Hanuman Dokha.',
        'link': '/basantapur',
        'image': '/static/images/content/basantapur.jpeg',
        'unesco': 'UNESCO Listed',
        'loc': 'Kathmandu',
        'lat': 27.704833,
        'long': 85.307562
    },
    {
        'id': 4,
        'name': 'Bhaktapur Durbar Square',
        'teaser': 'A major religious site in Bhaktapur Municipality.',
        'link': '/bhaktapur',
        'image': '/static/images/content/nyatapol.jpeg',
        'unesco': 'UNESCO Listed',
        'loc': 'Bhaktapur',
        'lat': 27.672413,
        'long': 85.428738
    },
    {
        'id': 5,
        'name': 'Patan Durbar Square',
        'teaser': 'A major religious place in Lalitpur Metropolitan City.',
        'link': '/patan',
        'image': '/static/images/content/basantapur.jpeg',
        'unesco': 'UNESCO Listed',
        'loc': 'Lalitpur',
        'lat': 27.673827,
        'long': 85.325055
    },
    {
        'id': 6,
        'name': 'Changu Narayan',
        'teaser': 'A major religious place in Changunarayan municipality of Bhaktapur. It is claimed to be the oldest temple of Nepal.',
        'link': '/changunarayan',
        'image': '/static/images/content/kttm.png',
        'unesco': 'UNESCO Listed',
        'loc': 'Bhaktapur',
        'lat': 27.716173,
        'long': 85.427874
    },
    {
        'id': 7,
        'name': 'Boudhanath',
        'teaser': 'A major Buddhist pilgrimage place in Kathmandu Metropolitan City.',
        'link': '/boudhanath',
        'image': '/static/images/content/kmc.png',
        'unesco': 'UNESCO Listed',
        'loc': 'Kathmandu',
        'lat': 27.721175,
        'long': 85.361932
    },
    {
        'id': 8,
        'name': 'Chitwan National Park',
        'teaser': 'Oldest National Park of Nepal, home to many ecosystem of animals and plants.',
        'link': '/chitwan-national-park',
        'image': '/static/images/content/sauraha.jpeg',
        'unesco': 'UNESCO Listed',
        'loc': 'Chitwan',
        'lat': 27.522692,
        'long': 84.326387
    },
    {
        'id': 9,
        'name': 'Lumbini',
        'teaser': 'A major Buddhist pilgrimage site renowned for being the birthplace of Lord Gautam Buddha.',
        'link': '/lumbini',
        'image': '/static/images/content/lumbini.png',
        'unesco': 'UNESCO Listed',
        'loc': 'Kapilvastu',
        'lat': 27.469477,
        'long': 83.275773
    },
    {
        'id': 10,
        'name': 'Sagarmatha National Park',
        'teaser': "Home to the world's tallest Mountain Sagarmatha or Mt. Everest in English. It is located in Solukhumbu District of Nepal.",
        'link': '/boudhanath',
        'image': 'https://www.nepalsanctuarytreks.com/wp-content/uploads/2018/09/Mt._Everest_from_Gokyo_Ri_November_5_2012-scaled.jpg',
        'unesco': 'UNESCO Listed',
        'loc': 'Solukhumbu',
        'lat': 27.985954,
        'long': 86.924352
    }
]
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
        'link': '/metadata'
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
        'image': 'cave.jpg',
        'link':'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwig19DG6v2NAxUlzTgGHaB7ECMQFnoECBgQAQ&url=https%3A%2F%2Fwhc.unesco.org%2Fdocument%2F206803&usg=AOvVaw04HQ7LMhBa0LQrlSFFqG4V&opi=89978449'
    },
    {
        'title': '3D Documentation of Angkor Wat',
        'location': 'Cambodia',
        'description': 'Using laser scanning to create detailed records of the temple complex',
        'image': '3d.jpg',
        'link' : 'https://www.researchgate.net/publication/253948834_Reality-based_3D_modeling_of_the_Angkorian_temples_using_aerial_images'
    },
    {
        'title': 'Community Archives of Intangible Heritage',
        'location': 'Brazil',
        'description': 'Empowering local communities to document their cultural practices',
        'image': 'brazil.jpg',
        'link' : 'https://www.unesco.org/en/fieldoffice/brasilia/expertise/world-cultural-heritage-brazil'
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
        time_created = time.strftime("%m/%d/%Y/%H/%M/%S")

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True) 
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            img_url = url_for('static', filename='uploads/' + filename)
        else:
            img_url = pic  
        
        if audd and audd.filename != '':
            audio_filename = secure_filename(audd.filename)
            audio_path = os.path.join('static', 'uploads', audio_filename)
            audd.save(audio_path)
            audio_url = url_for('static', filename='uploads/' + audio_filename)
        else:
            audio_url = None 

        audio_items = read()
        new_id = max([item['id'] for item in audio_items], default=0) + 1

        audio_items.append({
            'id': new_id,
            'name': name,
            'desc': desc,
            'date': date_created,
            'picture': img_url,
            'audio' : audio_url,
            'genre' : sell,
            'time' : time_created
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
                <input type="file" name="aud" accept="audio/*" required><br>
                <label>Audio genre:</label><br>
                <select id="sel" class="sel" name="sel">
                <option value="music">Music</option>
                <option value="music">Language</option>
                <option value="music">Book</option>
                </select><br>
                <input type="submit" value="Upload">
            </form>
            <a href="/audio_kit" class="back-link">← Back to Home</a>
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

def sort():
    with open('data.json', 'r') as f:
        data = json.load(f)
        
    data.sort(key=lambda x: datetime.fromisoformat(x['time']))
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    for item in data:
        print(item['name'], item['time'])
@app.route('/metadata')
def meta():
    fmap = folium.Map(location=[29.5, 84], zoom_start=6)

    for venue in venues:
        if 'loc' in venue and 'long' in venue:
            folium.Marker(
                location=[venue['lat'], venue['long']],  
                popup=folium.Popup(f"<strong><h1>{venue['name']}</h1></strong><br>{venue['teaser']}", max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(fmap)
    for ven in not1:
        if 'loc' in ven and 'lon' in ven:
         folium.Marker(
            location=[ven['lat'], ven['lon']],
            popup=folium.Popup(f"<strong><h1>{ven['name']}</h1></strong><br><strong style='color:gray'><h6>{ven['loc']}</h6></strong><br><br>{ven['teaser']}", max_width=300),
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(fmap)

    fmap.get_root().html.add_child(folium.Element("""
    <style>
        #map {
            border-radius: 20px;
            overflow: hidden;
        }
    </style>
"""))
    map_html = fmap._repr_html_()
    return render_template('metadata.html', venues=venues, map_html=map_html)
print("Adding non-UNESCO venues:")
for ven in not1:
    print(ven['name'])

if __name__ == '__main__':
    app.run(debug=True)

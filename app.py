from flask import Flask, render_template, url_for, redirect, request, send_from_directory
from GenerateMidi import generate_music
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


app = Flask(__name__)
# template_folder="Bootstrap-4/Bootstrap 4 Site Files" static_folder = 'img'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/downloadmidi')
def download_file():
    return send_from_directory("./static/songs", 'newPianoSong.mid', as_attachment=True)


@app.route('/', methods=['POST'])
def predictonImage():
    if request.method == 'POST':
        generate_music()
        return redirect('/downloadmidi')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)

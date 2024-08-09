from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
import yt_dlp as youtube_dl
import os

app = Flask(__name__)
CORS(app)

# Path to store downloads and valid links
DOWNLOAD_FOLDER = './downloads'
VALID_LINKS_FILE = './valid_links.txt'

@app.route('/download', methods=['POST'])
def download_video():
    with open(VALID_LINKS_FILE, 'r') as file:
        urls = file.readlines()

    current_index = int(request.cookies.get('last_index', '0'))
    if current_index >= len(urls):
        current_index = 0  # Reset to the first link if we reach the end

    url = urls[current_index].strip()
    next_index = (current_index + 1) % len(urls)

    def progress_hook(d):
        if d['status'] == 'finished':
            with open('/tmp/progress.txt', 'w') as f:
                f.write(f"Download completed: {d['filename']}")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'cookiefile': './cookies.txt',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
        return jsonify({'message': 'Download started', 'filename': filename, 'next_index': next_index}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress', methods=['GET'])
def get_progress():
    if os.path.exists('/tmp/progress.txt'):
        with open('/tmp/progress.txt', 'r') as f:
            progress = f.read()
        return jsonify({'progress': progress}), 200
    else:
        return jsonify({'progress': 'No download progress available'}), 200

@app.route('/video/<filename>', methods=['GET'])
def stream_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

@app.route('/delete_video', methods=['POST'])
def delete_video():
    filename = request.json.get('filename')
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'Video deleted'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

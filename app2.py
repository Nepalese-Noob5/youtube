from flask import Flask, request, jsonify, send_from_directory
import yt_dlp as youtube_dl
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = './downloads'
VALID_LINKS_FILE = './valid_links.txt'

@app.route('/download', methods=['POST'])
def download_video():
    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'No key provided'}), 400

    with open(VALID_LINKS_FILE, 'r') as file:
        lines = file.readlines()

    url = None
    for line in lines:
        if line.startswith(f"{key}="):
            url = line.split('=')[1].strip()
            break

    if not url:
        return jsonify({'error': 'No video found for the given key'}), 404

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
        return jsonify({'message': 'Download started', 'filename': filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Existing routes for progress, stream_video, and delete_video remain the same.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


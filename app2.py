from flask import Flask, request, jsonify
import yt_dlp as youtube_dl
import os
import time
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

DOWNLOAD_FOLDER = './downloads'
VALID_LINKS_FILE = './valid_links.txt'
COOKIES_FILE = './cookies.txt'

@app.route('/download', methods=['POST'])
def download_video():
    key = request.args.get('key')
    if not key:
        logging.error("No key provided.")
        return jsonify({'error': 'No key provided'}), 400

    # Retrieve URL using the provided key
    url = None
    try:
        with open(VALID_LINKS_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(f"{key}="):
                    url = line.split('=')[1].strip()
                    break
    except Exception as e:
        logging.error(f"Error reading valid links file: {str(e)}")
        return jsonify({'error': 'Error reading valid links file'}), 500

    if not url:
        logging.error(f"No video found for the given key: {key}.")
        return jsonify({'error': 'No video found for the given key'}), 404

    # Define a hook to log progress
    def progress_hook(d):
        if d['status'] == 'finished':
            with open('/tmp/progress.txt', 'w') as f:
                f.write(f"Download completed: {d['filename']}")
            logging.info(f"Download completed: {d['filename']}")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'cookiefile': COOKIES_FILE,
    }

    # Retry mechanism to handle HTTP 429
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
            logging.info(f"Download started for key: {key}, filename: {filename}.")
            return jsonify({'message': 'Download started', 'filename': filename}), 200
        except Exception as e:
            if "HTTP Error 429" in str(e):
                logging.warning(f"Rate limit hit. Retrying in {30 * (attempt + 1)} seconds...")
                time.sleep(30 * (attempt + 1))
            else:
                logging.error(f"Error: {str(e)}")
                return jsonify({'error': str(e)}), 500

    logging.error("Max retries reached. Could not download the video.")
    return jsonify({'error': 'Failed to download due to rate limiting'}), 429

# Existing routes for progress, stream_video, and delete_video remain the same.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

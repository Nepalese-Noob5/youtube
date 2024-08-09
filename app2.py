from flask import Flask, request, jsonify
import youtube_dl
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    def progress_hook(d):
        if d['status'] == 'finished':
            # Save the progress information
            with open('/tmp/progress.txt', 'w') as f:
                f.write(f"Download completed: {d['filename']}")

    ydl_opts = {
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],  # Hook for progress updates
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download started'}), 200
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

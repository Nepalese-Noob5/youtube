from flask import Flask, request, jsonify, send_file, after_this_request, Response
import yt_dlp
import os

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_DIRECTORY = "./downloads"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

@app.route('/')
def index():
    return "Welcome to the YouTube Downloader!"

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    video_filename = None

    # Set up yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'cookiefile': './cookies.txt',  # Ensure this path is correct
        'progress_hooks': [progress_hook],  # Hook for progress updates
    }

    def progress_hook(d):
        nonlocal video_filename
        if d['status'] == 'finished':
            video_filename = d['filename']
        # Add progress tracking logic if needed

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not video_filename or not os.path.exists(video_filename):
            return jsonify({'error': 'Video download failed'}), 500

        @after_this_request
        def remove_file(response):
            try:
                os.remove(video_filename)
            except Exception as error:
                print(f"Error removing file {video_filename}: {error}")
            return response

        video_url = f'/serve_video/{os.path.basename(video_filename)}'
        return jsonify({'video_url': video_url})

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/serve_video/<filename>')
def serve_video(filename):
    video_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
    if os.path.exists(video_path):
        return send_file(video_path)
    else:
        return "Video not found", 404

@app.route('/progress')
def get_progress():
    # Dummy progress endpoint for demonstration purposes
    # Replace with actual progress tracking if needed
    progress = {"percent": 75}  # Example static progress
    return jsonify(progress)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

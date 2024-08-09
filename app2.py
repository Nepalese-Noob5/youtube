from flask import Flask, request, jsonify, send_file, after_this_request
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
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Set up yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'cookiefile': './cookies.txt',  # Ensure this path is correct
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_filename = ydl.prepare_filename(info_dict)

        if not video_title or not os.path.exists(video_filename):
            return jsonify({'error': 'Video download failed'}), 500

        @after_this_request
        def remove_file(response):
            try:
                os.remove(video_filename)
            except Exception as error:
                print(f"Error removing file {video_filename}: {error}")
            return response

        return send_file(video_filename, as_attachment=True)

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

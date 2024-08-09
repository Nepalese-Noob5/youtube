from flask import Flask, request, jsonify, send_file, after_this_request, make_response
import yt_dlp
import os

app = Flask(__name__)

# Directory to store downloaded videos
DOWNLOAD_DIRECTORY = "./downloads"

if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

def download_from_youtube(url):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        video_ext = info_dict.get('ext', None)
        video_file_path = f"{DOWNLOAD_DIRECTORY}/{video_title}.{video_ext}"
        return video_file_path

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        video_file_path = download_from_youtube(url)

        if not os.path.exists(video_file_path):
            return jsonify({"error": "Video not found or download failed."}), 400

        # Construct the full URL for the downloaded video
        video_url = request.host_url + 'static/' + os.path.basename(video_file_path)

        # Set a cookie with the video URL
        resp = make_response(jsonify({"video_url": video_url}))
        resp.set_cookie('last_downloaded_video', video_url, max_age=60*60)  # Cookie expires in 1 hour

        @after_this_request
        def remove_file(response):
            try:
                os.remove(video_file_path)
            except Exception as error:
                print(f"Error removing or closing downloaded file handle: {error}")
            return response

        return resp

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<filename>')
def serve_video(filename):
    return send_file(os.path.join(DOWNLOAD_DIRECTORY, filename))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

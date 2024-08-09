from flask import Flask, request, jsonify, send_file, render_template_string, after_this_request
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
        video_file_path = os.path.join(DOWNLOAD_DIRECTORY, f"{video_title}.{video_ext}")
        return video_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        try:
            video_file_path = download_from_youtube(url)

            if not os.path.exists(video_file_path):
                return jsonify({"error": "Video not found or download failed."}), 400

            video_url = request.host_url + 'static/' + os.path.basename(video_file_path)

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(video_file_path)
                except Exception as error:
                    print(f"Error removing or closing downloaded file handle: {error}")
                return response

            # Simple HTML template to show video
            html = '''
            <!doctype html>
            <html>
            <head><title>Video Player</title></head>
            <body>
                <h1>Video Player</h1>
                <video width="640" height="360" controls>
                    <source src="{{ video_url }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <br><br>
                <form action="/" method="post">
                    <input type="text" name="url" placeholder="Enter YouTube URL" size="50">
                    <input type="submit" value="Download and Play">
                </form>
            </body>
            </html>
            '''

            return render_template_string(html, video_url=video_url)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Simple HTML form for entering the YouTube URL
    html = '''
    <!doctype html>
    <html>
    <head><title>YouTube Video Downloader</title></head>
    <body>
        <h1>YouTube Video Downloader</h1>
        <form action="/" method="post">
            <input type="text" name="url" placeholder="Enter YouTube URL" size="50">
            <input type="submit" value="Download and Play">
        </form>
    </body>
    </html>
    '''

    return render_template_string(html)

@app.route('/static/<filename>')
def serve_video(filename):
    return send_file(os.path.join(DOWNLOAD_DIRECTORY, filename))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

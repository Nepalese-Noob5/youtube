from flask import Flask, Response, request
import requests

app = Flask(__name__)

# Load video links from file
with open('valid_links.txt') as file:
    links = [line.strip().split('= ')[1] for line in file if '= ' in line]

@app.route('/video')
def video():
    index = int(request.args.get('index', 0))
    if index < 0 or index >= len(links):
        return "Invalid index", 404
    
    video_url = links[index]
    response = requests.get(video_url, stream=True)
    return Response(response.iter_content(chunk_size=1024), content_type='video/mp4')

@app.route('/next')
def next_video():
    index = int(request.args.get('index', 0))
    index = (index + 1) % len(links)
    return f'<a href="/video?index={index}">Watch Next Video</a>'

@app.route('/prev')
def prev_video():
    index = int(request.args.get('index', 0))
    index = (index - 1) % len(links)
    return f'<a href="/video?index={index}">Watch Previous Video</a>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    

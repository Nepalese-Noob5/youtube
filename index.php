<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <script>
        function downloadVideo() {
            var url = document.getElementById('videoURL').value;
            if (!url) {
                document.getElementById('status').innerText = 'Error: No URL provided.';
                return;
            }

            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'https://youtube-c6ei.onrender.com/download', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                if (xhr.status === 200) {
                    document.getElementById('status').innerText = 'Download started.';
                    checkProgress();
                } else {
                    document.getElementById('status').innerText = 'Error: ' + xhr.responseText;
                }
            };
            xhr.send('url=' + encodeURIComponent(url));
        }

        function checkProgress() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'https://youtube-c6ei.onrender.com/progress', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    var progress = JSON.parse(xhr.responseText).progress;
                    document.getElementById('progress').innerText = 'Download Progress: ' + progress;
                }
            };
            xhr.send();
        }
    </script>
</head>
<body>
    <h1>YouTube Video Downloader</h1>
    <form onsubmit="event.preventDefault(); downloadVideo();">
        <label for="videoURL">YouTube Video URL:</label>
        <input type="text" id="videoURL" name="videoURL" required>
        <button type="submit">Download</button>
    </form>
    <p id="status"></p>
    <p id="progress">Download Progress: 0%</p>
</body>
</html>

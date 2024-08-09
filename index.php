<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        label, button {
            display: block;
            margin: 10px 0;
        }
    </style>
    <script>
        async function downloadVideo() {
            const url = document.getElementById('url').value;
            if (!url) {
                alert('Please enter a YouTube video URL.');
                return;
            }

            try {
                const response = await fetch('https://youtube-c6ei.onrender.com/download', {  // Replace 'your-server-address' with your Render app's address
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `url=${encodeURIComponent(url)}`
                });

                if (response.ok) {
                    document.getElementById('status').innerText = 'Download started...';
                    checkProgress();
                } else {
                    const error = await response.json();
                    document.getElementById('status').innerText = `Error: ${error.error}`;
                }
            } catch (error) {
                document.getElementById('status').innerText = `Error: ${error.message}`;
            }
        }

        async function checkProgress() {
            try {
                const response = await fetch('https://youtube-c6ei.onrender.com/progress');  // Replace 'your-server-address' with your Render app's address
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('progress').innerText = data.progress || 'No progress available';
                    if (data.progress && !data.progress.includes('completed')) {
                        setTimeout(checkProgress, 5000); // Check progress every 5 seconds
                    }
                } else {
                    document.getElementById('progress').innerText = 'Failed to retrieve progress';
                }
            } catch (error) {
                document.getElementById('progress').innerText = `Error: ${error.message}`;
            }
        }
    </script>
</head>
<body>
    <h1>YouTube Video Downloader</h1>
    <form onsubmit="event.preventDefault(); downloadVideo();">
        <label for="url">YouTube Video URL:</label>
        <input type="text" id="url" name="url" placeholder="Enter YouTube video URL" required>
        <button type="submit">Download</button>
    </form>
    <p id="status"></p>
    <p id="progress">Download Progress: 0%</p>
</body>
</html>

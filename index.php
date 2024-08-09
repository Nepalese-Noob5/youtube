<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader & Player</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #fff;
            color: #000;
        }
        body.dark-mode {
            background-color: #121212;
            color: #ffffff;
        }
        #video-player {
            display: none;
            margin-top: 20px;
            width: 100%;
            max-width: 600px;
        }
        .controls {
            margin: 10px 0;
        }
        .key-input {
            margin-top: 10px;
        }
    </style>
    <script>
        let currentIndex = 0;

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            const mode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            document.cookie = `mode=${mode};path=/;max-age=31536000`;
        }

        async function downloadVideo() {
            const key = document.getElementById('video-key').value;
            if (!key) {
                alert("Please enter a valid key.");
                return;
            }

            try {
                const response = await fetch(`https://youtube-c6ei.onrender.com/download?key=${key}`, {
                    method: 'POST'
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('status').innerText = 'Download started...';
                    checkProgress();
                    playVideo(data.filename, data.next_index);
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
                const response = await fetch('https://youtube-c6ei.onrender.com/progress');
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('progress').innerText = data.progress || 'No progress available';
                    if (data.progress && !data.progress.includes('completed')) {
                        setTimeout(checkProgress, 5000);
                    }
                } else {
                    document.getElementById('progress').innerText = 'Failed to retrieve progress';
                }
            } catch (error) {
                document.getElementById('progress').innerText = `Error: ${error.message}`;
            }
        }

        async function playVideo(filename, nextIndex) {
            document.getElementById('video-player').src = `http://127.0.0.1:5000/video/${filename}`;
            document.getElementById('video-player').style.display = 'block';
            document.cookie = `last_index=${nextIndex};path=/;max-age=31536000`;  // Save next video index
        }

        async function deleteAndNext() {
            const filename = document.getElementById('video-player').src.split('/').pop();
            const response = await fetch('https://youtube-c6ei.onrender.com/delete_video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: filename })
            });

            if (response.ok) {
                document.getElementById('video-player').style.display = 'none';
                const userConfirmed = confirm('Enter number to proceed:');
                if (userConfirmed) {
                    downloadVideo();
                }
            } else {
                alert('Error deleting video');
            }
        }

        window.onload = () => {
            const mode = document.cookie.split('; ').find(row => row.startsWith('mode='));
            if (mode && mode.split('=')[1] === 'dark') {
                document.body.classList.add('dark-mode');
            }
        };
    </script>
</head>
<body>
    <h1>YouTube Video Downloader & Player</h1>
    <button onclick="toggleDarkMode()">Toggle Dark/Light Mode</button>
    <p id="status"></p>
    <p id="progress">Download Progress: 0%</p>

    <div class="key-input">
        <label for="video-key">Enter Video Key: </label>
        <input type="text" id="video-key" name="video-key" placeholder="e.g., 9">
        <button onclick="downloadVideo()">Download Video</button>
    </div>

    <div class="controls">
        <button onclick="deleteAndNext()">Next Video</button>
    </div>
    <video id="video-player" controls></video>
</body>
</html>

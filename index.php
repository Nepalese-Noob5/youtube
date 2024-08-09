<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
</head>
<body>
    <h1>YouTube Video Downloader</h1>

    <!-- Form to accept YouTube URL -->
    <form action="" method="post">
        <label for="url">YouTube URL:</label>
        <input type="text" id="url" name="url" required>
        <input type="submit" value="Download">
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $url = $_POST['url'];

        // Make a POST request to your Flask app to download the video
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://webyou.onrender.com/download');
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array('url' => $url)));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        // Get the response from the Flask app
        $response = curl_exec($ch);
        curl_close($ch);

        // Decode the JSON response
        $data = json_decode($response, true);

        if (isset($data['video_url'])) {
            // Display the downloaded video in the browser
            echo '<h2>Downloaded Video</h2>';
            echo '<video width="640" height="360" controls>';
            echo '<source src="' . htmlspecialchars($data['video_url']) . '" type="video/mp4">';
            echo 'Your browser does not support the video tag.';
            echo '</video>';
        } else {
            // Show an error message if the download failed
            echo '<p>Error: ' . htmlspecialchars($data['error']) . '</p>';
        }
    }
    ?>

</body>
</html>

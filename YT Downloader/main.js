const fs = require('fs');
const { exec } = require('child_process');
const readlineSync = require('readline-sync');
const path = require('path');

const checkIfPlaylist = (url, callback) => {
  exec(`yt-dlp --print "is_playlist" "${url}"`, (error, stdout, stderr) => {
    if (error || stderr) {
      console.error(`Error checking URL: ${stderr || error.message}`);
      return callback(null);
    }
    
    const isPlaylist = stdout.trim() === 'yes';
    callback(isPlaylist);
  });
};

const getTitle = (url, callback) => {
  exec(`yt-dlp --print "%(title)s" "${url}"`, (error, stdout, stderr) => {
    if (error || stderr) {
      console.error(`Error getting title: ${stderr || error.message}`);
      return callback(null);
    }

    const cleanTitle = stdout.trim().replace(/[<>:"/\\|?*]+/g, '_'); // Remove invalid characters
    callback(cleanTitle);
  });
};

const getPlaylistSize = (url, callback) => {
  exec(`yt-dlp --print "%(playlist_count)s" "${url}"`, (error, stdout, stderr) => {
    if (error || stderr) {
      console.error(`Error fetching playlist size: ${stderr || error.message}`);
      return callback(null);
    }

    const size = parseInt(stdout.trim(), 10);
    callback(isNaN(size) ? null : size);
  });
};

const checkDownloadCompletion = (folderPath, expectedCount) => {
  fs.readdir(folderPath, (err, files) => {
    if (err) {
      console.error(`Error reading download folder: ${err.message}`);
      return;
    }

    const downloadedFiles = files.filter(file => file.endsWith('.mp3') || file.endsWith('.mp4')).length;

    if (downloadedFiles >= expectedCount) {
      console.log(`✅ All ${expectedCount} files were successfully downloaded!`);
    } else {
      console.log(`⚠️ Download incomplete! Expected ${expectedCount}, but only found ${downloadedFiles} files.`);
    }
  });
};

const downloadMedia = (url, format, isPlaylist) => {
  getTitle(url, (title) => {
    if (!title) {
      console.log("Could not fetch title. Downloading to default folder.");
      title = "Unknown"; // Fallback in case the title couldn't be fetched
    }

    const folderPath = path.join(__dirname, 'Downloads', title);

    if (!fs.existsSync(folderPath)) {
      fs.mkdirSync(folderPath, { recursive: true });
    }

    if (isPlaylist) {
      getPlaylistSize(url, (playlistSize) => {
        if (!playlistSize) {
          console.log("Could not determine playlist size.");
          return;
        }

        const outputFormat = path.join(folderPath, '%(title)s.%(ext)s');

        const extraFlags = `--user-agent "com.google.android.youtube/17.10.35 (Linux; U; Android 11)" --force-insecure --no-check-formats --no-youtube-unavailable-fragments`;

        const command = format === 'mp3'
          ? `yt-dlp -x --audio-format mp3 --progress -o "${outputFormat}" "${url}"`
          : `yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 --progress -o "${outputFormat}" "${url}"`;

        console.log(`\nDetected: Playlist (${playlistSize} videos)`);
        console.log(`Saving in folder: ${folderPath}`);
        console.log(`Downloading ${format.toUpperCase()}...`);
        console.log(`Running command: ${command}\n`);

        const downloadProcess = exec(command, (error, stdout, stderr) => {
          if (error) {
            console.error(`Error: ${error.message}`);
            return;
          }
          if (stderr) {
            console.error(`yt-dlp error: ${stderr}`);
            return;
          }
          console.log(stdout);
          console.log(`Download complete! Files saved in: ${folderPath}`);

          // Check if all videos were downloaded
          checkDownloadCompletion(folderPath, playlistSize);
        });

        downloadProcess.stdout.on('data', (data) => {
          process.stdout.write(data);
        });
      });
    } else {
      // Single video download
      const outputFormat = path.join(folderPath, '%(title)s.%(ext)s');
      const command = format === 'mp3'
        ? `yt-dlp -x --audio-format mp3 --progress -o "${outputFormat}" "${url}"`
        : `yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 --progress -o "${outputFormat}" "${url}"`;

      console.log(`\nDetected: Single Video`);
      console.log(`Saving in folder: ${folderPath}`);
      console.log(`Downloading ${format.toUpperCase()}...`);
      console.log(`Running command: ${command}\n`);

      const downloadProcess = exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error: ${error.message}`);
          return;
        }
        if (stderr) {
          console.error(`yt-dlp error: ${stderr}`);
          return;
        }
        console.log(stdout);
        console.log(`Download complete! File saved in: ${folderPath}`);
      });

      downloadProcess.stdout.on('data', (data) => {
        process.stdout.write(data);
      });
    }
  });
};

const promptForUrl = () => {
  const url = readlineSync.question('Paste the YouTube video or playlist URL: ');

  checkIfPlaylist(url, (isPlaylist) => {
    if (isPlaylist === null) {
      console.log('Invalid URL or error detecting type. Please try again.');
      return promptForUrl();
    }

    // Ask format whether it's a single video or a playlist
    const format = readlineSync.question('Download MP4 (video) or MP3 (audio)? (Enter "mp4" or "mp3"): ').toLowerCase();
    
    if (format === 'mp4' || format === 'mp3') {
      downloadMedia(url, format, isPlaylist);
    } else {
      console.log('Invalid format. Please enter "mp4" or "mp3".');
      promptForUrl();
    }
  });
};

promptForUrl();

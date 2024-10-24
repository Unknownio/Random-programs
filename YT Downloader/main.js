const fs = require('fs');
const { exec } = require('child_process');
const readlineSync = require('readline-sync');
const path = require('path');

// Function to download audio or video using yt-dlp
const downloadMedia = (url, format) => {
  // Command to get the video title for naming
  const titleCommand = `yt-dlp -e "${url}"`;

  exec(titleCommand, (error, title) => {
    if (error) {
      console.error(`Error fetching title: ${error.message}`);
      return;
    }

    // Clean the title for file system compatibility
    const cleanTitle = title.trim().replace(/[<>:"/\\|?*]+/g, '_'); // Replace invalid characters
    const extension = format === 'mp3' ? 'mp3' : 'mp4';
    const filePath = path.join(__dirname, 'Downloads', `${cleanTitle}.${extension}`);

    // Ensure the Downloads folder exists
    if (!fs.existsSync(path.join(__dirname, 'Downloads'))) {
      fs.mkdirSync(path.join(__dirname, 'Downloads'));
    }

    // Command to download the media based on the user's choice (MP4 or MP3), with progress
    const command = format === 'mp3'
      ? `yt-dlp -x --audio-format mp3 --progress -o "${filePath}" "${url}"`
      : `yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 --progress -o "${filePath}" "${url}"`;

    console.log(`Downloading ${format.toUpperCase()}...`);

    // Start downloading the media
    const downloadProcess = exec(command);

    // Output download progress in real-time
    downloadProcess.stdout.on('data', (data) => {
      process.stdout.write(data); // Display yt-dlp's native progress output (speed, ETA, etc.)
    });

    downloadProcess.on('close', (code) => {
      process.stdout.write('\n'); // Move to a new line after completion
      if (code !== 0) {
        console.error(`Download process exited with code ${code}`);
        return;
      }

      console.log(`${format.toUpperCase()} downloaded: ${filePath}`);

      // Ask user if they want to download another video
      const another = readlineSync.keyInYNStrict('Do you want to download another video?');
      if (another) {
        promptForUrl(); // Start over if the user wants to download again
      } else {
        console.log('Goodbye ^^');
      }
    });
  });
};

// Function to prompt user for YouTube URL and format
const promptForUrl = () => {
  const url = readlineSync.question('Paste the YouTube video URL: ');

  // Validate URL using a basic check
  if (url.startsWith('https://www.youtube.com/watch?v=')) {
    // Ask the user whether they want to download MP4 (video) or MP3 (audio)
    const format = readlineSync.question('Do you want to download MP4 (video) or MP3 (audio)? (Enter "mp4" or "mp3"): ').toLowerCase();

    if (format === 'mp4' || format === 'mp3') {
      downloadMedia(url, format); // Proceed with the chosen format
    } else {
      console.log('Invalid format. Please enter "mp4" or "mp3".');
      promptForUrl(); // Ask again if the input is invalid
    }
  } else {
    console.log('Invalid URL. Please try again.');
    promptForUrl(); // Ask for the URL again
  }
};

// Start the process
promptForUrl();

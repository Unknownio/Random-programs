const fs = require('fs');
const { exec } = require('child_process');
const readlineSync = require('readline-sync');
const path = require('path');

// Function to show a loading indicator
const showLoadingIndicator = () => {
  const indicator = setInterval(() => {
    process.stdout.write('.'); // Show a simple loading indicator
  }, 1000);

  return {
    clear: () => clearInterval(indicator), // Clear the loading indicator
  };
};

// Function to download audio using yt-dlp
const downloadAudio = (url) => {
  // Command to get the video title for naming
  const titleCommand = `yt-dlp -e "${url}"`;

  exec(titleCommand, (error, title) => {
    if (error) {
      console.error(`Error fetching title: ${error.message}`);
      return;
    }

    // Clean the title for file system compatibility
    const cleanTitle = title.trim().replace(/[<>:"/\\|?*]+/g, '_'); // Replace invalid characters
    const filePath = path.join(__dirname, 'Downloads', `${cleanTitle}.mp3`);

    // Ensure the Downloads folder exists
    if (!fs.existsSync(path.join(__dirname, 'Downloads'))) {
      fs.mkdirSync(path.join(__dirname, 'Downloads'));
    }

    // Command to download the audio in MP3 format
    const command = `yt-dlp -x --audio-format mp3 -o "${filePath}" "${url}"`;

    const loadingIndicator = showLoadingIndicator(); // Show the loading indicator

    // Start downloading the audio
    const downloadProcess = exec(command);

    downloadProcess.on('close', (code) => {
      loadingIndicator.clear(); // Stop the loading indicator
      process.stdout.write('\n'); // Move to a new line after completion
      if (code !== 0) {
        console.error(`Download process exited with code ${code}`);
        return;
      }

      console.log(`Audio downloaded: ${filePath}`);

      // Ask user if they want to download another video
      const another = readlineSync.keyInYNStrict('Do you want to download another video?');
      if (another) {
        promptForUrl(); // Start over if the user wants to download again
      } else {
        console.log('Exiting the program. Goodbye!');
      }
    });
  });
};

// Function to prompt user for YouTube URL
const promptForUrl = () => {
  const url = readlineSync.question('Paste the YouTube video URL: ');

  // Validate URL using a basic check
  if (url.startsWith('https://www.youtube.com/watch?v=')) {
    downloadAudio(url);
  } else {
    console.log('Invalid URL. Please try again.');
    promptForUrl(); // Ask for the URL again
  }
};

// Start the process
promptForUrl();

// Unified Code Editor & Output Functionality
const codeEditor = document.getElementById('codeEditor');
const outputFrame = document.getElementById('outputFrame');

// Function to run the code and display the output
function runUnifiedCode() {
  const codeContent = codeEditor.value;

  // Wrap the user's code in a full HTML document
  const output = `
    <html>
      <head>
        <style>${extractCSS(codeContent)}</style>
      </head>
      <body>
        ${extractHTML(codeContent)}
        <script>${extractJS(codeContent)}<\/script>
      </body>
    </html>`;

  // Write to the iframe
  outputFrame.srcdoc = output;
}

// Function to extract HTML from the code editor
function extractHTML(code) {
  const htmlPattern = /<body>([\s\S]*)<\/body>/i;
  const match = htmlPattern.exec(code);
  return match ? match[1] : code;  // If no <body>, return everything
}

// Function to extract CSS from the code editor
function extractCSS(code) {
  const cssPattern = /<style>([\s\S]*)<\/style>/i;
  const match = cssPattern.exec(code);
  return match ? match[1] : '';  // If no <style>, return empty
}

// Function to extract JavaScript from the code editor
function extractJS(code) {
  const jsPattern = /<script>([\s\S]*)<\/script>/i;
  const match = jsPattern.exec(code);
  return match ? match[1] : '';  // If no <script>, return empty
}

// Video, Audio, and Message Handling
const video = document.getElementById('video');
const audio = document.getElementById('audio');
const playButton = document.getElementById('playButton');

// Messages
const helloMessage = document.getElementById('hello');
const welcomeMessage = document.getElementById('welcome');
const prototypeMessage = document.getElementById('prototype');
const optionsMessage = document.getElementById('options');
const compilersMessage = document.getElementById('compiler');
const chooseMessage = document.getElementById('choose');

// Function to play both video and audio and manage text display
function playMedia() {
    video.currentTime = 0; // Reset video to the beginning
    audio.currentTime = 0; // Reset audio to the beginning

    // Fade out play button
    playButton.style.transition = "opacity 1s ease";
    playButton.style.opacity = "0";

    // Wait for the button to fade out before playing media
    setTimeout(() => {
        video.play();
        audio.play();

        // Show and hide each message with the specified timing and fading
        setTimeout(() => {
            helloMessage.style.opacity = "1"; // Fade in the hello message
            setTimeout(() => {
                helloMessage.style.opacity = "0"; // Fade out the hello message
            }, 1500); // Show for 1 second
        }, 500); // Delay before showing "Hello"

        setTimeout(() => {
            welcomeMessage.style.opacity = "1"; // Fade in the welcome message
            setTimeout(() => {
                welcomeMessage.style.opacity = "0"; // Fade out the welcome message
            }, 2200); // Show for 1 second
        }, 2000); // Delay before showing "Welcome"

        setTimeout(() => {
            prototypeMessage.style.opacity = "1"; // Fade in the prototype message
            setTimeout(() => {
                prototypeMessage.style.opacity = "0"; // Fade out the prototype message
            }, 3500); // Show for 1 second
        }, 4200); // Delay before showing "Prototype"

        setTimeout(() => {
            optionsMessage.style.opacity = "1"; // Fade in the options message
            setTimeout(() => {
                optionsMessage.style.opacity = "0"; // Fade out the options message
            }, 2300); // Show for 1 second
        }, 8000); // Delay before showing "Options"

        setTimeout(() => {
            compilersMessage.style.opacity = "1"; // Fade in the compilers message
            setTimeout(() => {
                compilersMessage.style.opacity = "0"; // Fade out the compilers message
            }, 7500); // Show for 1 second
        }, 11000); // Delay before showing "Compilers"

        setTimeout(() => {
            chooseMessage.style.opacity = "1"; // Fade in the choose message
            setTimeout(() => {
                chooseMessage.style.opacity = "0"; // Fade out the choose message
            }, 2500); // Show for 1 second
        }, 19500); // Delay before showing "Choose"

        // Show buttons after the last message fades out
        setTimeout(() => {
            const buttonContainer = document.getElementById('buttonContainer');
            buttonContainer.style.display = "flex"; // Show the button container
            const buttons = buttonContainer.getElementsByClassName('button-52');
            Array.from(buttons).forEach((button, index) => {
                setTimeout(() => {
                    button.style.display = "block"; // Show each button one by one
                }, index * 1000); // 1 second delay between buttons
            });
        }, 22000); // Show buttons after 22 seconds
    }, 1000); // Delay media play until after the button fades out
}

// Function to skip the intro and go directly to the compilers options
function skipIntro() {
    video.pause();
    audio.pause();

    // Hide all messages
    const messages = [helloMessage, welcomeMessage, prototypeMessage, optionsMessage, compilersMessage, chooseMessage];
    messages.forEach(message => message.style.opacity = "0");

    // Hide the skip icon and the "Get Started" button
    skipButton.style.display = "none"; 
    playButton.style.display = "none"; 

    // Show the button container
    const buttonContainer = document.getElementById('buttonContainer');
    buttonContainer.style.display = "flex"; // Make the container visible

    // Show each button one after another
    const buttons = buttonContainer.getElementsByClassName('button-52');
    Array.from(buttons).forEach((button, index) => {
        setTimeout(() => {
            button.style.display = "block"; // Show button
        }, index * 1000); // Delay of 1 second for each button
    });
}

// Attach event listener to the play button
playButton.addEventListener('click', playMedia);

// Attach event listener to the skip icon
skipButton.addEventListener('click', skipIntro);

// Resizing functionality for the code editor and live output
const resizer = document.querySelector('.resizer');
const editor = document.querySelector('.editor');
const output = document.querySelector('.output');

resizer.addEventListener('mousedown', (e) => {
    e.preventDefault();
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
});

function handleMouseMove(e) {
    const containerWidth = document.querySelector('.container').clientWidth;
    const newWidth = e.clientX / containerWidth * 100; // Calculate width percentage

    // Set minimum width to prevent it from becoming too small
    if (newWidth > 10 && newWidth < 90) {
        editor.style.width = newWidth + '%';
        output.style.width = (100 - newWidth) + '%';
    }
}

function handleMouseUp() {
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
}

// Adjust layout on window resize
function adjustLayout() {
    const editorWidth = parseFloat(getComputedStyle(editor).width);
    const outputWidth = parseFloat(getComputedStyle(output).width);
    const totalWidth = editorWidth + outputWidth;
    const windowWidth = window.innerWidth;

    if (totalWidth < windowWidth) {
        editor.style.width = '40%';
        output.style.width = '60%';
    }
}

window.onload = adjustLayout;
window.onresize = adjustLayout;



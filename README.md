 Ollama Colab Connector: Your AI Models on the Go! ✨
Tired of complex local setups or limited hardware for running large language models? Want to experiment with Ollama models using the cloud's power?

This script is your one-stop solution! It automates setting up Ollama in a Google Colab environment and tunnels it to the internet using ngrok, letting you interact with models hosted on Colab's resources directly from your local machine!

Why is this awesome?

⚡️ Cloud Power: Leverage Google Colab's (potentially free!) GPUs for faster inference.
🛠️ Zero Local Setup (for the server): No need to install Ollama server locally if you just want to run models remotely.
🌍 Accessible Anywhere: Get a public URL to your Ollama instance running in Colab.
🚀 Quick Experiments: Fire up a model in minutes for testing or demos.
What Does the Magic Script Do?
This single Python script, designed to run in Google Colab, performs the following steps:

⬇️ Downloads and installs the latest Ollama version onto the Colab VM.
📦 Installs necessary Python libraries (pyngrok, nest_asyncio) required for tunneling and async operations.
🔑 Configures ngrok with your authtoken (more on security below!).
🔌 Starts the Ollama server process in the background.
🌐 Starts an ngrok tunnel, exposing Ollama's API port (11434) to a public URL.
✨ Prints the ngrok URL you'll need to connect!
Prerequisites
Before you embark on this cloud AI adventure, make sure you have:

A Google Account: Required to use Google Colab.
An ngrok Account & Authtoken: Sign up for a free account at ngrok.com. You'll find your authtoken on your dashboard after logging in. Keep this token secret!
Ollama Installed Locally: Yes, you'll still need the Ollama client installed on your local machine (or wherever you plan to connect from) to interact with the remote server. Download it from ollama.com.
Setup & Running (The Colab Part)
This is where the script comes to life!

Go to Google Colab and create a new notebook.
(Optional but Highly Recommended for Security): Add your ngrok authtoken as a Colab Secret:
Click the "🔑 Secrets" icon in the left sidebar.
Click "New Secret".
Set the Name to NGROK_AUTHTOKEN.
Set the Value to your actual ngrok authtoken (e.g., 2udHnIYkVWMhZPk42J0ujjajalDVu_7B2eKWEaN9uFfoneNTn8S).
Make sure the notebook access is toggled "On" for this secret.
Why? This prevents your token from being visible directly in your code or saved in the notebook file itself.
Copy the entire script code provided previously.
Paste the code into a Colab code cell.
If you did NOT use Colab Secrets: Find the line ngrok_token = "2udHnIYkVWMhZPk42J0uS3UlDVu_7B2eKWEaN9uFfoneNTn8S" in the script and replace the placeholder value with your actual ngrok authtoken. Again, using Colab Secrets is much safer!
Run the Colab cell (Shift + Enter).
Watch the output! The script will:

Print messages indicating installation progress.
Show output from the Ollama server starting.
Show output from ngrok, including the crucial url=https://... line.
Keep this Colab cell running! As long as the cell is executing, your Ollama server and ngrok tunnel will be active.

Using Your Remote Ollama Instance (The Local Part)
Now that your Ollama server is running in Colab and exposed via ngrok, you can connect to it from your local machine!

Find Your ngrok URL: Look at the output in your running Colab cell. Find the lines that start with >>> starting ngrok ... and then look for ngrok's own output. You'll see a line like:

...
t=2023-10-27T10:00:00+0000 lvl=info msg="tunnel established" obj=tunnels name=command_line id=... url=https://abcdef123456.ngrok-free.app
...
Copy the url value (e.g., https://abcdef123456.ngrok-free.app). This is your public Colab Ollama address!

Set OLLAMA_HOST Locally: Open a terminal on your local machine (where you installed the Ollama client). You need to tell your local Ollama client where the server is. Set the OLLAMA_HOST environment variable to the ngrok URL you copied.

For Bash, Zsh, or most Linux/macOS shells:

Bash

export OLLAMA_HOST=https://abcdef123456.ngrok-free.app
# Replace the URL above with your actual ngrok URL!
For Windows Command Prompt:

DOS

set OLLAMA_HOST=https://abcdef123456.ngrok-free.app
REM Replace the URL above with your actual ngrok URL!
For Windows PowerShell:

PowerShell

$env:OLLAMA_HOST="https://abcdef123456.ngrok-free.app"
# Replace the URL above with your actual ngrok URL!
Note: This variable setting is usually only active for the current terminal session. You might need to set it again in new terminals or add it to your shell profile (.bashrc, .zshrc, ~/.profile, etc.) for persistence.

Run Ollama Commands Locally: That's it! Now, any ollama command you run in that terminal session on your local machine will automatically talk to the Ollama server running remotely in your Colab instance!

Try it:

Bash

ollama list
# This should list models available on your Colab instance!
Bash

ollama run llama3 "Why is the sky blue?"
# This will download llama3 (if not already on Colab) and run the prompt using Colab's resources!
Important Notes & Cleanup
Security of Authtoken: Seriously, use Colab Secrets or environment variables instead of hardcoding your ngrok token.
Session Persistence: Colab VMs are temporary. When your Colab session ends (due to inactivity, hitting limits, or you manually stopping it), the VM is reset, the Ollama installation is gone, and the ngrok tunnel closes. You'll need to rerun the script in a new session.
Stopping: To stop everything, simply stop the running code cell in Google Colab (click the square stop button next to the cell). This will terminate the processes and close the ngrok tunnel. It's good practice to do this when you're finished to release Colab resources and end the ngrok session.
ngrok Limits: The ngrok free tier might disconnect your tunnel after a few hours.
Ollama Model Storage: Models downloaded via ollama run will be stored on the Colab VM's temporary disk and will also be lost when the session ends.
Happy remote model serving! 🎉

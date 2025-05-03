import os
import asyncio
import subprocess
import sys # Import sys for finding the python executable

# --- Setup Functions (Synchronous) ---

def run_setup_command(cmd, description):
    """Runs a setup command synchronously and checks for errors."""
    print(f">>> Running setup: {description}")
    try:
        # Use sys.executable to ensure pip is associated with the current python
        if cmd[0] == 'pip':
             cmd = [sys.executable, '-m'] + cmd
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
             print("STDERR:\n", result.stderr) # Print stderr even on success, sometimes useful
        print(f">>> Successfully completed: {description}")
    except FileNotFoundError:
        print(f"Error: Command not found: {cmd[0]}. Make sure it's installed and in your PATH.")
        sys.exit(1) # Exit if essential command not found
    except subprocess.CalledProcessError as e:
        print(f"Error during setup step: {description}")
        print("Command:", " ".join(e.cmd))
        print("Return Code:", e.returncode)
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        sys.exit(1) # Exit on setup errors
    except Exception as e:
        print(f"An unexpected error occurred during setup '{description}': {e}")
        sys.exit(1) # Exit on unexpected errors

# --- Async Helper Function ---

async def run_process(cmd):
    """Runs a command asynchronously and streams output."""
    print('>>> starting', *cmd)
    try:
        p = await asyncio.subprocess.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        async def pipe(lines):
            async for line in lines:
                print(line.strip().decode('utf-8'))

        await asyncio.gather(
            pipe(p.stdout),
            pipe(p.stderr),
        )

        await p.wait()  # Crucial step: wait for the process to finish
        if p.returncode != 0:
            print(f"Error: Command {' '.join(cmd)} exited with code {p.returncode}")
        return p.returncode  # Return exit code to check later

    except FileNotFoundError:
        print(f"Error: Command not found: {cmd[0]}. Make sure it's installed and in your PATH.")
        # Cannot exit directly from an async task without cancelling others,
        # so return a non-zero code to indicate failure.
        return 1
    except Exception as e:
        print(f"An unexpected error occurred running '{' '.join(cmd)}': {e}")
        return 1

# --- Main Async Logic ---

async def main():
    # --- ngrok Authtoken (SECURE WAY - RECOMMENDED VIA ENV VAR) ---
    # IMPORTANT: Replace hardcoded token with fetching from environment variable
    # Recommended: ngrok_token = os.environ.get("NGROK_AUTHTOKEN")
    # For demonstration, using the hardcoded token from your original script:
    ngrok_token = "ngrok_token" # <<-- REPLACE THIS WITH A SECURE METHOD

    if not ngrok_token or ngrok_token == "YOUR_NGROK_AUTHTOKEN_HERE": # Add a check for the placeholder
        print("ERROR: NGROK_AUTHTOKEN is not set or is the placeholder.")
        print("Please set the NGROK_AUTHTOKEN environment variable or replace the placeholder in the script.")
        sys.exit(1) # Exit if token is not set

    # Set the ngrok authtoken (only needs to be done once, ever)
    # Use synchronous subprocess.run for the config command
    run_setup_command(['ngrok', 'config', 'add-authtoken', ngrok_token], "Setting ngrok authtoken")

    # Set LD_LIBRARY_PATH (system-specific, adjust if needed)
    # Better to document this as a prerequisite, but keeping it as per original.
    # os.environ.update({'LD_LIBRARY_PATH': '/usr/lib64-nvidia'}) # Uncomment if needed and adjust path

    print("\n--- Starting Concurrent Processes (ollama serve and ngrok http) ---")
    # Run ollama and ngrok concurrently
    results = await asyncio.gather(
        run_process(['ollama', 'serve']),
        run_process(['ngrok', 'http', '--log', 'stderr', '11434', '--host-header', 'localhost:11434'])
    )

    # Check if any errors occurred in parallel processes
    if any(results):  # If any exit code is not 0, we have errors
        print("\n--- One or more processes failed. Check the output above for details. ---")
        sys.exit(1)
    else:
        print("\n--- Both ollama and ngrok seem to be running. Keep this script running! ---")
        # You might want to add a loop here or asyncio.Future to keep the main
        # event loop running indefinitely until manually stopped.
        # For now, the script will exit if the background processes exit.
        # A simple way to keep it running is to wait for a long time or signal.
        # Example: await asyncio.Future() # This will wait indefinitely
        # Or just let the script end if the subprocesses terminate.
        pass


# --- Script Entry Point ---

if __name__ == "__main__":
    print("--- Starting Setup Steps ---")

    # 1. Install Ollama (using curl | sh)
    # Breaking down the curl | sh command into safer steps: download then execute
    run_setup_command(['curl', '-fsSL', 'https://ollama.com/install.sh', '-o', '/tmp/ollama_install.sh'], "Downloading Ollama install script")
    # Make the downloaded script executable
    try:
         os.chmod('/tmp/ollama_install.sh', 0o755)
    except FileNotFoundError:
         print("Error: Failed to download ollama_install.sh to /tmp.")
         sys.exit(1)
    # Execute the script
    run_setup_command(['/tmp/ollama_install.sh'], "Executing Ollama install script")
    # Clean up the downloaded script
    try:
         os.remove('/tmp/ollama_install.sh')
    except OSError as e:
         print(f"Warning: Failed to remove temporary file /tmp/ollama_install.sh: {e}")


    # 2. Install Python packages
    # Added --break-system-packages flag as it's often needed in limited environments
    run_setup_command(['pip', 'install', 'aiohttp', 'pyngrok', 'nest_asyncio', '--break-system-packages'], "Installing Python packages")

    # 3. Apply nest_asyncio (needed for environments like Jupyter/Colab)
    # This is just Python code, doesn't need subprocess
    try:
        import nest_asyncio
        nest_asyncio.apply()
        print(">>> Applied nest_asyncio")
    except ImportError:
        print("Error: nest_asyncio failed to import. Check pip install step.")
        sys.exit(1)


    print("--- Setup Complete. Starting Main Async Process. ---")
    # Run the main asynchronous part
    asyncio.run(main())

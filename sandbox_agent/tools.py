import os
import uuid
import subprocess
import time

SESSION_NAME = "gemini-sandbox"

def get_or_create_sandbox() -> str:
    """Gets or creates the tmux -L geminisock session and returns its name."""
    res = subprocess.run(["tmux", "-L", "geminisock", "has-session", "-t", SESSION_NAME], capture_output=True)
    if res.returncode != 0:
        subprocess.run(["tmux", "-L", "geminisock", "new-session", "-d", "-s", SESSION_NAME])
        # Allow bash to load
        time.sleep(1)
    return SESSION_NAME

def run_bash_command_in_sandbox(command: str):
    """Executes a bash command in the persistent sandbox (tmux -L geminisock) and returns the output.
    
    This is extremely useful when state needs to persist across multiple commands,
    such as setting environment variables or navigating directories.
    
    Args:
        command: The bash command to run.
        
    Returns:
        The output of the command.
    """
    session = get_or_create_sandbox()
    
    # We will use window 0, pane 0
    target = session
    
    # Generate unique ID for polling
    unique_id = uuid.uuid4().hex
    log_file = f"/tmp/sandbox_{unique_id}.log"
    done_file = f"/tmp/sandbox_{unique_id}.done"
    
    # Remove old logs just in case
    if os.path.exists(log_file): os.remove(log_file)
    if os.path.exists(done_file): os.remove(done_file)
    
    # We write a bash snippet and pipe it to tmux -L geminisock send-keys
    script = f'''
(
{command}
) > {log_file} 2>&1
echo "{unique_id}" > {done_file}
'''
    
    # To execute this effectively via tmux -L geminisock send-keys without quoting hell,
    # let's write it to a temporary bash script and execute that script in the tmux -L geminisock partition.
    script_file = f"/tmp/sandbox_script_{unique_id}.sh"
    with open(script_file, "w") as f:
        f.write(script)
    
    subprocess.run(["chmod", "+x", script_file])
    subprocess.run(["tmux", "-L", "geminisock", "send-keys", "-t", target, f"bash {script_file}", "C-m"])
    
    # Polling for completion
    timeout = 180
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(done_file):
            break
        time.sleep(0.5)
        
    if not os.path.exists(done_file):
        # We can try to capture pane output
        pane_out = subprocess.run(["tmux", "-L", "geminisock", "capture-pane", "-p", "-t", target], capture_output=True, text=True).stdout
        return f"Command timed out after {timeout} seconds.\nCurrent Pane output:\n{pane_out}"
        
    with open(log_file, "r") as f:
        output = f.read()
        
    # Clean up temp files
    try:
        os.remove(log_file)
        os.remove(done_file)
        os.remove(script_file)
    except:
        pass
    
    return output if output.strip() else "(Command successfully executed with no output)"

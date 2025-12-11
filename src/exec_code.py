import docker
import tempfile
import os

def run_code_in_container(code: str) -> str:
    # 1. Write the LLM code to a temp file on the host
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='/tmp') as tmp:
        tmp.write(code)
        code_path = tmp.name

    try:
        client = docker.from_env()
        
        # 2. Run the container
        # The ENTRYPOINT is 'python exec_script.py', so we just pass the file path
        container = client.containers.run(
            'langchain-sandbox',
            command=[f'/code/{os.path.basename(code_path)}'],
            volumes={'/tmp': {'bind': '/code', 'mode': 'ro'}}, # Mount host /tmp to container /code
            network_mode='bridge',  # Allow internet for pip install
            mem_limit='512m',       # Sandbox resource limits
            remove=True             # Auto-delete after run
        )
        
        result= container.decode('utf-8').strip()
    except Exception as e:
        result = f"""{{"status": "error", "output": {str(e)}}}"""
    finally:
        try:
            os.unlink(code_path) # Cleanup host file
        except:
            pass

    return result
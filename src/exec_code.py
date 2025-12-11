import docker
import tempfile
import os
import json

def run_code_in_container(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='/tmp') as tmp:
        tmp.write(code)
        code_path = tmp.name
    try:
        client = docker.from_env()
        
        # Run container with network access for MCP HTTP servers
        container = client.containers.run(
            'langchain-sandbox',
            command=[f'/code/{os.path.basename(code_path)}'],
            volumes={'/tmp': {'bind': '/code', 'mode': 'ro'}},
            network_mode='bridge',  # Allow network access to MCP servers
            mem_limit='512m',
            cpu_period=100000,
            cpu_quota=50000,
            remove=True,
            detach=False,
            stdout=True,
            stderr=True
        )
        
        
        # Decode output
        output = container.decode('utf-8').strip()

        # results = [json.loads(line) for line in output.strip().split('\n')]
        
        result = output

    except Exception as e:
        result = f"""{{"status": "error", "output": {str(e)}}}"""
    finally:
        try:
            os.unlink(code_path)
        except:
            pass

    return result
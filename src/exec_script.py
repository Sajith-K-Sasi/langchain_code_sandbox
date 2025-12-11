import sys
import subprocess
import re
import importlib
import json

def install_packages(code_str: str):
    """
    Scans code for '# AUTO_INSTALL: pandas numpy' and installs them using uv.
    """
    pattern = r'#\s*AUTO_INSTALL:\s*(.+)'
    matches = re.findall(pattern, code_str)
    
    if matches:
        packages = []
        for match in matches:
            packages.extend(match.split())
    
        # Use uv for fast installation
        print(json.dumps({"status": "info", "output": f"Installing packages: {' '.join(packages)}"}))
        subprocess.check_call(["uv", "pip", "install"] + packages)
        print(json.dumps({"status": "info", "output": "Packages installed successfully"}))
        importlib.invalidate_caches()
        

def execute_code(code_str: str):
    try:
        install_packages(code_str)
        
        # Execute the code in a shared scope
        execution_scope = {}
        exec(code_str, execution_scope, execution_scope)
        
        # Extract the 'result' variable
        result = execution_scope.get('result', None)
        print(json.dumps({"status": "success", "output": result}))
        
    except Exception as e:
        print(json.dumps({"status": "error", "output": str(e)}))

if __name__ == "__main__":
    # Read the code file passed from Docker command
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    execute_code(code)
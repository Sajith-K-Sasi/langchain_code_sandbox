import sys
import subprocess
import re
import importlib
import json

def install_packages(code_str: str):
    """
    Scans code for '# AUTO_INSTALL: [pandas, numpy]' and installs them using uv.
    """
    pattern = r'#\s*AUTO[-_\s]+INSTALL\s*:?\s*\[(.*?)\]'
    matches = re.findall(pattern, code_str, re.IGNORECASE | re.DOTALL)
    
    all_packages = []
    if matches:
        for content in matches:
            content = content.replace('\n', ',')

            # Split by comma and strip whitespace from each package name
            pkgs = [p.strip() for p in content.split(',') if p.strip()]
            all_packages.extend(pkgs)
    
    if all_packages:
        # Remove duplicates
        unique_packages = list(dict.fromkeys(all_packages))
        
        print(json.dumps({"status": "info", "output": f"Installing packages: {', '.join(unique_packages)}"}))
        try:
            subprocess.check_call(["uv", "pip", "install"] + unique_packages)
            print(json.dumps({"status": "info", "output": "Packages installed successfully"}))
            importlib.invalidate_caches()
        except subprocess.CalledProcessError as e:
            print(json.dumps({"status": "error", "output": str(e)}))
        

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
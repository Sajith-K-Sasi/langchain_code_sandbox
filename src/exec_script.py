import sys
import json
import traceback
import subprocess
import re
import importlib
import site

def install_packages(code_str: str) -> None:
    """Parse and install packages from AUTO_INSTALL comments."""
    # Look for lines like: # AUTO_INSTALL: package1 package2
    pattern = r'#\s*AUTO_INSTALL:\s*(.+)'
    matches = re.findall(pattern, code_str)
    
    packages_to_install = []
    
    if matches:
        for match in matches:
            # Split by comma or whitespace to be robust
            parts = re.split(r'[,\s]+', match.strip())
            packages_to_install.extend([p for p in parts if p])
            
    if packages_to_install:
        try:
            print(json.dumps({
                "status": "info", 
                "message": f"Installing packages: {', '.join(packages_to_install)}"
            }), file=sys.stderr)
            
            # 1. Remove '--system'. standard uv install works because VIRTUAL_ENV is set.
            # 2. Install all at once for speed (uv is very fast at resolving batched deps).
            subprocess.check_call(
                ["uv", "pip", "install"] + packages_to_install,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE  # Capture stderr to keep main output clean
            )
            
            # 3. CRITICAL: Invalidate caches so Python sees the new libs
            importlib.invalidate_caches()
            importlib.reload(site)
            
            print(json.dumps({
                "status": "info", 
                "message": "Installation successful"
            }), file=sys.stderr)
            
        except subprocess.CalledProcessError as e:
            # Catch stderr from uv if possible
            error_msg = str(e)
            if e.stderr:
                error_msg += f": {e.stderr.decode().strip()}"
                
            print(json.dumps({
                "status": "warning", 
                "message": f"Package installation failed: {error_msg}"
            }), file=sys.stderr)

def execute_code(code_str: str) -> None:
    try:
        # 1. Install dependencies first
        install_packages(code_str)
        
        # 2. Execute code
        # FIX: Use a single dictionary for both globals and locals.
        # This allows functions defined in the string to see imports defined in the string.
        execution_scope = {}
        
        # Pass the same dict for both arguments
        exec(code_str, execution_scope, execution_scope)
        
        result = execution_scope.get('result', None)
        
        print(json.dumps({"status": "success", "output": result}))
        
    except Exception as e:
        print(json.dumps({
            "status": "error", 
            "output": str(e), 
            "traceback": traceback.format_exc()
        }))

if __name__ == "__main__":
    # Fallback to reading from stdin if no file provided
    # This makes it easier to use with 'docker run -i ...'
    if len(sys.argv) < 2:
        code_str = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r') as f:
            code_str = f.read()
            
    if not code_str.strip():
        print(json.dumps({"status": "error", "output": "No code provided"}))
        sys.exit(1)

    execute_code(code_str)
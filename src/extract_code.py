import docker
import tempfile
import os
import json

def extract_code(response: str) -> str:
    code = response
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    return code
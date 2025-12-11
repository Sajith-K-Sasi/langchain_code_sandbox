FROM python:3.12-slim

# 1. Install uv
# It is faster/cleaner to copy the binary than to pip install it
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 2. Setup the application directory and user
# Create directory and user in one step to keep layers small
RUN useradd -m codeuser && \
    mkdir /app && \
    chown codeuser:codeuser /app

# 3. Switch Context
USER codeuser
WORKDIR /app

# 4. Environment Variables
# Add the venv to PATH so "python" automatically uses the venv
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# 5. Install Dependencies
# Create a venv and install packages into it
# --no-cache prevents uv from leaving a cache directory in your image layer
RUN uv venv && \
    uv pip install --no-cache requests numpy

# 6. Copy Code
# Use --chown to ensure the user owns their own script
COPY --chown=codeuser:codeuser src/exec_script.py /app/

ENTRYPOINT ["python", "exec_script.py"]
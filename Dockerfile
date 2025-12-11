FROM python:3.12-slim

# 1. Install uv for lightning-fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 2. Setup user permissions (Security Best Practice)
RUN useradd -m codeuser && \
    mkdir /app && \
    chown codeuser:codeuser /app

USER codeuser
WORKDIR /app

# 3. Configure Virtual Environment
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# 4. Create venv and pre-install common libs
RUN uv venv && \
    uv pip install --no-cache requests numpy

# 5. The Wrapper Script
COPY --chown=codeuser:codeuser src/exec_script.py /app/

# The container acts as an executable wrapper
ENTRYPOINT ["python", "exec_script.py"]
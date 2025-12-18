#### 1. Build the image first (one time)
```bash
docker build -t langchain-sandbox .
```

#### 2. Test the container interactively with a simple Python script
```bash
docker run --rm -it -v "$(pwd)/test:/code" langchain-sandbox:latest /code/sample.py
```

#### 3. Set up environment variables
Copy `example.env` to `.env` and add your Hugging Face API token:
```bash
cp example.env .env
# Edit .env and add your HUGGINGFACEHUB_API_TOKEN
```

#### 4. Install dependencies
```bash
uv sync
```

#### 5. Run the langchain_example.py
```bash
uv run langchain_example.py
```

#### 6. Run the langgraph_agent.py
```bash
uv run langgraph_agent.py
```

#### 7. Example usage
Try asking questions like:
- "what's the time and date now in Indian timezone"
- "calculate 25 * 17"
- "what's the highlight in this page https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct"


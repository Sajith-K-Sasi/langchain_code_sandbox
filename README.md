# 1. Build the image first (one time)
docker build -t langchain-sandbox .

# 2. Test the container interactively with a simple Python script
docker run --rm -it -v "$(pwd)/code:/code" langchain-sandbox:latest /code/sample.py

# 3. Run the main.py
uv run main.py

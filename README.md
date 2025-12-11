#### 1. Build the image first (one time)
```bash
docker build -t langchain-sandbox .
```

#### 2. Test the container interactively with a simple Python script
```bash
docker run --rm -it -v "$(pwd)/code:/code" langchain-sandbox:latest /code/sample.py
```

#### 3. Set up environment variables
Copy `example.env` to `.env` and add your Hugging Face API token:
```bash
cp example.env .env
# Edit .env and add your HUGGINGFACEHUB_API_TOKEN
```

#### 4. Run the main.py
```bash
uv run main.py
```

#### 5. Example usage
Try asking questions like:
- "what's the time and date now in Indian timezone"
- "calculate 25 * 17"
- "generate a random password"

#### Output
```bash
╭───────────────────────────────────────────── Question ──────────────────────────────────────────────╮
│ what's the time and date now in Indian timezone                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────── AI Response - without code execution ────────────────────────────────╮
│ I don't have access to real-time information, so I can't tell you the current time and date in      │
│ India.                                                                                              │
│                                                                                                     │
│ To get the current time in India (IST - Indian Standard Time), you can:                             │
│ - Search "current time in India" on Google                                                          │
│ - Check a world clock website                                                                       │
│ - Use your phone's world clock feature                                                              │
│ - Ask a voice assistant like Siri or Google Assistant                                               │
│                                                                                                     │
│ India's timezone is UTC+5:30, and it doesn't observe daylight saving time, so it remains consistent │
│ year-round.                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────── AI Response - with code execution ─────────────────────────────────╮
│ {"status": "info", "message": "Installing packages: pytz"}                                          │
│ {"status": "info", "message": "Installation successful"}                                            │
│ {"status": "success", "output": "The current date and time in Indian timezone is: 2025-12-11        │
│ 17:04:00 IST"}                                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

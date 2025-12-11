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
╭─────────────────────────────────────────── Question ───────────────────────────────────────────╮
│ what's the time and date now in Indian timezone                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────── AI Response - without code execution ─────────────────────────────╮
│ I don't have access to real-time information, so I can't tell you the current time and date.   │
│ However, I can help you find it!                                                               │
│                                                                                                │
│ India uses **IST (Indian Standard Time)**, which is UTC+5:30.                                  │
│                                                                                                │
│ To get the current time in India, you can:                                                     │
│ - Search "current time in India" in your web browser                                           │
│ - Check your phone's world clock feature                                                       │
│ - Use a timezone converter website                                                             │
│ - Ask a voice assistant like Siri or Google Assistant                                          │
│                                                                                                │
│ Is there anything else about Indian timezones I can help you with?                             │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── AI Generated Code ───────────────────────────────────────╮
│ # AUTO_INSTALL: pytz                                                                           │
│ def execute_code():                                                                            │
│     import datetime                                                                            │
│     import pytz                                                                                │
│                                                                                                │
│     # Get the current time in UTC                                                              │
│     utc_now = datetime.datetime.now(pytz.UTC)                                                  │
│                                                                                                │
│     # Convert to Indian timezone (IST - India Standard Time)                                   │
│     india_tz = pytz.timezone('Asia/Kolkata')                                                   │
│     india_time = utc_now.astimezone(india_tz)                                                  │
│                                                                                                │
│     # Format the date and time                                                                 │
│     formatted_time = india_time.strftime("%Y-%m-%d %H:%M:%S %Z")                               │
│                                                                                                │
│     return f"The current date and time in Indian timezone is: {formatted_time}"                │
│                                                                                                │
│ result = execute_code()                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────── Code Execution Result ─────────────────────────────────────╮
│ {"status": "info", "message": "Installing packages: pytz"}                                     │
│ {"status": "info", "message": "Installation successful"}                                       │
│ {"status": "success", "output": "The current date and time in Indian timezone is: 2025-12-11   │
│ 17:15:22 IST"}                                                                                 │
╰────────────────────────────────────────────────────────────────────────────────────────────────╯

```

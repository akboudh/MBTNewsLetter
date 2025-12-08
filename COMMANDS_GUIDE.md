# MBT Newsletter - Complete Guide to Files & Commands

## 📁 Project Files Explained

### Core Python Files

#### `main.py` - **The Orchestrator**
- **What it does**: Main entry point that coordinates the entire newsletter process
- **Steps it runs**:
  1. Scrapes all news sources
  2. Generates newsletter content using OpenAI
  3. Sends email to recipients
- **Command modes**:
  - `python main.py` - Run once and send email immediately
  - `python main.py --test` - Generate newsletter but don't send (preview mode)
  - `python main.py --schedule` - Start scheduler to run every 5 days automatically

#### `scraper.py` - **Web Scraper**
- **What it does**: Fetches content from all 6 news websites
- **Functions**:
  - `scrape_source(url)` - Scrapes a single website, extracts text and article links
  - `scrape_all_sources(urls)` - Scrapes all sources with 2-second delays (rate limiting)
- **Returns**: Dictionary with URL, text content, article links, and success status

#### `openai_client.py` - **AI Content Generator**
- **What it does**: Uses OpenAI GPT-4 to analyze scraped content and generate newsletter
- **Function**: `generate_newsletter(scraped_items, days_since_last_run)`
- **Process**:
  - Formats scraped content for OpenAI
  - Sends your system prompt + scraped data to GPT-4
  - Returns formatted newsletter content (500-650 words)

#### `email_sender.py` - **Email Handler**
- **What it does**: Creates beautiful HTML email and sends it via SMTP
- **Functions**:
  - `create_purdue_theme_html(content)` - Converts newsletter text into card-based HTML with Purdue colors
  - `send_email(newsletter_content, subject)` - Sends email to all recipients in RECIPIENT_EMAILS
- **Features**: 
  - Card-based design with gold/black theme
  - Responsive (mobile-friendly)
  - Sends to multiple recipients

#### `scheduler.py` - **Automation Manager**
- **What it does**: Manages scheduling and tracks when newsletter last ran
- **Functions**:
  - `get_days_since_last_run()` - Calculates days since last newsletter (min 5 days)
  - `update_last_run()` - Saves timestamp to `last_run.json`
  - `start_scheduler()` - Runs newsletter every 5 days automatically
- **File**: Creates `last_run.json` to track last execution time

#### `config.py` - **Configuration Manager**
- **What it does**: Loads all settings from `.env` file
- **Contains**:
  - OpenAI API key
  - Email credentials (SMTP settings)
  - List of recipient emails
  - News source URLs
  - Your system prompt (the long prompt for OpenAI)
  - User prompt template

### Helper Files

#### `run.sh` - **Convenience Script**
- **What it does**: Automatically activates virtual environment and runs main.py
- **Why use it**: You don't need to manually activate `venv` each time
- **Usage**: 
  ```bash
  ./run.sh              # Send email
  ./run.sh --test       # Test mode
  ./run.sh --schedule   # Schedule mode
  ```

#### `requirements.txt` - **Dependencies List**
- **What it does**: Lists all Python packages needed
- **Contains**: openai, beautifulsoup4, requests, schedule, etc.
- **Install**: `pip install -r requirements.txt`

#### `.env` - **Secrets & Settings** (not in git)
- **What it does**: Stores your API keys and email passwords
- **Contains**:
  - `OPENAI_API_KEY` - Your OpenAI API key
  - `EMAIL_ADDRESS` - Your Gmail address
  - `EMAIL_PASSWORD` - Gmail app password
  - `RECIPIENT_EMAILS` - Comma-separated list of recipients
  - SMTP settings

#### `.env.example` - **Template**
- **What it does**: Example file showing what variables to set
- **Use**: Copy to `.env` and fill in your actual values

#### `README.md` - **Documentation**
- **What it does**: Setup instructions and usage guide

### Generated Files

#### `last_run.json` - **Tracking File**
- **What it does**: Stores timestamp of last newsletter run
- **Created by**: `scheduler.py`
- **Used by**: Calculates "days since last run" for OpenAI prompt

#### `venv/` - **Virtual Environment**
- **What it does**: Isolated Python environment with all packages
- **Contains**: All installed dependencies (openai, beautifulsoup4, etc.)
- **Why**: Keeps project dependencies separate from system Python

---

## 🚀 Commands Explained

### Basic Commands

#### `./run.sh`
- **What it does**: 
  1. Activates virtual environment
  2. Runs `python main.py`
  3. Scrapes → Generates → Sends email
- **When to use**: When you want to send newsletter immediately

#### `./run.sh --test`
- **What it does**: 
  1. Activates virtual environment
  2. Runs `python main.py --test`
  3. Scrapes → Generates → **Prints to console** (doesn't send)
- **When to use**: To preview newsletter content before sending

#### `./run.sh --schedule`
- **What it does**: 
  1. Activates virtual environment
  2. Runs `python main.py --schedule`
  3. Starts scheduler that runs newsletter every 5 days
  4. Keeps running until you stop it (Ctrl+C)
- **When to use**: For automatic recurring newsletters

### Manual Commands (if you activate venv yourself)

#### `source venv/bin/activate`
- **What it does**: Activates the virtual environment
- **Why**: Makes Python packages available in your shell
- **Note**: `run.sh` does this automatically

#### `python main.py`
- **What it does**: Same as `./run.sh` but requires venv to be activated first
- **When to use**: If you prefer manual control

#### `python main.py --test`
- **What it does**: Same as `./run.sh --test`

#### `python main.py --schedule`
- **What it does**: Same as `./run.sh --schedule`

### Setup Commands

#### `python3 -m venv venv`
- **What it does**: Creates virtual environment folder
- **When to use**: First time setup (already done for you)

#### `pip install -r requirements.txt`
- **What it does**: Installs all required Python packages
- **When to use**: First time setup or after adding new dependencies
- **Note**: Must be run with venv activated

---

## 🔄 Complete Workflow

### When you run `./run.sh`:

```
1. run.sh activates venv
   ↓
2. main.py starts
   ↓
3. scraper.py fetches content from 6 websites
   ↓
4. openai_client.py sends data to GPT-4
   ↓
5. GPT-4 generates newsletter content
   ↓
6. email_sender.py creates HTML email
   ↓
7. email_sender.py sends to all recipients
   ↓
8. scheduler.py updates last_run.json
   ↓
9. Done! ✅
```

### When you run `./run.sh --schedule`:

```
1. Scheduler starts
   ↓
2. Waits 5 days
   ↓
3. Runs full workflow (steps 2-9 above)
   ↓
4. Waits another 5 days
   ↓
5. Repeats forever (until you stop it)
```

---

## 📧 Email Flow

1. **Content Generation**: OpenAI creates newsletter text
2. **HTML Conversion**: `email_sender.py` parses text and creates card-based HTML
3. **Styling**: Applies Purdue theme (gold #CEB888, black)
4. **Sending**: Connects to Gmail SMTP and sends to each recipient
5. **Delivery**: Each recipient gets a personalized email

---

## 🛠️ Troubleshooting

- **"pip not found"**: Use `python3 -m pip` or activate venv first
- **"Module not found"**: Run `pip install -r requirements.txt` with venv activated
- **"Email failed"**: Check `.env` has correct Gmail app password
- **"Scraping failed"**: Some sites block scrapers (normal), system uses successful ones
- **"OpenAI error"**: Check API key in `.env` is valid

---

## 💡 Pro Tips

1. **Test first**: Always run `--test` before sending to new recipients
2. **Check logs**: The output shows what's happening at each step
3. **Multiple emails**: Add comma-separated emails in `RECIPIENT_EMAILS` in `.env`
4. **Scheduling**: For production, use cron job instead of `--schedule` mode
5. **Backup**: Keep your `.env` file secure (it's in `.gitignore`)



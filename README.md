# MBT Newsletter Generator

An automated newsletter system that scrapes tech news sources, analyzes them with OpenAI, and sends a curated newsletter to your email every 5 days. Perfect for staying updated on the latest tech and business insights.

## 🚀 Features

- **Automated Scraping**: Scrapes content from 6 major tech news sources
- **AI-Powered Curation**: Uses OpenAI GPT-4 to analyze and curate the most relevant stories
- **Beautiful HTML Emails**: Generates polished, Purdue-themed HTML newsletters
- **Automated Scheduling**: Automatically sends emails every 5 days
- **Strategic Focus**: Curates stories with strategic insights for business + AI students
- **Multi-Recipient Support**: Send newsletters to multiple email addresses

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- An **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- A **Gmail account** with 2-Step Verification enabled (for app passwords)
- Basic familiarity with command line/terminal

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/akboudh/MBTNewsLetter.git
cd MBTNewsLetter
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# On macOS/Linux
cp .env.example .env

# Or create manually
touch .env
```

Edit the `.env` file and add the following variables:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Required: Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here

# Optional: Email Settings (defaults provided)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional: Recipient emails (comma-separated for multiple recipients)
# If not set, defaults to EMAIL_ADDRESS
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com
```

#### Getting Your Gmail App Password

1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification** (enable it if not already enabled)
3. Scroll down to **App passwords**
4. Select **Mail** and **Other (Custom name)**
5. Enter "MBT Newsletter" as the name
6. Copy the generated 16-character password and use it as `EMAIL_PASSWORD`

## 🎯 Usage

### Test Mode (Recommended First Run)

Test the newsletter generation without sending an email:

```bash
# Using the helper script (automatically activates venv)
./run.sh --test

# Or manually (make sure venv is activated)
python main.py --test
```

This will generate the newsletter content and display it in the terminal without sending any emails.

### Run Once (Generate and Send)

Generate and send the newsletter immediately:

```bash
# Using the helper script
./run.sh

# Or manually
python main.py
```

### Run as Scheduled Service

Run the newsletter automatically every 5 days:

```bash
# Using the helper script
./run.sh --schedule

# Or manually
python main.py --schedule
```

This will keep the script running and check daily if it's time to send the newsletter (every 5 days).

### Using Cron (Production - Recommended)

For production environments, it's recommended to use cron instead of the Python scheduler:

```bash
# Edit crontab
crontab -e

# Add this line to run every 5 days at 9 AM
0 9 */5 * * cd /path/to/mbtnewsletter && /path/to/venv/bin/python main.py
```

## 📁 Project Structure

```
mbtnewsletter/
├── main.py              # Main entry point
├── scraper.py           # Web scraping logic
├── openai_client.py     # OpenAI API integration
├── email_sender.py      # Email sending functionality
├── scheduler.py         # Scheduling logic
├── config.py            # Configuration and settings
├── requirements.txt     # Python dependencies
├── run.sh              # Helper script for running
├── .env.example        # Example environment variables
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 📰 News Sources

The system automatically scrapes content from:

- [TLDR Tech](https://tldr.tech/newsletters)
- [Morning Brew](https://www.morningbrew.com/)
- [The Hustle](https://thehustle.co/news)
- [Axios Newsletters](https://www.axios.com/newsletters)
- [Tech Brew](https://www.techbrew.com/all/stories/news)
- [The Founder Playbook](https://thefounderplaybook.hustlefund.vc/)

## 🎨 Email Theme

Newsletters are styled with Purdue's colors (gold #CEB888 and black) for a professional, branded look. The HTML emails are mobile-responsive and work across all major email clients.

## ⚙️ Configuration

### Customizing News Sources

Edit `config.py` to add or modify news sources:

```python
NEWS_SOURCES = [
    'https://your-news-source.com',
    # Add more sources here
]
```

### Customizing Newsletter Style

The newsletter generation prompt can be customized in `config.py` by modifying the `SYSTEM_PROMPT` variable.

### Email Settings

You can customize email settings in `config.py` or via environment variables:

- `EMAIL_ADDRESS`: Your sender email address
- `EMAIL_PASSWORD`: Your email app password
- `SMTP_SERVER`: SMTP server (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP port (default: 587)
- `RECIPIENT_EMAILS`: Comma-separated list of recipient emails

## 🐛 Troubleshooting

### Common Issues

**Issue: "OPENAI_API_KEY not set"**
- Solution: Make sure your `.env` file exists and contains `OPENAI_API_KEY=your_key_here`

**Issue: "EMAIL_PASSWORD not set"**
- Solution: Ensure you've created a Gmail app password and added it to your `.env` file

**Issue: "Authentication failed" when sending email**
- Solution: 
  - Verify you're using an app password, not your regular Gmail password
  - Ensure 2-Step Verification is enabled on your Google account
  - Check that `EMAIL_ADDRESS` matches the account the app password was created for

**Issue: Scraping fails for some sources**
- Solution: Some websites may block automated requests. The script will continue with successfully scraped sources.

**Issue: Virtual environment not activating**
- Solution: Make sure you're in the project directory and the venv folder exists. Recreate it if needed: `python3 -m venv venv`

### Debug Mode

Enable more detailed logging by modifying the logging level in `main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 📝 Notes

- The scraper respects rate limits with 2-second delays between requests
- Newsletter content is limited to 500-650 words for readability
- The system tracks the last run date in `last_run.json` to calculate days since last newsletter
- The scheduler checks every hour if it's time to send the newsletter

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- News sources: TLDR Tech, Morning Brew, The Hustle, Axios, Tech Brew, and The Founder Playbook
- Built with OpenAI GPT-4 for content generation

---

**Made with ❤️ for MBT students**

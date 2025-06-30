# Rx-Recall Watch

A Python tool to monitor FDA drug recalls, summarize reasons using a local LLM, and send alert emails.

# Overview
Rx-Recall Watch automatically fetches drug recall data from the FDA, summarizes the reason using a local LLM (Mistral via Ollama), stores the results in a SQLite database, and sends email alerts to keep users informed. Designed for simplicity, privacy, and extendability.

# Features
- Automatically fetches FDA recall data
- Summarizes recall reasons using offline AI (Ollama)
- Stores data in a local SQLite database
- Sends email alerts with the latest summaries
- Designed for automation (e.g. Task Scheduler or cron)

# Project Structure
rx-recall-watch/
├── data/                  # SQLite DB file 
├── utils/
│   └── email_utils.py     # Email sending logic
├── recall_job.py          # Main automation script
├── schema.sql             # SQL table schema
├── requirements.txt       # Python dependencies
├── .env.example           # Template for email config
├── .gitignore             # Files to exclude from version control
└── README.md              # This file

## Setup - For users wishing to use this tool

# 1. Clone this repo

git clone https://github.com/yourusername/rx-recall-watch.git
cd rx-recall-watch

# 2. Create and activate virtual env
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows

# 3. Install your dependencies
pip install -r requirements.txt

# 4. Setup your evironment vars
cp .env.example .env

Open the .env and fill in your email credentials

Note: the pass is not your normal email password you must have Google 2FA setup and generate a Gmail app password

# 5. Run python recall_job.py
Test if this works

# 6. Automate this system
Use TaskScheduler to run this program daily and it will send you an email if anything got added to your database

# Heroku Deployment Guide

## Quick Deployment Steps

### 1. Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use package manager
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Deploy the App
```bash
# Create a new Heroku app
heroku create your-app-name

# Or use the deployment script
chmod +x deploy.sh
./deploy.sh your-app-name
```

### 4. Set Environment Variables
In Heroku dashboard or via CLI:
```bash
heroku config:set GOOGLE_SHEETS_CREDENTIALS="your-google-credentials-json"
heroku config:set OPENAI_API_KEY="your-openai-api-key"
heroku config:set SHEET_ID="your-google-sheet-id"
heroku config:set MISTRAL_OCR_API_KEY="your-mistral-api-key"  # optional
```

### 5. Add Heroku Scheduler
```bash
heroku addons:create scheduler:standard
```

### 6. Configure Scheduled Task
1. Go to Heroku Dashboard → Your App → Resources → Heroku Scheduler
2. Click "Add Job"
3. Command: `python main.py`
4. Frequency: Choose your preferred schedule (e.g., Every hour at 00)
5. Save the job

## File Structure for Heroku
```
resume-analysis/
├── main.py                 # Main script
├── Procfile               # Heroku process definition
├── runtime.txt            # Python version
├── requirements.txt       # Dependencies
├── src/                   # Your source code
└── deploy.sh             # Deployment script
```

## Testing the Deployment
```bash
# Test locally first
python main.py

# Check Heroku logs
heroku logs --tail

# Run manually on Heroku
heroku run python main.py
```

## Troubleshooting
- Check logs: `heroku logs --tail`
- Restart dyno: `heroku restart`
- Check config: `heroku config`
- Run one-off dyno: `heroku run python main.py` 
#!/bin/bash

# Heroku Deployment Script for Resume Analysis

echo "🚀 Starting Heroku deployment..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Not logged in to Heroku. Please run: heroku login"
    exit 1
fi

# Get app name from user or use default
APP_NAME=${1:-resume-analysis-app}

echo "📦 Creating/updating Heroku app: $APP_NAME"

# Create app if it doesn't exist
heroku apps:info $APP_NAME &> /dev/null || heroku create $APP_NAME

# Set buildpacks
echo "🔧 Setting up buildpacks..."
heroku buildpacks:clear $APP_NAME
heroku buildpacks:add heroku/python $APP_NAME

# Set environment variables
echo "🔐 Setting environment variables..."
echo "Please make sure to set the following environment variables in Heroku:"
echo "  - GOOGLE_SHEETS_CREDENTIALS"
echo "  - OPENAI_API_KEY"
echo "  - SHEET_ID"
echo "  - MISTRAL_OCR_API_KEY (optional)"

# Deploy to Heroku
echo "📤 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up environment variables in Heroku dashboard"
echo "2. Add Heroku Scheduler addon: heroku addons:create scheduler:standard"
echo "3. Configure scheduled tasks in Heroku dashboard to run: python main.py"
echo "4. Set the frequency (e.g., every hour) in the scheduler" 
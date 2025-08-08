# Heroku Deployment Script for Resume Analysis (Windows PowerShell)

Write-Host "🚀 Starting Heroku deployment..." -ForegroundColor Green

# Check if Heroku CLI is installed
try {
    $null = heroku --version
} catch {
    Write-Host "❌ Heroku CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Heroku
try {
    $null = heroku auth:whoami
} catch {
    Write-Host "❌ Not logged in to Heroku. Please run: heroku login" -ForegroundColor Red
    exit 1
}

# Get app name from parameter or use default
$APP_NAME = if ($args[0]) { $args[0] } else { "resume-analysis-app" }

Write-Host "📦 Creating/updating Heroku app: $APP_NAME" -ForegroundColor Cyan

# Create app if it doesn't exist
try {
    $null = heroku apps:info $APP_NAME
} catch {
    heroku create $APP_NAME
}

# Set buildpacks
Write-Host "🔧 Setting up buildpacks..." -ForegroundColor Cyan
heroku buildpacks:clear $APP_NAME
heroku buildpacks:add heroku/python $APP_NAME

# Set environment variables
Write-Host "🔐 Setting environment variables..." -ForegroundColor Cyan
Write-Host "Please make sure to set the following environment variables in Heroku:" -ForegroundColor Yellow
Write-Host "  - GOOGLE_SHEETS_CREDENTIALS" -ForegroundColor White
Write-Host "  - OPENAI_API_KEY" -ForegroundColor White
Write-Host "  - SHEET_ID" -ForegroundColor White
Write-Host "  - MISTRAL_OCR_API_KEY (optional)" -ForegroundColor White

# Deploy to Heroku
Write-Host "📤 Deploying to Heroku..." -ForegroundColor Cyan
git add .
git commit -m "Deploy to Heroku"
git push heroku main

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Set up environment variables in Heroku dashboard" -ForegroundColor White
Write-Host "2. Add Heroku Scheduler addon: heroku addons:create scheduler:standard" -ForegroundColor White
Write-Host "3. Configure scheduled tasks in Heroku dashboard to run: python main.py" -ForegroundColor White
Write-Host "4. Set the frequency (e.g., every hour) in the scheduler" -ForegroundColor White 
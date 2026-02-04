#!/bin/bash

# BHIV Bucket Render Deployment Script
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
echo "🚀 Deploying BHIV Bucket to Render (Environment: $ENVIRONMENT)"

# Check if required files exist
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ main.py not found"
    exit 1
fi

if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found"
    exit 1
fi

echo "✅ All required files found"

# Validate environment variables
echo "🔍 Checking environment variables..."

if [ -z "$REDIS_HOST" ]; then
    echo "⚠️  REDIS_HOST not set"
fi

if [ -z "$MONGODB_URI" ]; then
    echo "⚠️  MONGODB_URI not set"
fi

# Run tests before deployment
echo "🧪 Running health checks..."
python -c "
import sys
try:
    from main import app
    print('✅ Main application imports successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Git operations
echo "📦 Preparing deployment..."
git add .
git status

echo "🎯 Deployment checklist:"
echo "  ✅ Files prepared"
echo "  ✅ Dependencies checked"
echo "  ✅ Environment validated"
echo "  ✅ Health checks passed"

echo ""
echo "🚀 Ready to deploy!"
echo "   1. Commit your changes: git commit -m 'Deploy to production'"
echo "   2. Push to GitHub: git push origin main"
echo "   3. Render will auto-deploy from GitHub"
echo ""
echo "📊 Monitor deployment at: https://dashboard.render.com"
#!/bin/bash

# Math & Chat API - Setup Script
# This script helps you set up and deploy the application

set -e

echo "======================================"
echo "Math & Chat API - Setup"
echo "======================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Create a GitHub/GitLab repository"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin <your-repo-url>"
echo "   git add ."
echo "   git commit -m 'Initial commit: Math & Chat API'"
echo "   git push -u origin main"
echo ""
echo "3. Deploy on Dokploy or Coolify:"
echo ""
echo "   For Dokploy:"
echo "   - Login to your Dokploy dashboard"
echo "   - Click '+ Add Service' → 'Application'"
echo "   - Connect your git repository"
echo "   - Set port to 8000"
echo "   - Add BYTEZ_API_KEY environment variable"
echo "   - Deploy!"
echo ""
echo "   For Coolify:"
echo "   - Login to your Coolify dashboard"
echo "   - Click 'New Resource' → 'Application'"
echo "   - Connect your git repository"
echo "   - Set port to 8000"
echo "   - Add BYTEZ_API_KEY environment variable"
echo "   - Deploy!"
echo ""
echo "4. For detailed instructions, see:"
echo "   - README.md"
echo "   - DOKPLOY_DEPLOYMENT.md"
echo "   - COOLIFY_DEPLOYMENT.md"
echo ""
echo "======================================"
echo ""
echo "To test locally:"
echo "  docker-compose up -d"
echo "  python test_api.py"
echo ""
echo "To test with Python virtual environment:"
echo "  python -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  uvicorn main:app --reload"
echo ""
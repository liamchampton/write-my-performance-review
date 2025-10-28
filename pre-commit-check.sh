#!/bin/bash

# Pre-commit security check script for Activity Impact Tracker
# Run this before pushing to GitHub

echo "🔐 Running pre-commit security checks..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# Check 1: Verify .env is ignored
echo "1. Checking if .env is properly ignored..."
if git check-ignore .env > /dev/null 2>&1; then
    echo -e "${GREEN}✅ .env is in .gitignore${NC}"
else
    echo -e "${RED}❌ CRITICAL: .env is NOT ignored!${NC}"
    FAILED=1
fi

# Check 2: Verify .env is not staged
echo "2. Checking if .env is staged..."
if git diff --cached --name-only | grep -q "^\.env$"; then
    echo -e "${RED}❌ CRITICAL: .env is staged for commit!${NC}"
    echo "   Run: git reset HEAD .env"
    FAILED=1
else
    echo -e "${GREEN}✅ .env is not staged${NC}"
fi

# Check 3: Verify activities_data.json is ignored
echo "3. Checking if activities_data.json is ignored..."
if git check-ignore activities_data.json > /dev/null 2>&1; then
    echo -e "${GREEN}✅ activities_data.json is ignored${NC}"
else
    echo -e "${YELLOW}⚠️  activities_data.json might not be ignored${NC}"
fi

# Check 4: Search for potential secrets in staged files
echo "4. Scanning staged files for potential secrets..."
SECRET_MATCHES=$(git diff --cached | grep -inE "(api_key|password|secret|token|credential).*=.*['\"][^'\"]{20,}")
if [ -n "$SECRET_MATCHES" ]; then
    echo -e "${RED}❌ WARNING: Potential secrets found in staged files!${NC}"
    echo ""
    echo "Found in the following lines:"
    echo "$SECRET_MATCHES" | while IFS= read -r line; do
        echo -e "${YELLOW}   $line${NC}"
    done
    echo ""
    echo "   Review your changes carefully with: git diff --cached"
    FAILED=1
else
    echo -e "${GREEN}✅ No obvious secrets detected${NC}"
fi

# Check 5: Verify .env.example has no real credentials
echo "5. Checking .env.example for placeholder values..."
if grep -q "your-api-key-here\|your-resource-name\|your-deployment-name" .env.example; then
    echo -e "${GREEN}✅ .env.example uses placeholder values${NC}"
else
    echo -e "${RED}❌ WARNING: .env.example might contain real credentials!${NC}"
    FAILED=1
fi

# Check 6: Verify config.py uses environment variables
echo "6. Verifying config.py uses environment variables..."
if grep -q "os.environ.get" config.py; then
    echo -e "${GREEN}✅ config.py uses environment variables${NC}"
else
    echo -e "${RED}❌ WARNING: config.py might have hardcoded values!${NC}"
    FAILED=1
fi

# Check 7: Look for test files with credentials
echo "7. Checking test files..."
if find tests/ -type f -name "*.py" -exec grep -l "AZURE_AI.*=" {} \; 2>/dev/null | grep -v "conftest.py"; then
    echo -e "${YELLOW}⚠️  Test files might contain credentials${NC}"
else
    echo -e "${GREEN}✅ No credentials found in test files${NC}"
fi

echo ""
echo "========================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All security checks passed!${NC}"
    echo ""
    echo "You are safe to push to GitHub 🚀"
    echo ""
    echo "Next steps:"
    echo "  git add ."
    echo "  git commit -m \"Initial commit\""
    echo "  git push origin main"
    exit 0
else
    echo -e "${RED}❌ Security checks FAILED!${NC}"
    echo ""
    echo "⚠️  DO NOT PUSH TO GITHUB YET!"
    echo ""
    echo "Fix the issues above before committing."
    echo "Review SECURITY.md for guidance."
    exit 1
fi

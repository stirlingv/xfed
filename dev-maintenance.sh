#!/usr/bin/env bash

# XFED Development Environment Setup & Maintenance Script
# Run this periodically to keep your development environment updated

echo "🚀 XFED Development Environment Maintenance"
echo "=========================================="

# Activate virtual environment if not already active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    if [[ $? -ne 0 ]]; then
        echo "❌ Could not activate virtual environment"
        echo "💡 Make sure you're in the project root with a 'venv' directory"
        exit 1
    fi
else
    echo "✅ Virtual environment already active: $VIRTUAL_ENV"
fi

echo ""

# Check and update pip
echo "📦 Checking pip version..."
current_pip=$(pip --version | grep -o 'pip [0-9.]*' | grep -o '[0-9.]*')
echo "   Current: pip $current_pip"

# Update pip
echo "🔄 Updating pip to latest version..."
python -m pip install --upgrade pip --quiet

new_pip=$(pip --version | grep -o 'pip [0-9.]*' | grep -o '[0-9.]*')
if [[ "$current_pip" != "$new_pip" ]]; then
    echo "   ✅ Updated pip from $current_pip to $new_pip"
else
    echo "   ✅ pip was already up to date ($current_pip)"
fi

echo ""

# Check for outdated packages
echo "📋 Checking for outdated packages..."
outdated_count=$(pip list --outdated --format=json 2>/dev/null | python -c "import json, sys; data = json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")

if [[ "$outdated_count" -gt "0" ]]; then
    echo "   ⚠️  Found $outdated_count outdated packages"
    echo "   📄 Outdated packages:"
    pip list --outdated --format=columns 2>/dev/null || echo "   Could not list outdated packages"
    echo ""
    echo "   💡 To update all packages: pip install --upgrade \$(pip list --outdated --format=json | python -c 'import json, sys; print(\" \".join([pkg[\"name\"] for pkg in json.load(sys.stdin)]))')"
else
    echo "   ✅ All packages are up to date"
fi

echo ""

# Check Django and project status
echo "🔍 Checking Django project status..."
python -c "
import django
from django.conf import settings
django.setup()
print(f'   Django version: {django.get_version()}')
print('   ✅ Django project loads successfully')
" 2>/dev/null || echo "   ⚠️  Could not load Django project (migrations needed?)"

echo ""

# Run navigation status check
if [[ -f "./navigation.sh" ]]; then
    echo "🧭 Navigation system status:"
    ./navigation.sh status
fi

echo ""
echo "🎯 Development Environment Summary:"
echo "  • Virtual environment: Active"
echo "  • pip: Updated to latest version"
echo "  • Packages: $outdated_count outdated"
echo ""

if [[ "$outdated_count" -gt "0" ]]; then
    echo "💡 Recommendations:"
    echo "  1. Review outdated packages and update as needed"
    echo "  2. Test your application after updates"
    echo "  3. Update requirements.txt if you upgrade core dependencies"
fi

echo "✨ Maintenance check complete!"

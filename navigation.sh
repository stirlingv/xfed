#!/usr/bin/env bash

# Navigation Management Script for XFED
# This script helps manage navigation content between development and production

echo "🚀 XFED Navigation Management"
echo "=============================="

# Function to export navigation data
export_navigation() {
    echo "📤 Exporting navigation data to fixtures..."
    python manage.py dumpdata main.NavigationItem main.SocialMediaLink \
        --indent 2 \
        --output fixtures/navigation.json

    if [ $? -eq 0 ]; then
        echo "✅ Navigation data exported successfully to fixtures/navigation.json"
        echo "📋 Found:"
        echo "   - $(python -c "import json; data=json.load(open('fixtures/navigation.json')); print(len([x for x in data if x['model']=='main.navigationitem']))")" navigation items
        echo "   - $(python -c "import json; data=json.load(open('fixtures/navigation.json')); print(len([x for x in data if x['model']=='main.socialmedialink']))")" social media links

        # Check if fixture has changes and auto-stage it
        if git status --porcelain fixtures/navigation.json | grep -q "fixtures/navigation.json"; then
            echo "🔄 Navigation fixture has changes - staging for commit"
            git add fixtures/navigation.json
        else
            echo "ℹ️  Navigation fixture unchanged"
        fi
    else
        echo "❌ Export failed!"
        exit 1
    fi
}

# Function to commit navigation changes
commit_navigation() {
    echo "💾 Committing navigation changes..."

    # First export the current navigation
    export_navigation

    # Check if there are changes to commit
    if git diff --cached --quiet fixtures/navigation.json; then
        echo "⚠️  No navigation changes to commit"
        return 0
    fi

    # Get commit message
    if [ -z "$1" ]; then
        echo "📝 Enter commit message for navigation changes:"
        read commit_message
    else
        commit_message="$1"
    fi

    # Commit the changes
    git commit -m "Navigation: $commit_message"

    if [ $? -eq 0 ]; then
        echo "✅ Navigation changes committed successfully!"
        echo "💡 Run 'git push origin main' to deploy to production"
    else
        echo "❌ Commit failed!"
        exit 1
    fi
}

# Function to import navigation data
import_navigation() {
    echo "📥 Importing navigation data from fixtures..."

    if [ ! -f "fixtures/navigation.json" ]; then
        echo "❌ No navigation.json fixture found!"
        echo "💡 Run './navigation.sh export' first to create fixture"
        exit 1
    fi

    python manage.py loaddata fixtures/navigation.json

    if [ $? -eq 0 ]; then
        echo "✅ Navigation data imported successfully!"
    else
        echo "❌ Import failed!"
        exit 1
    fi
}

# Function to reset navigation to defaults
reset_navigation() {
    echo "🔄 Resetting navigation to defaults..."
    python manage.py create_default_navigation

    if [ $? -eq 0 ]; then
        echo "✅ Navigation reset to defaults!"
        echo "💡 Run './navigation.sh export' to save these defaults as fixtures"
    else
        echo "❌ Reset failed!"
        exit 1
    fi
}

# Function to check and update pip
check_pip() {
    echo "🔧 Checking pip version..."
    current_version=$(pip --version | grep -o 'pip [0-9.]*' | grep -o '[0-9.]*')
    echo "   Current pip version: $current_version"

    # Check for updates (suppress output to avoid clutter)
    pip list --outdated --format=json 2>/dev/null | python -c "
import json, sys
data = json.load(sys.stdin)
pip_outdated = [pkg for pkg in data if pkg['name'] == 'pip']
if pip_outdated:
    print(f'   ⚠️  pip update available: {pip_outdated[0][\"latest_version\"]}')
    print('   💡 Run: pip install --upgrade pip')
else:
    print('   ✅ pip is up to date')
" 2>/dev/null || echo "   ℹ️  Could not check for pip updates"
}

# Function to show current navigation status
status() {
    echo "📊 Current Navigation Status:"
    echo "----------------------------"

    # Check pip version
    check_pip
    echo ""

    # Check if models exist (migrations run)
    python -c "
from main.models import NavigationItem, SocialMediaLink
try:
    nav_count = NavigationItem.objects.count()
    social_count = SocialMediaLink.objects.count()
    active_nav = NavigationItem.objects.filter(is_active=True).count()
    print(f'📁 Navigation Items: {nav_count} total, {active_nav} active')
    print(f'🔗 Social Links: {social_count} total')

    if nav_count == 0:
        print('⚠️  No navigation items found - run reset to create defaults')
    else:
        print('✅ Navigation system is set up')

except Exception as e:
    print('❌ Database not ready - run migrations first')
    print(f'   Error: {e}')
" 2>/dev/null || echo "❌ Could not check status - ensure migrations are run"

    # Check if fixture exists
    if [ -f "fixtures/navigation.json" ]; then
        echo "📄 Fixture: fixtures/navigation.json exists"
    else
        echo "⚠️  No fixture file found"
    fi
}

# Main script logic
case "$1" in
    "export")
        export_navigation
        ;;
    "import")
        import_navigation
        ;;
    "reset")
        reset_navigation
        ;;
    "status")
        status
        ;;
    "commit")
        commit_navigation "$2"
        ;;
    *)
        echo "Usage: $0 {export|import|reset|status|commit}"
        echo ""
        echo "Commands:"
        echo "  export          - Export current navigation to fixtures/navigation.json"
        echo "  import          - Import navigation from fixtures/navigation.json"
        echo "  reset           - Reset navigation to default items"
        echo "  status          - Show current navigation status"
        echo "  commit [msg]    - Export, stage, and commit navigation changes"
        echo ""
        echo "Typical workflow:"
        echo "  1. ./navigation.sh reset              # Set up defaults"
        echo "  2. Edit navigation in admin interface"
        echo "  3. ./navigation.sh commit 'Add services menu'  # Export & commit"
        echo "  4. git push origin main               # Deploy to production"
        echo ""
        echo "Or use the pre-commit hook (already installed) to auto-export on any commit!"
        exit 1
        ;;
esac

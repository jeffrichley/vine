#!/bin/bash
# Test CI workflows in generated projects

set -e

PROJECT_NAME="ci-test-project"
TEST_DIR="/tmp/$PROJECT_NAME"

echo "🧪 Testing CI workflows in generated project..."

# Clean up previous test
rm -rf "$TEST_DIR"

# Generate test project
echo "📦 Generating test project..."
copier copy . "$TEST_DIR" --trust --data-file test-data.yaml

cd "$TEST_DIR"

# Create GitHub repo
echo "🔗 Creating GitHub repo..."
gh repo create "$PROJECT_NAME" --private --push

# Test 1: Pre-commit-ci auto-fixes
echo "🔧 Testing pre-commit-ci auto-fixes..."
echo "def bad_function(  ): return 'bad'" >> src/test_seedling_project/test.py
git add .
git commit -m "test: add poorly formatted code"
git push

echo "⏳ Waiting for pre-commit-ci to run..."
sleep 30

# Check if auto-fix commit was made
if git log --oneline | grep -q "pre-commit-ci"; then
    echo "✅ pre-commit-ci auto-fix working"
else
    echo "❌ pre-commit-ci auto-fix failed"
    exit 1
fi

# Test 2: Type checking failure
echo "🔍 Testing type checking failure..."
echo "def bad_type() -> str: return 42" >> src/test_seedling_project/test.py
git add .
git commit -m "test: add type error"
git push

echo "⏳ Waiting for CI to run..."
sleep 30

# Check CI status
if gh pr list --json statusCheckRollup | grep -q "FAILURE"; then
    echo "✅ CI correctly blocked merge on type error"
else
    echo "❌ CI did not block merge on type error"
    exit 1
fi

echo "🎉 All CI tests passed!"

# Cleanup
gh repo delete "$PROJECT_NAME" --yes

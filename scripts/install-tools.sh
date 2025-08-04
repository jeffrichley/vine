#!/bin/bash
# Install all recommended tools for Seedling
# Usage: ./scripts/install-tools.sh

set -e

echo "🌱 Installing recommended tools for Seedling..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install uv
print_status "Installing uv..."
if command_exists uv; then
    print_warning "uv is already installed"
else
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        curl -LsSf https://astral.sh/uv/install.sh | sh
        print_success "uv installed successfully"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -LsSf https://astral.sh/uv/install.sh | sh
        print_success "uv installed successfully"
        # Update PATH for current session
        export PATH="$HOME/.local/bin:$PATH"
    else
        print_error "Unsupported OS: $OSTYPE"
        print_warning "Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
fi

# Install Copier using uv
print_status "Installing Copier..."
if command_exists copier; then
    print_warning "Copier is already installed"
else
    if command_exists uv; then
        uv pip install --system copier
        print_success "Copier installed successfully"
    else
        print_error "uv not found. Please install uv first."
        exit 1
    fi
fi

# Install Nox using uv
print_status "Installing Nox..."
if command_exists nox; then
    print_warning "Nox is already installed"
else
    if command_exists uv; then
        uv pip install --system nox
        print_success "Nox installed successfully"
    else
        print_error "uv not found. Please install uv first."
        exit 1
    fi
fi

# Install Just
print_status "Installing Just..."
if command_exists just; then
    print_warning "Just is already installed"
else
    # Use the official Just install script
    if curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin; then
        print_success "Just installed successfully"
    else
        print_error "Failed to install Just using the official installer"
        print_warning "Please install Just manually: https://just.systems/man/en/"
        exit 1
    fi
fi

echo ""
print_success "Installation complete!"
echo ""
echo "Installed tools:"
echo "  • uv: $(uv --version 2>/dev/null || echo 'Not found')"
echo "  • Copier: $(copier --version 2>/dev/null || echo 'Not found')"
echo "  • Nox: $(nox --version 2>/dev/null | head -1 || echo 'Not found')"
echo "  • Just: $(just --version 2>/dev/null || echo 'Not found')"

# Verify all tools are actually available
echo ""
echo "Verification:"
if command_exists uv; then
    print_success "✓ uv is available"
else
    print_error "✗ uv is not available"
fi

if command_exists copier; then
    print_success "✓ copier is available"
else
    print_error "✗ copier is not available"
fi

if command_exists nox; then
    print_success "✓ nox is available"
else
    print_error "✗ nox is not available"
fi

if command_exists just; then
    print_success "✓ just is available"
else
    print_error "✗ just is not available"
fi
echo ""
echo "Next steps:"
echo "  1. Generate a new project: copier copy https://github.com/jeffrichley/seedling.git my-awesome-project"
echo "  2. Navigate to your project: cd my-awesome-project"
echo "  3. Install dependencies: uv sync"
echo "  4. Start developing!"
echo ""
echo "For more information, see the documentation: https://jeffrichley.github.io/seedling/" 
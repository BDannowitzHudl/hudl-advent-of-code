#!/usr/bin/env bash
set -e

# Script to collect all devcontainer post create commands.
# This keeps the devcontainer.json file cleaner and the postCreate command more readable.
#
# This script must be run from the parent directory of the `.devcontainer` directory.

if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    [ -f "$HOME/.local/bin/env" ] && source "$HOME/.local/bin/env"
fi

# Make bash_env.sh executable and ensure BASH_ENV is set
if [ -f .devcontainer/bash_env.sh ]; then
    chmod +x .devcontainer/bash_env.sh
    export BASH_ENV="$(pwd)/.devcontainer/bash_env.sh"
fi

.pymarvel/install_oh_my_bash.sh

add_uv_config() {
    local rc_file="$1"
    if [ -f "$rc_file" ] && ! grep -q '.local/bin' "$rc_file" 2>/dev/null; then
        {
            echo ''
            echo '# Add uv to PATH'
            echo 'export PATH="$HOME/.local/bin:$PATH"'
            echo 'export UV_LINK_MODE=copy'
            echo 'if [ -f .pymarvel/build_tokens.sh ]; then'
            echo '  source .pymarvel/build_tokens.sh uv-apply 2>/dev/null'
            echo 'fi'
            echo ''
            echo '# Function to refresh uv CodeArtifact tokens'
            echo 'uv-refresh() { source .pymarvel/build_tokens.sh uv-apply; }'
        } >> "$rc_file"
    fi
}

add_uv_config ~/.bashrc
add_uv_config ~/.zshrc

.pymarvel/log_devcontainer_event.sh SUCCEEDED

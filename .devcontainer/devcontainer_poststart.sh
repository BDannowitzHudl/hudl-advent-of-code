#!/usr/bin/env bash
set -e

# Script to collect all devcontainer post start commands.
# This keeps the devcontainer.json file cleaner and the postStart command more readable.
#
# This script must be run from the parent directory of the `.devcontainer` directory.

export PATH="$HOME/.local/bin:$PATH"
[ -f "$HOME/.local/bin/env" ] && source "$HOME/.local/bin/env"
export UV_LINK_MODE=copy

.pymarvel/build_tokens.sh fetch-token

if [ ! -f .devcontainer/pypi-token.txt ]; then
    echo "Error: PyPI token file not found"
    exit 1
fi

export UV_INDEX_HUDL_USERNAME=aws
export UV_INDEX_HUDL_PASSWORD=$(cat .devcontainer/pypi-token.txt)

[ ! -d ".venv" ] && uv venv .venv

uv sync

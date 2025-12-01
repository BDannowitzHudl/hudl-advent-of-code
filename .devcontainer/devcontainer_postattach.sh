#!/usr/bin/env bash
set -e

# Script to collect all devcontainer post attach commands.
# This keeps the devcontainer.json file cleaner and the postAttach command more readable.
#
# This script must be run from the parent directory of the `.devcontainer` directory.

export PATH="$HOME/.local/bin:$PATH"
[ -f "$HOME/.local/bin/env" ] && source "$HOME/.local/bin/env"

source .pymarvel/build_tokens.sh

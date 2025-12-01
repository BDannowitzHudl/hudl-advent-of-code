#!/usr/bin/env bash

# URL of the AML ECR Registry to check if the ECR Credentials helper is configured.
AWS_DOMAIN_OWNER="690616407375"
AWS_REGION="us-east-1"
ECR_DOMAIN="${AWS_DOMAIN_OWNER}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# File to store the access token into.
PYPI_TOKEN_LOCATION=${PYPI_TOKEN_LOCATION:-".devcontainer/pypi-token.txt"}

# How long tokens will be valid for (30 minutes by default).
TOKEN_TTL=${TOKEN_TTL:-1800}

## INDIVIDUAL STEPS ##

# Log into ECR, if docker is installed and ECR Credentials helper is not or running on Codebuild.
docker_access() {
  if which docker >/dev/null 2>/dev/null; then
    if docker_ecr_ready && ! running_on_codebuild; then
      echo "Found ECR Credentials helper, skipping ECR Login"
    else
      echo "Configuring ECR access for Docker"
      echo "AWS_PROFILE: ${AWS_PROFILE}"
      ${AWS_CLI_PATH}aws ecr get-login-password --region $AWS_REGION | \
        docker login --username AWS --password-stdin $AWS_DOMAIN_OWNER.dkr.ecr.$AWS_REGION.amazonaws.com
    fi
  else
    echo "Docker not found, skpping login"
  fi
}

# Check if the ECR credentials helper is installed and configured.
docker_ecr_ready() {
  which docker-credential-ecr-login >/dev/null 2>/dev/null
}

# Check if running on CodeBuild by checking the presence of the CODEBUILD_BUILD_ID environment variable.
running_on_codebuild() {
  [ -n "$CODEBUILD_BUILD_ID" ]
}

# Generate an access token to the CodeArtifacts internal repository.
# This is used by both tools (such as uv below) and docker intermediate build stages.
fetch_token() {
  echo "Fetching fresh internal PyPi token"
  # Ensure the directory exists
  mkdir -p "$(dirname "${PYPI_TOKEN_LOCATION}")"
  # Remove existing file if it exists to avoid noclobber issues
  [ -f "${PYPI_TOKEN_LOCATION}" ] && rm -f "${PYPI_TOKEN_LOCATION}"
  # Write token to file
  ${AWS_CLI_PATH}aws codeartifact get-authorization-token \
    --domain hudlaml \
    --domain-owner 690616407375 \
    --duration-seconds "${TOKEN_TTL}" \
    --query authorizationToken \
    --output text \
    --region ${AWS_REGION} > "${PYPI_TOKEN_LOCATION}" || {
    echo "Error: Failed to fetch token" >&2
    return 1
  }
}

# Configure pip with additional access to the internal packages.
# This is used to pip install build tools during the INSTALL phase.
pip_access() {
  echo "Configuring PyPi access for pip"
  ${AWS_CLI_PATH}aws codeartifact login \
    --tool pip \
    --domain hudlaml \
    --domain-owner 690616407375 \
    --repository hudlaml \
    --duration-seconds "${TOKEN_TTL}" \
    --region ${AWS_REGION}

  # We want the internal index to be extra, not the only option.
  # Since this is not supported by the aws cli we shuffle pip's config after logging in.
  pip config set 'global.extra-index-url' "$(pip config get 'global.index-url')"
  pip config unset 'global.index-url'
}

# Configure uv, if present, in the build environment with access to internal packages.
# This is used by library builds to fetch dependencies during the INSTALL phase.
# Fetches a fresh token and exports environment variables for uv.
# Usage: uv_apply [--skip-fetch] - skip fetching token if already present
uv_apply() {
  if which uv >/dev/null 2>/dev/null; then
    echo "Configuring PyPi access for uv"
    # Fetch token unless --skip-fetch is passed
    if [ "${1:-}" != "--skip-fetch" ]; then
      fetch_token
    fi
    export UV_INDEX_HUDL_USERNAME=aws
    export UV_INDEX_HUDL_PASSWORD=$(cat "${PYPI_TOKEN_LOCATION}")
  else
    echo "uv not found, skipping configuration"
  fi
}

## ENTRY POINT ##
# Handle both sourced and directly executed cases
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
  # Script is being executed directly
  set -e
  case "${1:-}" in
    "")
      fetch_token
      pip_access
      uv_apply --skip-fetch
      docker_access
      ;;
    fetch-token)
      fetch_token
      ;;
    pip)
      pip_access
      ;;
    uv-apply)
      uv_apply
      ;;
    python)
      fetch_token
      pip_access
      uv_apply --skip-fetch
      ;;
    docker)
      docker_access
      ;;
    *)
      echo "Unsupported option '${1}'" >&2
      echo "" >&2
      echo "Usage: source .pymarvel/build_tokens.sh [MODE]" >&2
      echo "   OR: .pymarvel/build_tokens.sh [MODE]" >&2
      echo "" >&2
      echo "MODE can be one of:" >&2
      echo "  fetch-token    Fetch a PyPI token to access the AML internal repository" >&2
      echo "  pip            Configure PIP to use the AML internal repository as a secondary source" >&2
      echo "  uv-apply       Configure access to the AML internal repository for uv (requires token)" >&2
      echo "  docker         Configure docker access to AML private repositories" >&2
      echo "" >&2
      echo "Default (no argument): fetch-token, pip, uv, and docker" >&2
      echo "" >&2
      echo "Note: Source the script to persist environment variables:" >&2
      echo "      source .pymarvel/build_tokens.sh" >&2
      exit 1
      ;;
  esac
else
  # Script is being sourced
  case "${1:-}" in
    "")
      fetch_token
      pip_access
      uv_apply --skip-fetch
      docker_access
      ;;
    fetch-token)
      fetch_token
      ;;
    pip)
      pip_access
      ;;
    uv-apply)
      uv_apply
      ;;
    python)
      fetch_token
      pip_access
      uv_apply --skip-fetch
      ;;
    docker)
      docker_access
      ;;
    *)
      echo "Unsupported option '${1}'" >&2
      return 1 2>/dev/null || exit 1
      ;;
  esac
fi

#!/usr/bin/env bash
set -e

# Script to convert a Poetry-style pyproject.toml to uv-style (PEP 621)
# Usage: ./convert_poetry_to_uv.sh [pyproject.toml]
#
# Requirements:
#   - Python 3 with 'toml' library installed
#   - Install with: pip install toml
#   - Or use Python 3.11+ which has tomllib built-in (script will need minor modification)

PYPROJECT_FILE="${1:-pyproject.toml}"

if [ ! -f "$PYPROJECT_FILE" ]; then
    echo "Error: $PYPROJECT_FILE not found"
    exit 1
fi

# Check if toml library is available
if ! python3 -c "import toml" 2>/dev/null; then
    echo "Error: 'toml' Python library not found."
    echo ""
    echo "Please install it with one of these methods:"
    echo "  1. pip install toml"
    echo "  2. pip install --user toml"
    echo "  3. python3 -m pip install toml"
    echo ""
    echo "Or if you have Python 3.11+, you can modify this script to use 'tomllib' instead."
    exit 1
fi

# Check if file is already converted (has [project] section)
if grep -q '^\[project\]' "$PYPROJECT_FILE"; then
    echo "Warning: $PYPROJECT_FILE already appears to be in uv/PEP 621 format"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create backup
BACKUP_FILE="${PYPROJECT_FILE}.poetry-backup"
cp "$PYPROJECT_FILE" "$BACKUP_FILE"
echo "Created backup: $BACKUP_FILE"

# Use Python to do the conversion (more reliable than pure bash)
PYPROJECT_FILE="$PYPROJECT_FILE" python3 << 'PYTHON_SCRIPT'
import sys
import re
from pathlib import Path
import toml

def convert_version_constraint(version_str):
    """Convert Poetry version constraints to PEP 440 compatible format"""
    if not version_str:
        return ""
    
    version_str = str(version_str).strip().strip('"').strip("'")
    
    # Handle ^ constraint: ^1.2.3 becomes >=1.2.3,<2.0.0
    # For major version 0: ^0.2.3 becomes >=0.2.3,<0.3.0
    if version_str.startswith('^'):
        version_str = version_str[1:]
        parts = version_str.split('.')
        if len(parts) >= 1:
            try:
                major = int(parts[0])
                if major == 0 and len(parts) >= 2:
                    # For 0.x versions, bump minor version
                    minor = int(parts[1])
                    return f">={version_str},<0.{minor + 1}.0"
                else:
                    # For 1.x+ versions, bump major version
                    return f">={version_str},<{major + 1}.0.0"
            except ValueError:
                return f">={version_str}"
        return f">={version_str}"
    
    # Handle ~ constraint: ~1.2.3 becomes >=1.2.3,<1.3.0
    if version_str.startswith('~'):
        version_str = version_str[1:]
        parts = version_str.split('.')
        if len(parts) >= 2:
            try:
                major, minor = int(parts[0]), int(parts[1])
                return f">={version_str},<{major}.{minor + 1}.0"
            except ValueError:
                return f">={version_str}"
        return f">={version_str}"
    
    # Handle >=, <=, ==, !=, etc. (keep as-is)
    if any(version_str.startswith(op) for op in ['>=', '<=', '==', '!=', '>', '<']):
        return version_str
    
    # Default: add >= if no operator
    if version_str and not any(version_str.startswith(op) for op in ['>=', '<=', '==', '!=', '>', '<', '*']):
        return f">={version_str}"
    
    return version_str

def format_dependency(name, spec):
    """Format a dependency entry"""
    if isinstance(spec, dict):
        version = spec.get('version', '')
        extras = spec.get('extras', [])
        git = spec.get('git')
        path = spec.get('path')
        
        if git:
            # Git dependencies - keep as-is for now (uv supports git URLs)
            ref = spec.get('rev', spec.get('tag', spec.get('branch', '')))
            if ref:
                return f'    "{name} @ git+{git}@{ref}",'
            return f'    "{name} @ git+{git}",'
        
        if path:
            return f'    "{name} @ file://{path}",'
        
        version_str = convert_version_constraint(version)
        if extras:
            extras_str = '[' + ','.join(extras) + ']'
            return f'    "{name}{extras_str}{version_str}",'
        else:
            return f'    "{name}{version_str}",'
    elif isinstance(spec, str):
        version_str = convert_version_constraint(spec)
        return f'    "{name}{version_str}",'
    else:
        return f'    "{name}",'

def convert_pyproject(file_path):
    """Convert Poetry pyproject.toml to uv/PEP 621 format"""
    # Try to import toml library
    try:
        import toml
    except ImportError:
        print("Error: 'toml' library not found.", file=sys.stderr)
        print("Please install it with: pip install toml", file=sys.stderr)
        print("Or use Python 3.11+ which has tomllib built-in", file=sys.stderr)
        sys.exit(1)
    
    try:
        data = toml.load(file_path)
    except Exception as e:
        print(f"Error parsing TOML: {e}", file=sys.stderr)
        print("Falling back to line-by-line conversion...", file=sys.stderr)
        return convert_pyproject_line_by_line(file_path)
    
    # Read original file to preserve comments and formatting for non-Poetry sections
    original_lines = Path(file_path).read_text().split('\n')
    output_lines = []
    
    # Extract Poetry data
    poetry_data = data.get('tool', {}).get('poetry', {})
    poetry_deps = poetry_data.get('dependencies', {})
    poetry_groups = poetry_data.get('group', {})
    poetry_dev_deps = poetry_groups.get('dev', {}).get('dependencies', {})
    poetry_sources = data.get('tool', {}).get('poetry', {}).get('source', [])
    
    # Extract project metadata
    project_name = poetry_data.get('name', '')
    project_version = poetry_data.get('version', '0.1.0')
    project_description = poetry_data.get('description', '')
    project_authors = poetry_data.get('authors', [])
    python_version = poetry_deps.pop('python', None)
    
    # Build output
    in_poetry_section = False
    in_build_system = False
    poetry_section_handled = False
    
    i = 0
    while i < len(original_lines):
        line = original_lines[i]
        stripped = line.strip()
        
        # Skip Poetry sections
        if stripped.startswith('[tool.poetry]'):
            in_poetry_section = True
            i += 1
            continue
        elif stripped.startswith('[tool.poetry.dependencies]'):
            in_poetry_section = True
            i += 1
            continue
        elif stripped.startswith('[tool.poetry.group.dev.dependencies]'):
            in_poetry_section = True
            i += 1
            continue
        elif stripped.startswith('[[tool.poetry.source]]'):
            in_poetry_section = True
            i += 1
            continue
        elif stripped.startswith('[build-system]'):
            in_build_system = True
            output_lines.append('[build-system]')
            output_lines.append('requires = ["hatchling"]')
            output_lines.append('build-backend = "hatchling.build"')
            # Skip until next section
            i += 1
            while i < len(original_lines) and not original_lines[i].strip().startswith('['):
                i += 1
            continue
        elif stripped.startswith('[') and not stripped.startswith('[['):
            # New section starting
            if in_poetry_section and not poetry_section_handled:
                # Insert converted [project] section
                output_lines.append('')
                output_lines.append('[project]')
                if project_name:
                    output_lines.append(f'name = "{project_name}"')
                if project_version:
                    output_lines.append(f'version = "{project_version}"')
                if project_description:
                    output_lines.append(f'description = "{project_description}"')
                if project_authors:
                    authors_str = str(project_authors).replace("'", '"')
                    output_lines.append(f'authors = {authors_str}')
                if python_version:
                    python_req = convert_version_constraint(python_version)
                    output_lines.append(f'requires-python = "{python_req}"')
                
                output_lines.append('dependencies = [')
                for name, spec in sorted(poetry_deps.items()):
                    if name != 'python':  # Already handled
                        output_lines.append(format_dependency(name, spec))
                output_lines.append(']')
                output_lines.append('')
                
                # Add dev dependencies if they exist
                if poetry_dev_deps:
                    output_lines.append('[dependency-groups]')
                    output_lines.append('dev = [')
                    for name, spec in sorted(poetry_dev_deps.items()):
                        output_lines.append(format_dependency(name, spec))
                    output_lines.append(']')
                    output_lines.append('')
                
                # Add uv indexes for non-PyPI sources
                if poetry_sources:
                    for source in poetry_sources:
                        if source.get('name') != 'PyPI':
                            output_lines.append('[[tool.uv.index]]')
                            output_lines.append(f'name = "{source.get("name", "private").lower()}"')
                            output_lines.append(f'url = "{source.get("url", "")}"')
                            output_lines.append('explicit = false')
                            output_lines.append('')
                
                poetry_section_handled = True
                in_poetry_section = False
            
            # Keep non-Poetry sections
            output_lines.append(line)
            i += 1
            continue
        
        # Skip lines in Poetry sections
        if in_poetry_section:
            i += 1
            continue
        
        # Keep all other lines
        output_lines.append(line)
        i += 1
    
    # Handle case where file ends while in Poetry section
    if in_poetry_section and not poetry_section_handled:
        output_lines.append('')
        output_lines.append('[project]')
        if project_name:
            output_lines.append(f'name = "{project_name}"')
        if project_version:
            output_lines.append(f'version = "{project_version}"')
        if project_description:
            output_lines.append(f'description = "{project_description}"')
        if project_authors:
            authors_str = str(project_authors).replace("'", '"')
            output_lines.append(f'authors = {authors_str}')
        if python_version:
            python_req = convert_version_constraint(python_version)
            output_lines.append(f'requires-python = "{python_req}"')
        
        output_lines.append('dependencies = [')
        for name, spec in sorted(poetry_deps.items()):
            if name != 'python':
                output_lines.append(format_dependency(name, spec))
        output_lines.append(']')
        output_lines.append('')
        
        if poetry_dev_deps:
            output_lines.append('[dependency-groups]')
            output_lines.append('dev = [')
            for name, spec in sorted(poetry_dev_deps.items()):
                output_lines.append(format_dependency(name, spec))
            output_lines.append(']')
            output_lines.append('')
        
        if poetry_sources:
            for source in poetry_sources:
                if source.get('name') != 'PyPI':
                    output_lines.append('[[tool.uv.index]]')
                    output_lines.append(f'name = "{source.get("name", "private").lower()}"')
                    output_lines.append(f'url = "{source.get("url", "")}"')
                    output_lines.append('explicit = false')
                    output_lines.append('')
    
    return '\n'.join(output_lines)

def convert_pyproject_line_by_line(file_path):
    """Fallback conversion method if TOML parsing fails"""
    # This is a simpler line-by-line approach
    # For now, just return a message
    print("Line-by-line conversion not yet implemented. Please install python-toml: pip install toml")
    sys.exit(1)

# Main conversion
import os
pyproject_path = Path(os.environ['PYPROJECT_FILE'])
try:
    converted = convert_pyproject(pyproject_path)
    pyproject_path.write_text(converted)
    print(f"✓ Converted {pyproject_path} successfully!")
    print(f"  Backup saved to: {pyproject_path}.poetry-backup")
    print("\nNext steps:")
    print("  1. Review the converted pyproject.toml")
    print("  2. Run: uv lock  (to generate uv.lock)")
    print("  3. Run: uv sync  (to install dependencies)")
    print("  4. Test your project")
except Exception as e:
    print(f"Error during conversion: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_SCRIPT

def detect_dependency_changes(baseline_deps: dict, pr_deps: dict) -> dict:
    """Detect dependency changes between baseline and PR.
    
    Args:
        baseline_deps: Dependencies before the PR (e.g., from requirements.txt)
        pr_deps: Dependencies after the PR (e.g., from PR's requirements.txt)
    
    Returns:
        dict: Dependency change analysis results
    """
    # Parse dependencies
    baseline_parsed = _parse_dependencies(baseline_deps)
    pr_parsed = _parse_dependencies(pr_deps)
    
    # Identify changes
    added = []
    removed = []
    updated = []
    unchanged = []
    
    # Check all dependencies in PR
    for name, version in pr_parsed.items():
        if name not in baseline_parsed:
            added.append({'name': name, 'version': version})
        elif baseline_parsed[name] != version:
            updated.append({
                'name': name,
                'old_version': baseline_parsed[name],
                'new_version': version
            })
        else:
            unchanged.append({'name': name, 'version': version})
    
    # Check for removed dependencies
    for name, version in baseline_parsed.items():
        if name not in pr_parsed:
            removed.append({'name': name, 'version': version})
    
    # Generate safety warnings (placeholder for actual safety checks)
    warnings = []
    for dep in added:
        if dep['name'] in ['requests', 'django', 'flask']:  # Example high-risk dependencies
            warnings.append({
                'dependency': dep['name'],
                'version': dep['version'],
                'type': 'security',
                'message': f"High-risk dependency {dep['name']} version {dep['version']} may have known vulnerabilities"
            })
    
    for dep in updated:
        if dep['name'] in ['requests', 'django', 'flask']:  # Example high-risk dependencies
            warnings.append({
                'dependency': dep['name'],
                'version': dep['new_version'],
                'type': 'security',
                'message': f"High-risk dependency {dep['name']} version {dep['new_version']} may have known vulnerabilities"
            })
    
    return {
        'added': added,
        'removed': removed,
        'updated': updated,
        'unchanged': unchanged,
        'warnings': warnings,
        'total_changes': len(added) + len(removed) + len(updated)
    }

def _parse_dependencies(deps: dict) -> dict:
    """Parse dependencies from input format to a normalized dictionary.
    
    Args:
        deps: Dependencies in various formats
    
    Returns:
        dict: Normalized dependencies (name: version)
    """
    # Handle different formats
    if isinstance(deps, str):
        return _parse_requirements_txt(deps)
    elif isinstance(deps, dict):
        return deps
    return {}

def _parse_requirements_txt(requirements: str) -> dict:
    """Parse requirements.txt content into a dictionary.
    
    Args:
        requirements: Content of requirements.txt
    
    Returns:
        dict: Dependencies (name: version)
    """
    parsed = {}
    for line in requirements.split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue
        # Handle simple cases: package==version
        if '==' in line:
            name, version = line.split('==', 1)
            parsed[name.strip()] = version.strip()
        elif '>=' in line:
            name, version = line.split('>=', 1)
            parsed[name.strip()] = version.strip()
        elif '<=' in line:
            name, version = line.split('<=', 1)
            parsed[name.strip()] = version.strip()
        else:
            parsed[line.strip()] = 'latest'
    return parsed

def analyze_test_coverage(baseline_coverage: dict, pr_coverage: dict) -> dict:
    """Analyze test coverage changes in a PR.
    
    Args:
        baseline_coverage: Coverage data before the PR (e.g., from main branch)
        pr_coverage: Coverage data after the PR (e.g., from PR branch)
    
    Returns:
        dict: Coverage analysis results
    """
    # Calculate overall coverage change
    baseline_total = baseline_coverage.get('total', 0.0)
    pr_total = pr_coverage.get('total', 0.0)
    coverage_change = pr_total - baseline_total
    
    # Identify files with coverage changes
    changed_files = []
    
    baseline_files = baseline_coverage.get('files', {})
    pr_files = pr_coverage.get('files', {})
    
    # Check all files in PR coverage
    for file_path, pr_file_coverage in pr_files.items():
        baseline_file_coverage = baseline_files.get(file_path, {})
        
        baseline_file_total = baseline_file_coverage.get('coverage', 0.0)
        pr_file_total = pr_file_coverage.get('coverage', 0.0)
        
        file_coverage_change = pr_file_total - baseline_file_total
        
        # Identify untested lines in new code
        pr_lines = pr_file_coverage.get('lines', {})
        baseline_lines = baseline_file_coverage.get('lines', {})
        
        untested_new_lines = []
        for line_num, covered in pr_lines.items():
            if line_num not in baseline_lines and not covered:
                untested_new_lines.append(line_num)
        
        if file_coverage_change != 0 or untested_new_lines:
            changed_files.append({
                'file_path': file_path,
                'baseline_coverage': baseline_file_total,
                'pr_coverage': pr_file_total,
                'coverage_change': file_coverage_change,
                'untested_new_lines': untested_new_lines
            })
    
    # Determine coverage status
    status = "improved" if coverage_change > 0 else "declined" if coverage_change < 0 else "unchanged"
    
    return {
        'status': status,
        'baseline_total_coverage': baseline_total,
        'pr_total_coverage': pr_total,
        'coverage_change': coverage_change,
        'changed_files': changed_files,
        'untested_new_files': [file['file_path'] for file in changed_files if file['pr_coverage'] == 0]
    }
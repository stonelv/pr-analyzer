def scan_security_vulnerabilities(code: str, language: str = "python") -> dict:
    """Scan code for security vulnerabilities and code defects.
    
    Args:
        code: Code to scan
        language: Programming language of the code
    
    Returns:
        dict: Security scan results
    """
    vulnerabilities = []
    
    # Simple security checks for MVP
    lines = code.split('\n')
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Check for hardcoded secrets
        if any(secret_keyword in line.lower() for secret_keyword in ['api_key', 'secret', 'password', 'key=', 'token=']):
            if not line.startswith('#'):
                vulnerabilities.append({
                    'line': line_num,
                    'type': 'hardcoded_secret',
                    'message': 'Potential hardcoded secret detected',
                    'severity': 'high'
                })
        
        # Check for SQL injection vulnerabilities
        if any(sql_keyword in line.lower() for sql_keyword in ['execute(', 'query(', 'select ', 'insert ', 'update ', 'delete ']):
            if '%s' not in line and '?' not in line and not line.startswith('#'):
                vulnerabilities.append({
                    'line': line_num,
                    'type': 'sql_injection',
                    'message': 'Potential SQL injection vulnerability detected',
                    'severity': 'high'
                })
        
        # Check for XSS vulnerabilities
        if any(xss_keyword in line.lower() for xss_keyword in ['html(', 'render(', 'escape(', 'safe=']):
            if 'escape' not in line.lower() and not line.startswith('#'):
                vulnerabilities.append({
                    'line': line_num,
                    'type': 'xss',
                    'message': 'Potential XSS vulnerability detected',
                    'severity': 'medium'
                })
        
        # Check for insecure imports
        if line.startswith('import') or line.startswith('from'):
            if any(insecure_module in line for insecure_module in ['pickle', 'eval', 'exec', 'subprocess']):
                vulnerabilities.append({
                    'line': line_num,
                    'type': 'insecure_import',
                    'message': 'Potential insecure module import detected',
                    'severity': 'medium'
                })
    
    # Calculate severity counts
    severity_counts = {
        'high': len([v for v in vulnerabilities if v['severity'] == 'high']),
        'medium': len([v for v in vulnerabilities if v['severity'] == 'medium']),
        'low': len([v for v in vulnerabilities if v['severity'] == 'low'])
    }
    
    return {
        'vulnerabilities': vulnerabilities,
        'severity_counts': severity_counts,
        'total_vulnerabilities': len(vulnerabilities),
        'language': language
    }

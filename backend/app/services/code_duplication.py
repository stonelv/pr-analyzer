def detect_code_duplication(code: str, language: str = "python", min_lines: int = 3) -> dict:
    """Detect duplicate code fragments in the given code.
    
    Args:
        code: Code to scan for duplicates
        language: Programming language of the code
        min_lines: Minimum number of consecutive lines to consider as duplicate
    
    Returns:
        dict: Code duplication analysis results
    """
    lines = code.split('\n')
    line_count = len(lines)
    
    # Create a dictionary to store line sequences and their positions
    sequences = {}
    duplicates = []
    
    # Iterate through lines with sliding window
    for i in range(line_count - min_lines + 1):
        # Extract sequence of min_lines lines
        sequence = tuple(lines[i:i+min_lines])
        
        # Check if sequence already exists
        if sequence in sequences:
            # Found duplicate
            existing_pos = sequences[sequence]
            duplicates.append({
                'original_start': existing_pos,
                'original_end': existing_pos + min_lines - 1,
                'duplicate_start': i,
                'duplicate_end': i + min_lines - 1,
                'code': '\n'.join(sequence)
            })
        else:
            # Store the sequence and its starting position
            sequences[sequence] = i
    
    # Remove duplicate entries (keep only first occurrence)
    unique_duplicates = []
    seen = set()
    for dup in duplicates:
        key = (dup['original_start'], dup['duplicate_start'])
        if key not in seen:
            seen.add(key)
            unique_duplicates.append(dup)
    
    # Calculate duplication metrics
    total_duplicate_lines = sum(dup['duplicate_end'] - dup['duplicate_start'] + 1 for dup in unique_duplicates)
    duplication_ratio = total_duplicate_lines / line_count if line_count > 0 else 0
    
    return {
        'duplicates': unique_duplicates,
        'total_duplicate_lines': total_duplicate_lines,
        'total_lines': line_count,
        'duplication_ratio': duplication_ratio,
        'language': language
    }

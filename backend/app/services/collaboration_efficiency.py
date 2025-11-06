def analyze_collaboration(comments: list) -> dict:
    """Analyze PR comments for collaboration efficiency.
    
    Args:
        comments: List of PR comments
    
    Returns:
        dict: Collaboration analysis results with comment classification and action items
    """
    # Define comment categories and keywords
    categories = {
        'question': ['?', 'question', 'clarify', 'what', 'how', 'why', 'when', 'where'],
        'bug_report': ['bug', 'error', 'issue', 'problem', 'broken', 'fail', 'crash'],
        'suggestion': ['suggest', 'recommend', 'improve', 'better', 'could', 'should'],
        'approval': ['approve', 'lgtm', 'looks good', 'great', 'excellent', 'ok'],
        'request_change': ['change', 'fix', 'update', 'modify', 'correct', 'adjust'],
        'other': []
    }
    
    classified_comments = []
    action_items = []
    
    for comment in comments:
        # Get comment text
        comment_text = comment.get('body', '').lower()
        comment_author = comment.get('author', 'unknown')
        comment_date = comment.get('created_at', '')
        
        # Classify comment
        category = 'other'
        for cat, keywords in categories.items():
            if any(keyword in comment_text for keyword in keywords):
                category = cat
                break
        
        # Extract action items
        action_item_keywords = ['need to', 'should', 'must', 'fix', 'change', 'update', 'add', 'remove', 'implement']
        has_action_item = any(keyword in comment_text for keyword in action_item_keywords)
        
        classified_comment = {
            'author': comment_author,
            'created_at': comment_date,
            'body': comment.get('body', ''),
            'category': category,
            'has_action_item': has_action_item
        }
        classified_comments.append(classified_comment)
        
        # If it's an action item, add to the list
        if has_action_item:
            action_items.append({
                'author': comment_author,
                'created_at': comment_date,
                'comment': comment.get('body', ''),
                'status': 'pending'
            })
    
    # Calculate category counts
    category_counts = {}
    for cat in categories.keys():
        category_counts[cat] = len([c for c in classified_comments if c['category'] == cat])
    
    return {
        'classified_comments': classified_comments,
        'action_items': action_items,
        'category_counts': category_counts,
        'total_comments': len(classified_comments),
        'total_action_items': len(action_items)
    }

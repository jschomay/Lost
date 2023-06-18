def progress(min_bound, max_bound, value):
    """
    Returns a value between 0 and 1 based on the percentage between the bounds, clampped at the bounds.
    
    Examples:
        progress(100, 200, 150) = 0.5
        progress(100, 200, 250) = 1
        progress(100, 200, 50) = 0
    """
    return max(min((value - min_bound) / (max_bound - min_bound), 1), 0)

def check_range(value, upper_bound, lower_bound):
    if upper_bound < value or value < lower_bound:
        raise ValueError
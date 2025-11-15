def quicksort(arr):
    """
    Simplified quicksort implementation with detailed comments for educational purposes.
    Uses last element as pivot and includes clear step-by-step explanations.
    """
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose the last element as the pivot
    pivot = arr[-1]
    
    # Partition elements into three groups:
    # - Elements less than pivot
    # - Elements equal to pivot
    # - Elements greater than pivot
    less = []    # Elements < pivot
    equal = []   # Elements == pivot
    greater = [] # Elements > pivot
    
    # Categorize each element
    for element in arr:
        if element < pivot:
            less.append(element)
        elif element == pivot:
            equal.append(element)
        else:
            greater.append(element)
    
    # Recursively sort the 'less' and 'greater' groups, then combine results
    # This is the divide-and-conquer step
    return quicksort(less) + equal + quicksort(greater)

# Example usage with visual explanation
if __name__ == "__main__":
    # Test with various input types
    test_arrays = [
        [3, 6, 8, 10, 1, 2, 1],  # With duplicates
        [],                       # Empty array
        [5],                      # Single element
        [9, 7, 5, 11, 12, 2]      # Reverse sorted
    ]
    
    for arr in test_arrays:
        original = arr.copy()
        sorted_arr = quicksort(arr)
        print(f"Original: {original:20} Sorted: {sorted_arr}")
        
    # Step-by-step example for educational purposes
    print("\nStep-by-step example:")
    example = [4, 2, 6, 5, 3, 1]
    print(f"Sorting: {example}")
    print(f"1. Pivot = {example[-1]} (last element)")
    print(f"2. Partition: less={[x for x in example if x < example[-1]]}, equal={[example[-1]]}, greater={[x for x in example if x > example[-1]]}")
    print(f"3. Recursively sort subarrays and combine: {quicksort(example)}")
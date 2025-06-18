def bubblesort(arr):
    """
    Takes an array to be sorted.
    Returns a list of arrays with all intermediate sorting steps.
    """
    steps = [arr.copy()]
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr.copy())
    return steps
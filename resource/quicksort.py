def quicksort(arr, pivot_selector):
    steps = []
    _quicksort(arr, 0, len(arr), steps, pivot_selector)
    return steps

def _quicksort(A, left, right, steps, pivot_selector):
    if right - left <= 1:
        return  # Base case: One or zero elements
    
    pivot_index = pivot_selector(A, left, right)  # Get pivot index from function
    A[pivot_index], A[right - 1] = A[right - 1], A[pivot_index]  # Move pivot to end
    pivot = A[right - 1]

    lmbda = left  # Left pointer
    rho = right - 2  # Right pointer (before pivot)

    while lmbda <= rho:
        while lmbda <= rho and A[lmbda] < pivot:
            lmbda += 1
        while lmbda <= rho and A[rho] > pivot:
            rho -= 1

        if lmbda < rho:
            A[lmbda], A[rho] = A[rho], A[lmbda]
            lmbda += 1
            rho -= 1
            steps.append(A.copy())  # Save step

    # Place pivot at correct position
    A[right - 1], A[lmbda] = A[lmbda], A[right - 1]
    steps.append(A.copy())

    # Recursive calls for left and right partitions
    _quicksort(A, left, lmbda, steps, pivot_selector)   # Left part
    _quicksort(A, lmbda + 1, right, steps, pivot_selector)  # Right part

# Example pivot selection strategies:
def choose_first(A, left, right):
    return left

def choose_last(A, left, right):
    return right - 1

def choose_middle(A, left, right):
    return (left + right - 1) // 2

def choose_random(A, left, right):
    import random
    return random.randint(left, right - 1)


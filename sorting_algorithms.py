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
    
def selectionsort(arr):
    steps = [arr.copy()]
    i = 0
    while i < len(arr):
        smallest = i
        for j in range(i, len(arr)):
            if arr[j] < arr[smallest]:
                   smallest = j
        arr[i], arr[smallest] = arr[smallest], arr[i]
        steps.append(arr.copy())
        i += 1
    
    return steps
    
def insertionsort(arr):
    steps = [arr.copy()]
    for i in range(1,len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
        steps.append(arr.copy())
    return steps

def heapify(arr, k, l, steps):
    left_child = 2 * k + 1
    right_child = 2 * k + 2
    
    # Überprüfen, ob k keine Kinder hat
    if left_child >= l:
        return
    
    # Berechnung des maximalen Sohns
    if right_child == l or arr[left_child] > arr[right_child]:
        maxson = left_child
    else:
        maxson = right_child
    
    # Überprüfen, ob k bereits das Sickerziel ist
    if arr[k] >= arr[maxson]:
        return
    
    # Tauschen von k mit maxson
    arr[k], arr[maxson] = arr[maxson], arr[k]
    steps.append(arr.copy())
    
    # Rekursiver Aufruf
    heapify(arr, maxson, l, steps)

def buildheap(arr, steps):
    n = len(arr)
    for j in range(n // 2 - 1, -1, -1):
        heapify(arr, j, n, steps)

        
def heapsort(arr):
    steps = [arr.copy()]
    n = len(arr)
    
    # Großschritt 0: Falls n ≤ 1, Rückgabe
    if n <= 1:
        return
    
    # Großschritt 1: Aufbauphase des Heaps
    buildheap(arr, steps)
    
    # Großschritt 2: Auswahlphase
    heapsize = n
    while heapsize >= 2:
        arr[0], arr[heapsize - 1] = arr[heapsize - 1], arr[0]
        steps.append(arr.copy())
        # Verringern des Heapsizes
        heapsize -= 1
        # Reheapify den Heap (entspricht der heapify-Funktion)
        heapify(arr, 0, heapsize, steps)
    return steps
 
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
def pivot_first(A, left, right):
    return left

def pivot_last(A, left, right):
    return right - 1

def pivot_middle(A, left, right):
    return (left + right - 1) // 2

def pivot_random(A, left, right):
    import random
    return random.randint(left, right - 1)
           

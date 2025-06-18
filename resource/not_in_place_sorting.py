def counting_sort(A):
    B = len(A) * [0]
    C = len(A) * [0]
    for i in range(len(A)):
        C[A[i]-1] += 1
    for i in range(1,len(A)):
        C[i] += C[i-1]
    for i in range(len(A)-1, -1, -1):
        B[C[A[i]-1]-1] = A[i]
    return B

def counting_sort(A, exp):
    B = [0] * len(A)
    C = [0] * 10  # Digits range from 0-9

    # Count occurrences of digits at the current exponent place
    for i in range(len(A)):
        index = (A[i] // exp) % 10
        C[index] += 1

    # Convert C[] to store actual positions
    for i in range(1, 10):
        C[i] += C[i - 1]

    # Build the output array B[] in a stable way
    for i in range(len(A) - 1, -1, -1):
        index = (A[i] // exp) % 10
        B[C[index] - 1] = A[i]
        C[index] -= 1

    # Copy sorted values back to A
    for i in range(len(A)):
        A[i] = B[i]

def radix_sort(A):
    max_value = max(A)  # Find the maximum number to know digit count
    exp = 1  # Start with the least significant digit (1s place)

    while max_value // exp > 0:
        counting_sort(A, exp)
        print(A)
        exp *= 10  # Move to the next significant digit

# Example usage
A = [0.329, 0.457, 0.657, 0.839, 0.436, 0.720, 0.355]
radix_sort(A)
print(A)  # Output: [329, 355, 436, 457, 657, 720, 839]

def mergesort(steps, arr, left, right):
    if left < right:
        mid = (left + right) // 2
        mergesort(steps, arr, left, mid)
        mergesort(steps, arr, mid + 1, right)
        merge(steps, arr, left, mid, right)
    return steps

def merge(steps, arr, left, mid, right):
    temp = arr[left:right+1]  # Copy relevant portion
    i, j, k = 0, mid - left + 1, left

    while i <= mid - left and j < len(temp):
        if temp[i] <= temp[j]:
            arr[k] = temp[i]
            i += 1
        else:
            arr[k] = temp[j]
            j += 1
        k += 1
        steps.append(arr.copy())  # Store state

    while i <= mid - left:
        arr[k] = temp[i]
        i += 1
        k += 1
        #steps.append(arr.copy())

    while j < len(temp):
        arr[k] = temp[j]
        j += 1
        k += 1
    steps.append(arr.copy())

def track_mergesort():
    steps = []
    arr = [7,3,4,8,6,5,1,2]
    steps.append(arr.copy())  # Store initial state
    mergesort(steps, arr, 0, len(arr) - 1)
    return steps

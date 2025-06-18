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
            

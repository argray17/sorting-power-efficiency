"""
CS350-01: Analysis of Algorithms
Team Project 2: Analyzing Sorting Algorithms and Experimental Results
Group - APPLE 10: Austin Gray, Blake Bleem, & Sean Poston
Date: 11/01/2021
"""

import csv
import os
import random

MIN_MERGE = 32


def main(file="data.csv"):
    unsorted_data = load_data("datafiles/" + file)
    arr_names = ["Unsorted", "Heap Sort", "Merge Sort", "Quick Sort", "Radix Sort", "Tim Sort", "Selection Sort"]
    functions = [heap_sort, merge_sort, quick_sort, radix_sort, tim_sort, selection_sort]

    for i in range(len(functions)):
        arr = unsorted_data.copy()
        f = functions[i]
        name = arr_names[i+1]

        input("Press Enter to start " + name + '...')
        if f == quick_sort:
            f(0, len(arr)-1, arr)
        else:
            f(arr)

        name = name.lower().replace(' ', '_')
        write_csv_data(arr, "datafiles/" + name + '_' + file)
        print("Done")

    # print_data(arr_names, unsorted_data, heap_data, merge_data, quick_data, radix_data, tim_data, selection_data)


def load_data(file_path):
    data = []
    with open(os.path.join(os.getcwd(), file_path), 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(int(row[0]))
    return data


def write_csv_data(input_data, new_file_path):
    with open(os.path.join(os.getcwd(), new_file_path), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(map(lambda x: [x], input_data))

def print_data(arr_names, unsorted_data, heap_data, merge_data, quick_data, radix_data, selection_data, tim_data):
    n = len(unsorted_data)

    print("__________________________"
          "__________________________"
          "__________________________"
          "__________________________"
          "__________________________"
          "__________________________"
          "__________________________")

    header_format = "|{:^25s}|{:^25s}|{:^25s}|{:^25s}|{:^25s}|{:^25s}|{:^25s}|"
    print(header_format.format(
        arr_names[0],
        arr_names[1],
        arr_names[2],
        arr_names[3],
        arr_names[4],
        arr_names[5],
        arr_names[6]))

    print("|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________|")

    row_format = "|{:>8}: {:<15}|{:>8}: {:<15}|{:>8}: {:<15}|{:>8}: {:<15}|{:>8}: {:<15}|{:>8}: {:<15}|{:>8}: {:<15}|"
    for i in range(n):
        print(row_format.format(
            i + 1, unsorted_data[i],
            i + 1, heap_data[i],
            i + 1, merge_data[i],
            i + 1, quick_data[i],
            i + 1, radix_data[i],
            i + 1, selection_data[i],
            i + 1, tim_data[i]))

    print("|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________"
          "|_________________________|")


"""
HEAP SORT ALGORITHM
Source: https://www.geeksforgeeks.org/heap-sort/?ref=lbp
Date: 11/01/2021
"""


def heapify(heap_size, i, arr):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size and arr[largest] < arr[left]:
        largest = left

    if right < heap_size and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(heap_size, largest, arr)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i, arr)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0, arr)


"""
MERGE SORT ALGORITHM
Source: https://www.geeksforgeeks.org/merge-sort
Date: 11/01/2021
"""


def merge_sort(arr):
    n = len(arr)

    if n > 1:
        mid = n // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    return arr


"""
QUICK SORT ALGORITHM
Source: https://www.geeksforgeeks.org/quick-sort/
Date: 11/01/2021
"""


def partition(start, end, arr):
    pivot_idx = start
    pivot_val = arr[pivot_idx]

    while start < end:
        while start < len(arr) and arr[start] <= pivot_val:
            start += 1

        while arr[end] > pivot_val:
            end -= 1

        if start < end:
            arr[start], arr[end] = arr[end], arr[start]

    arr[end], arr[pivot_idx] = arr[pivot_idx], arr[end]

    return end


def quick_sort(start, end, arr):
    if len(arr) == 1:
        return arr

    if start < end:
        p = partition(start, end, arr)
        quick_sort(start, p-1, arr)
        quick_sort(p+1, end, arr)


"""
RADIX SORT ALGORITHM
Source: https://www.geeksforgeeks.org/radix-sort/
Date: 11/01/2021
"""


def counting_sort(arr, place):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(0, n):
        index = arr[i] // place
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // place
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(0, n):
        arr[i] = output[i]


def radix_sort(arr):
    max_element = max(arr)
    place = 1
    while max_element // place > 0:
        counting_sort(arr, place)
        place *= 10


"""
SELECTION SORT ALGORITHM
Source: https://www.geeksforgeeks.org/python-program-for-selection-sort/
Date: 11/01/2021
"""


def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


"""
TIM SORT ALGORITHM
Source: https://www.geeksforgeeks.org/timsort/
Date: 11/01/2021
"""


def calc_min_run(n):
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort(left_idx, right_idx, arr):
    for i in range(left_idx + 1, right_idx + 1):
        j = i
        while j > left_idx and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1


def tim_merge(left_idx, mid_idx, right_idx, arr):
    len1, len2 = mid_idx - left_idx + 1, right_idx - mid_idx
    left_arr, right_arr = [], []

    for i in range(0, len1):
        left_arr.append(arr[left_idx + i])
    for i in range(0, len2):
        right_arr.append(arr[mid_idx + 1 + i])

    i, j, k = 0, 0, left_idx

    while i < len1 and j < len2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1

        else:
            arr[k] = right_arr[j]
            j += 1

        k += 1

    while i < len1:
        arr[k] = left_arr[i]
        k += 1
        i += 1

    while j < len2:
        arr[k] = right_arr[j]
        k += 1
        j += 1


def tim_sort(arr):
    n = len(arr)
    min_run = calc_min_run(n)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(start, end, arr)

    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            if mid < right:
                tim_merge(left, mid, right, arr)

        size = 2 * size


def make_large_data(size, name="large_data.csv"):
    l = [i for i in range(size)]
    random.shuffle(l)
    write_csv_data(l, "datafiles/" + name)


if __name__ == "__main__":
    # make_large_data(10 ** 6)
    main("large_data.csv")

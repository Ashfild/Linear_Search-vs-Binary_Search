import kagglehub
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import random

path = kagglehub.dataset_download("elvinrustam/books-dataset")
print("Path to dataset files:", path)

dataset_file = f"{path}/BooksDataset.csv"
data = pd.read_csv(dataset_file)

print(data.columns)

books = data['Title'].dropna().sort_values().values
books = np.array(books)
print("Jumlah buku:", len(books))

# Fungsi Binary Search Iteratif
def binary_search_iterative(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Fungsi Binary Search Rekursif
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1  # Target tidak ditemukan
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# Fungsi Linear Search Iteratif
def linear_search_iterative(arr, target):
    n = len(arr)
    for i in range(0, n):
        if (arr[i] == target):
            return i
    return -1

# Fungsi Linear Search Rekursif
def linear_search_recursive(arr, target, index=0):
    if index >= len(arr):
        return -1  # Target tidak ditemukan
    if arr[index] == target:
        return index
    return linear_search_recursive(arr, target, index + 1)

# Simulasi Pencarian
def simulate_search(books, search_algo, *args):
    target = random.choice(books)
    start_time = time.time()
    search_algo(books, target, *args) if args else search_algo(books, target)
    return time.time() - start_time

sizes = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

binary_iterative_times_samples = []
binary_recursive_times_samples = []
linear_iterative_times_samples = []
linear_recursive_times_samples = []
dataset_sizes = []

for size in sizes:
    subset_books = books[:size]

    for _ in range(100):
        binary_iterative_search_time = simulate_search(subset_books, binary_search_iterative)
        binary_iterative_times_samples.append(binary_iterative_search_time)

        binary_recursive_search_time = simulate_search(subset_books, binary_search_recursive, 0, size - 1)
        binary_recursive_times_samples.append(binary_recursive_search_time)

        linear_iterative_search_time = simulate_search(subset_books, linear_search_iterative)
        linear_iterative_times_samples.append(linear_iterative_search_time)

        linear_recursive_search_time = simulate_search(subset_books, linear_search_recursive)
        linear_recursive_times_samples.append(linear_recursive_search_time)

        dataset_sizes.append(size)

# Membuat DataFrame untuk analisis
df = pd.DataFrame({
    'Ukuran Dataset': dataset_sizes,
    'Waktu Binary Search (detik)': binary_iterative_times_samples,
    'Waktu Binary Search Rekursif (detik)': binary_recursive_times_samples,
    'Waktu Linear Search (detik)': linear_iterative_times_samples,
    'Waktu Linear Search Rekursif (detik)': linear_recursive_times_samples
})

average_times = df.groupby('Ukuran Dataset').mean().reset_index()

print(average_times)

# Visualisasi Hasil
plt.figure(figsize=(15, 9))
plt.plot(average_times['Ukuran Dataset'], average_times['Waktu Binary Search (detik)'],
         label='Binary Search (Iteratif)', color='blue', marker='o')
plt.plot(average_times['Ukuran Dataset'], average_times['Waktu Binary Search Rekursif (detik)'],
         label='Binary Search (Rekursif)', color='green', marker='s')
plt.plot(average_times['Ukuran Dataset'], average_times['Waktu Linear Search (detik)'],
         label='Linear Search (Iteratif)', color='red', marker='x')
plt.plot(average_times['Ukuran Dataset'], average_times['Waktu Linear Search Rekursif (detik)'],
         label='Linear Search (Rekursif)', color='orange', marker='d')

plt.xlabel('Ukuran Dataset (Jumlah Buku)', fontsize=12)
plt.ylabel('Waktu Pencarian (detik)', fontsize=12)
plt.title('Perbandingan Waktu Pencarian: Binary Search vs Linear Search (Rata-rata)', fontsize=14)
plt.legend()

plt.grid(True)
plt.xscale('linear')
plt.yscale('log')
plt.show()

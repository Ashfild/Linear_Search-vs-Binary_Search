# -*- coding: utf-8 -*-
"""main.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DHym1V-dJYtGmMEz_CMRu8qN460GndFw
"""

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

def binary_search(arr, target):
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

def linear_search(arr, target):
    n = len(arr)
    for i in range(0, n):
        if (arr[i] == target):
            return i
    return -1

def simulate_search(books, search_algo):
    target = random.choice(books)

    start_time = time.time()
    search_algo(books, target)
    return time.time() - start_time

sizes = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

binary_times_samples = []
linear_times_samples = []
dataset_sizes = []

for size in sizes:
    subset_books = books[:size]

    for _ in range(100):
        binary_search_time = simulate_search(subset_books, binary_search)
        binary_times_samples.append(binary_search_time)

        linear_search_time = simulate_search(subset_books, linear_search)
        linear_times_samples.append(linear_search_time)

        dataset_sizes.append(size)

df = pd.DataFrame({
    'Ukuran Dataset': dataset_sizes,
    'Waktu Binary Search (detik)': binary_times_samples,
    'Waktu Linear Search (detik)': linear_times_samples
})

average_times = df.groupby('Ukuran Dataset').mean().reset_index()

print(average_times)

plt.figure(figsize=(15, 9))
plt.plot(average_times['Ukuran Dataset'], average_times['Waktu Binary Search (detik)'],
         label='Binary Search', color='blue', marker='o')
plt.plot(average_times['Ukuran Dataset'], average_times['Waktu Linear Search (detik)'],
         label='Linear Search', color='red', marker='x')

plt.xlabel('Ukuran Dataset (Jumlah Buku)', fontsize=12)
plt.ylabel('Waktu Pencarian (detik)', fontsize=12)
plt.title('Perbandingan Waktu Pencarian: Binary Search vs Linear Search (Rata-rata)', fontsize=14)
plt.legend()

plt.grid(True)
plt.xscale('linear')
plt.yscale('log')
plt.show()
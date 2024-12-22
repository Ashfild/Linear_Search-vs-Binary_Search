import random
import time
from bisect import bisect_left
import matplotlib.pyplot as plt

def random_vec(vec_len):
    """Membuat vektor acak terurut dengan panjang yang diberikan."""
    vec = [random.randint(0, 255) for _ in range(vec_len)]
    vec.sort()
    return vec

def random_vecs(num_vecs, vec_len):
    """Membuat beberapa vektor acak, masing-masing dengan nilai acak untuk dicari."""
    return [(random.randint(0, 255), random_vec(vec_len)) for _ in range(num_vecs)]

def linear_search(key, vec):
    """Melakukan pencarian linear untuk mencari nilai key di dalam vec dan menghitung perbandingan."""
    comparisons = 0
    for i, elem in enumerate(vec):
        comparisons += 1
        if elem == key:
            return comparisons  # Mengembalikan jumlah perbandingan ketika key ditemukan
        if elem > key:
            return comparisons  # Mengembalikan jumlah perbandingan jika key tidak ditemukan
    return comparisons  # Mengembalikan jumlah perbandingan jika key tidak ditemukan

def timed(func, *args, **kwargs):
    """Menjalankan fungsi dan mengukur waktu eksekusinya dalam milidetik."""
    start = time.time()
    result = func(*args, **kwargs)
    duration = (time.time() - start) * 1000  # Mengonversi ke milidetik
    return result, duration

def run(num_vecs, vec_len, iterations):
    """Menjalankan percobaan untuk pencarian linear dan pencarian biner."""
    vecs = random_vecs(num_vecs, vec_len)

    # Pencarian linear dan jumlah perbandingan
    def linear_work():
        total_comparisons = 0
        for _ in range(iterations):
            for key, vec in vecs:
                comparisons = linear_search(key, vec)
                total_comparisons += comparisons
        return total_comparisons

    linear_total_comparisons, _ = timed(linear_work)

    # Pencarian biner dan jumlah perbandingan
    def binary_work():
        total_comparisons = 0
        for _ in range(iterations):
            for key, vec in vecs:
                index = bisect_left(vec, key)
                comparisons = 1  # Pencarian biner selalu melakukan setidaknya satu perbandingan
                if index < len(vec) and vec[index] == key:
                    total_comparisons += comparisons
                else:
                    total_comparisons += comparisons
        return total_comparisons

    binary_total_comparisons, _ = timed(binary_work)

    # Menghitung rata-rata perbandingan per pencarian
    linear_avg_comparisons = linear_total_comparisons / (num_vecs * iterations)
    binary_avg_comparisons = binary_total_comparisons / (num_vecs * iterations)

    return vec_len, linear_avg_comparisons, binary_avg_comparisons

def main():
    num_vecs = 1000
    iterations = 100
    vec_lens = list(range(10, 256, 10))  # Ukuran array untuk diuji

    linear_avg_comparisons = []
    binary_avg_comparisons = []

    for vec_len in vec_lens:
        _, linear_avg, binary_avg = run(num_vecs, vec_len, iterations)
        linear_avg_comparisons.append(linear_avg)
        binary_avg_comparisons.append(binary_avg)

    # Menampilkan hasil dalam bentuk grafik
    plt.figure(figsize=(10, 6))
    plt.plot(vec_lens, linear_avg_comparisons, label="Pencarian Linear", color="red", marker="o")
    plt.plot(vec_lens, binary_avg_comparisons, label="Pencarian Biner", color="blue", marker="o")
    plt.title("Rata-rata Perbandingan per Pencarian (Pencarian Linear vs Pencarian Biner)")
    plt.xlabel("Panjang Array")
    plt.ylabel("Rata-rata Perbandingan")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()

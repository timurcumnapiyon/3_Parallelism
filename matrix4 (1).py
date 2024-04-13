import random
import numpy as np
import os
from multiprocessing import Pool
from multiprocessing import Pool, Manager
import time

# Функция перемножения элементов матриц
def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    return res

# Функция для распараллеливания вычислений
def parallel_multiply_matrices(A, B):
def parallel_multiply_matrices(A, B, result_queue, stop_event):
    if len(A[0]) != len(B):
        raise ValueError("Количество столбцов матрицы A должно быть равно количеству строк матрицы B")

    # Создаем список индексов для каждого элемента результирующей матрицы
    indices = [(i, j) for i in range(len(A)) for j in range(len(B[0]))]

    # Определяем количество параллельных потоков
    num_threads = os.cpu_count()

    # Создаем пул процессов
    with Pool(num_threads) as pool:
        # Выполняем перемножение элементов матриц параллельно с помощью функции element
        result_elements = pool.starmap(element, [(index, A, B) for index in indices])

    # Преобразуем список результатов в матрицу
    result_matrix = np.reshape(result_elements, (len(A), len(B[0])))
    try:
        for index in indices:
            if stop_event.is_set():
                return
            result = element(index, A, B)
            result_queue.put((index, result))
    except Exception as e:
        print("Error during matrix multiplication:", e)

    return result_matrix

# Функция для генерации случайной квадратной матрицы
def generate_random_matrix(size):
    return np.random.randint(0, 10, size=(size, size))

if __name__ == '__main__':
    a, b = map(int, input("For matrix1, a,b").split())
    c, d = map(int, input("For matrix2, c,d").split())
    # Создаем две случайные матрицы размером 5x5
    A = np.random.randint(0, 10, size=(a, b))
    B = np.random.randint(0, 10, size=(c, d))
    matrix_size = int(input("Enter the size of square matrices: "))
    stop_event = Manager().Event()
    result_queue = Manager().Queue()

    # Генерация двух случайных квадратных матриц
    A = generate_random_matrix(matrix_size)
    B = generate_random_matrix(matrix_size)

    try:
        # Выполняем перемножение матриц с использованием многопроцессорности
        result = parallel_multiply_matrices(A, B)

        # Выводим результат
        print("Matrix A:")
        print(A)
        print("\nMatrix B:")
        print(B)
        print("\nResult:")
        print(result)
         # Создаем пул процессов
        with Pool(processes=os.cpu_count()) as pool:
            # Запускаем процесс перемножения матриц
            process = pool.apply_async(parallel_multiply_matrices, (A, B, result_queue, stop_event))

            # Ждем некоторое время, а затем останавливаем процесс перемножения
            time.sleep(2)
            stop_event.set()

            # Получаем результаты из очереди
            results = []
            while not result_queue.empty():
                results.append(result_queue.get())

            # Выводим результаты
            print("Matrix A:")
            print(A)
            print("\nMatrix B:")
            print(B)
            print("\nResult:")
            result_matrix = np.zeros((matrix_size, matrix_size))
            for index, result in results:
                i, j = index
                result_matrix[i][j] = result
            print(result_matrix)
    except ValueError as e:
        print(e)

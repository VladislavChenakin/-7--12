import tkinter as tk # Создания графического GUI
from tkinter import scrolledtext, messagebox # Виджет для многострочного текста с прокруткой, Модуль для диалоговых окон
import itertools
import time
import random


def measure_time(func, N, K):
    start = time.perf_counter()
    result = func(N, K)
    end_time = time.perf_counter()
    return result, end_time - start


def algorithmic_method(N, K):
    result = []
    for v1 in range(1, N+1): #каждый цикл отвечает за выбор вагона для одного конкретного человека
        for v2 in range(1, N+1):
            if v2 == v1 or (v1, v2) in restricted: # Вагоны не должны совпадать и не должны находится рядом
                continue
            for v3 in range(1, N+1):
                if v3 in {v1, v2} or (v2, v3) in restricted:
                    continue
                for v4 in range(1, N+1):
                    if v4 in {v1, v2, v3} or (v3, v4) in restricted:
                        continue
                    result.append((v1, v2, v3, v4))
    return result


def itertools_method(N, K):
    all_perm = itertools.permutations(range(1, N + 1), K)  # Создает последовательность чисел от 1 до N, Генерирует все перестановки из N элементов по K
    allowed_permutations = []  # Вагоны не должны совпадать - permutations исключает повторения

    for p in all_perm:  # Перебираем все перестановки
        has_bad_pair = False

        # Проверяем соседние пары
        for i in range(K - 1):
            if (p[i], p[i + 1]) in restricted:  # Вагоны не должны находится рядом
                has_bad_pair = True
                break  # Дальше проверять нет смысла

        # Если все пары разрешены
        if not has_bad_pair:
            allowed_permutations.append(p)

    return allowed_permutations


# Целевая функция для оптимизации
def comfort_score(combination): #Принимает на вход кортеж с номерами вагонов
    return sum(comfort[wagon] for wagon in combination) #Возвращает суммарный комфорт всех вагонов в этой комбинации.


def create_interface():
    window = tk.Tk() #создаёт корневое окно приложения
    window.title("Оптимальная рассадка в вагонах") #заголовок окна
    window.geometry("900x700") #размер окна

    param_frame = tk.Frame(window) #контейнер для группировки элементов
    param_frame.pack(pady=5) #фрейм с отступом 10 пикселей сверху и снизу

    tk.Label(param_frame, text="Количество вагонов (N):").grid(row=0, column=0, padx=5)
    entry_n = tk.Entry(param_frame, width=10)
    entry_n.insert(0, "9")
    entry_n.grid(row=0, column=1, padx=5)

    tk.Label(param_frame, text="Количество людей (K):").grid(row=0, column=2, padx=5)
    entry_k = tk.Entry(param_frame, width=10)
    entry_k.insert(0, "4")
    entry_k.grid(row=0, column=3, padx=5)

    output_text = scrolledtext.ScrolledText(window, width=100, height=30, wrap=tk.WORD)
    output_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    def run_calculation():
        output_text.delete(1.0, tk.END)
        try:
            N = int(entry_n.get())
            K = int(entry_k.get())

            if N < 1 or K < 1 or K > N:
                raise ValueError("Некорректные значения: N ≥ 1, 1 ≤ K ≤ N")

            random.seed(42)
            global comfort, restricted
            comfort = {i: random.randint(1, 10) for i in range(1, N + 1)}
            restricted = {(1, 2), (3, 4), (7, 8)}

            output_text.insert(tk.END, "=" * 50 + "\n")
            output_text.insert(tk.END, f"Расчет для N={N}, K={K}\n")
            output_text.insert(tk.END, f"Уровни комфорта вагонов:\n{comfort}\n")
            output_text.insert(tk.END, "-" * 50 + "\n")

            # Алгоритмический метод
            output_text.insert(tk.END, "Алгоритмический метод:\n")
            window.update()
            algo_result, algo_time = measure_time(algorithmic_method, N, K)
            output_text.insert(tk.END,
                               f"Найдено вариантов: {len(algo_result)}\n"
                               f"Время выполнения: {algo_time:.4f} сек.\n\n")

            # Метод itertools
            output_text.insert(tk.END, "Itertools:\n")
            window.update()
            itertools_result, itertools_time = measure_time(itertools_method, N, K)
            output_text.insert(tk.END,
                               f"Найдено вариантов: {len(itertools_result)}\n"
                               f"Время выполнения: {itertools_time:.4f} сек.\n")
            output_text.insert(tk.END, "-" * 50 + "\n")

            # Поиск оптимальных решений
            if algo_result:
                output_text.insert(tk.END, "Оптимальное решение (алгоритм):\n")
                best_algo = max(algo_result, key=comfort_score)
                output_text.insert(tk.END,
                                   f"Оптимальная рассадка:\n{best_algo}\n"
                                   f"Общий комфорт: {comfort_score(best_algo)}\n\n")

            if itertools_result:
                output_text.insert(tk.END, "Оптимальное решение (itertools):\n")
                best_itertools = max(itertools_result, key=comfort_score)
                output_text.insert(tk.END,
                                   f"Оптимальная рассадка:\n{best_itertools}\n"
                                   f"Общий комфорт: {comfort_score(best_itertools)}\n")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(window,
              text="Начать расчет",
              command=run_calculation,
              bg="#4CAF50",
              fg="white").pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    create_interface()
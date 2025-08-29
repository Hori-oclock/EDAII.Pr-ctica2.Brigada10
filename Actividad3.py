import time
import random
import math
import matplotlib.pyplot as plt
from tabulate import tabulate

# =========================================================
# QUICK SORT (Particionar / QuickSort)
# =========================================================
def intercambia(A, x, y):
    tmp = A[x]; A[x] = A[y]; A[y] = tmp

def Particionar(A, p, r, contador):
    x = A[p]; i = p
    for j in range(p+1, r+1):
        contador['comparaciones'] += 1
        if A[j] <= x:
            i += 1
            intercambia(A, i, j)
    intercambia(A, i, p)
    return i

def QuickSort(A, p, r, contador):
    if p < r:
        q = Particionar(A, p, r, contador)
        QuickSort(A, p, q-1, contador)
        QuickSort(A, q+1, r, contador)

# =========================================================
# HEAP SORT (hIzq, hDer, maxHeapify, construir, ordenación)
# =========================================================
def hIzq(i): return 2*i + 1
def hDer(i): return 2*i + 2

def maxHeapify(A, i, sizeHeap, contador):
    L = hIzq(i); R = hDer(i)
    if (L <= sizeHeap-1) and (A[L] > A[i]): posMax = L
    else: posMax = i
    if (R <= sizeHeap-1) and (A[R] > A[posMax]): posMax = R

    # contar comparaciones con hijos existentes (hasta 2 por llamada)
    if L <= sizeHeap-1: contador['comparaciones'] += 1
    if R <= sizeHeap-1: contador['comparaciones'] += 1

    if posMax != i:
        intercambia(A, i, posMax)
        maxHeapify(A, posMax, sizeHeap, contador)

def construirHeapMaxIni(A, sizeHeap, contador):
    for i in range((math.ceil((sizeHeap-1)/2)), -1, -1):
        maxHeapify(A, i, sizeHeap, contador)

def ordenacionHeapSort(A, sizeHeap, contador):
    construirHeapMaxIni(A, sizeHeap, contador)
    for i in range(len(A)-1, 0, -1):
        intercambia(A, 0, i)
        sizeHeap -= 1
        maxHeapify(A, 0, sizeHeap, contador)

# =========================================================
# EXPERIMENTO – Actividad 3
# =========================================================
valores_n = [10, 50, 90, 130, 170, 210, 250]
resultados = []   # [n, t_quick, t_heap, c_quick, c_heap]

for n in valores_n:
    tiempos_q, tiempos_h, comps_q, comps_h = [], [], [], []
    for _ in range(5):  # 5 listas por n
        base = [random.randint(0, 1000) for _ in range(n)]

        Aq = base[:]; cq = {'comparaciones': 0}
        t0 = time.time(); QuickSort(Aq, 0, len(Aq)-1, cq)
        tiempos_q.append(time.time() - t0); comps_q.append(cq['comparaciones'])

        Ah = base[:]; ch = {'comparaciones': 0}
        t0 = time.time(); ordenacionHeapSort(Ah, len(Ah), ch)
        tiempos_h.append(time.time() - t0); comps_h.append(ch['comparaciones'])

    resultados.append([
        n,
        sum(tiempos_q)/len(tiempos_q),
        sum(tiempos_h)/len(tiempos_h),
        sum(comps_q)/len(comps_q),
        sum(comps_h)/len(comps_h),
    ])

# =========================================================
# TABLA
# =========================================================
print("\n=== Tabla comparativa (promedios sobre 5 corridas) ===")
headers = ["n", "Tiempo(Quick)", "Tiempo(Heap)", "Comparaciones(Quick)", "Comparaciones(Heap)"]
print(tabulate(resultados, headers=headers, tablefmt="grid"))

# =========================================================
# CURVAS TEÓRICAS ESCALADAS POR ALGORITMO
# Base teórica: O(n log n). Escalamos con el primer punto (n0 = 10).
# =========================================================
n_vals   = [r[0] for r in resultados]
t_quick  = [r[1] for r in resultados]
t_heap   = [r[2] for r in resultados]
c_quick  = [r[3] for r in resultados]
c_heap   = [r[4] for r in resultados]

def nlogn_series(ns): return [n * math.log2(n) for n in ns]

# Escalado individual para TIEMPO
nlogn = nlogn_series(n_vals)
n0 = n_vals[0]; base = n0 * math.log2(n0)
k_t_quick = t_quick[0] / base
k_t_heap  = t_heap[0]  / base
t_quick_teo = [k_t_quick * x for x in nlogn]
t_heap_teo  = [k_t_heap  * x for x in nlogn]

# Escalado individual para COMPARACIONES
k_c_quick = c_quick[0] / base
k_c_heap  = c_heap[0]  / base
c_quick_teo = [k_c_quick * x for x in nlogn]
c_heap_teo  = [k_c_heap  * x for x in nlogn]

# =========================================================
# GRÁFICAS
# =========================================================
# TIEMPO
plt.plot(n_vals, t_quick, marker='o', label="QuickSort (empírico)")
plt.plot(n_vals, t_heap,  marker='s', label="HeapSort (empírico)")
plt.plot(n_vals, t_quick_teo, linestyle="--", label="QuickSort (O(n log n) escalado)")
plt.plot(n_vals, t_heap_teo,  linestyle="--", label="HeapSort (O(n log n) escalado)")
plt.xlabel("n"); plt.ylabel("Tiempo (s)"); plt.title("Tiempo promedio vs n")
plt.legend(); plt.show()

# COMPARACIONES
plt.plot(n_vals, c_quick, marker='o', label="QuickSort (empírico)")
plt.plot(n_vals, c_heap,  marker='s', label="HeapSort (empírico)")
plt.plot(n_vals, c_quick_teo, linestyle="--", label="QuickSort (O(n log n) escalado)")
plt.plot(n_vals, c_heap_teo,  linestyle="--", label="HeapSort (O(n log n) escalado)")
plt.xlabel("n"); plt.ylabel("Comparaciones promedio"); plt.title("Comparaciones promedio vs n")
plt.legend()
plt.show()
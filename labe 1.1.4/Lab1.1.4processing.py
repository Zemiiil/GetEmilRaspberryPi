import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm
OUT_DIR = os.path.dirname(os.path.abspath(__file__)) #Сохранять файлы сюда
plt.rcParams.update({
    "font.size": 10, #шрифт
    "figure.dpi": 130,
    "axes.grid": True, #оси везде чтоб были
    "grid.alpha": 0.3, #сетка полупрозрачная
}) #Настройки на все последующие графики




DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Experiment1.1.4.csv")
#отсюда доставатть данные, путь к CSV рядом
df = pd.read_csv(DATA_PATH, header=None, comment="#", names=["n"]) #считывает данные в df
df["n"] = df["n"].astype(str).str.strip().astype(int) #превращает в строку убирает пробелы и привращает в числа
raw = df["n"].to_numpy() #теперь нампайный массив

T_total = 4000





taus = [10, 20, 40, 80]

results = {}  #словарь с данными для каждого tau

for tau in taus:
    N = T_total // tau
    bins = raw.reshape(N, tau).sum(axis=1) #делит массив на матрицу размером N строк и tau столбцов и потом суммирует числа в каждой строке и получается массив
    results[tau] = bins #записывает сюда результат





stats_rows = []
for tau in taus:
    bins = results[tau]
    N = len(bins)
    mean_n = bins.mean() #<n> считает
    std_n = bins.std(ddof=1) #среднеквадратичное отклонение
    err_mean = std_n / np.sqrt(N) #погрешность среднего
    j = mean_n / tau #интенсивность
    sigma_j = err_mean / tau #её погрешность

    stats_rows.append({
        "tau, c": tau,
        "N=t/tau": N,
        "<n>": mean_n,
        "sigma_n": std_n,
        "sqrt(<n>)": np.sqrt(mean_n),
        "sigma_<n>": err_mean,
        "j, 1/c": j,
        "sigma_j, 1/c": sigma_j,
    })


stats_df = pd.DataFrame(stats_rows) #массив в таблицу
pd.set_option("display.float_format", lambda x: f"{x:.4f}") #слишком много знаков после точки чтоб не было
print("\nСводная таблица статистики")
print(stats_df.to_string(index=False)) #выравнивание и убирание столбцов с индексами






fig, axes = plt.subplots(2, 2, figsize=(11, 8)) #чтоб 4 графика
axes = axes.ravel() #для удобства в одномерный массив

for ax, tau in zip(axes, taus): #по парам идет (axes[0], 10), (axes[1], 20), (axes[2], 40), (axes[3], 80)
    bins = results[tau]
    N = len(bins)
    mean_n = bins.mean()
    std_n = bins.std(ddof=1)

    n_min, n_max = bins.min(), bins.max()
    n_values = np.arange(n_min, n_max + 1)
    counts = np.array([(bins == n).sum() for n in n_values]) #поэлементно сравнивает каждый эл-т bins с n и считает совпадения
    w_n = counts / N  #массив из всех значений Wn
    #гистограмма ступенчатая/столбчатая
    ax.bar(n_values, w_n, width=0.9, color="#4C72B0", alpha=0.7,
           label="эксперимент", edgecolor="white") #строит график

    #Пуассон
    n_fine = np.arange(max(0, n_min - 2), n_max + 3) #чтоб гистограмма не обрывалась резко по краям
    poisson_pmf = poisson.pmf(n_fine, mu=mean_n)
    ax.plot(n_fine, poisson_pmf, "o-", color="#C44E52", ms=4,
             label=f"Пуассон (<n>={mean_n:.2f})")

    #Гаусс
    gauss_pdf = norm.pdf(n_fine, loc=mean_n, scale=std_n)
    ax.plot(n_fine, gauss_pdf, "s--", color="#55A868", ms=4,
             label=f"Гаусс (<n>={mean_n:.2f}, σ={std_n:.2f})")

    ax.set_title(f"τ = {tau} с   (N = {N} точек)")
    ax.set_xlabel("число отсчётов n")
    ax.set_ylabel("w$_n$")
    ax.legend(fontsize=8)

fig.suptitle("Экспериментальные распределения w$_n$ для разных τ\n"
             "с наложением теоретических распределений Пуассона и Гаусса", y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "histograms_all_tau.png"), dpi=150, bbox_inches="tight")
plt.close(fig)




#строим ещё один
tau_focus = 40
bins = results[tau_focus]
N = len(bins)
mean_n = bins.mean()
std_n = bins.std(ddof=1)
n_min, n_max = bins.min(), bins.max()
n_values = np.arange(n_min, n_max + 1)
counts = np.array([(bins == n).sum() for n in n_values])
w_n = counts / N

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(n_values, w_n, width=0.9, color="#4C72B0", alpha=0.7,
        label="эксперимент", edgecolor="white")
n_fine = np.linspace(max(0, n_min - 3), n_max + 3, 400)
n_int = np.arange(max(0, n_min - 3), n_max + 4)
ax2.plot(n_int, poisson.pmf(n_int, mu=mean_n), "o-", color="#C44E52",
          label=f"Пуассон (λ={mean_n:.2f})")
ax2.plot(n_fine, norm.pdf(n_fine, loc=mean_n, scale=std_n), "--",
          color="#55A868", lw=2, label=f"Гаусс (<n>={mean_n:.2f}, σ={std_n:.2f})")
ax2.set_title(f"Сравнение с теорией: τ = {tau_focus} с, N = {N}")
ax2.set_xlabel("число отсчётов n")
ax2.set_ylabel("w$_n$")
ax2.legend()
fig2.tight_layout()
fig2.savefig(os.path.join(OUT_DIR, "histogram_focus_tau40.png"), dpi=150, bbox_inches="tight")
plt.close(fig2)






print("\nПроверка sigma_n ~ sqrt(<n>)  (Var(n) = <n> для Пуассона)")
for tau in taus:
    bins = results[tau]
    N = len(bins)
    mean_n = bins.mean()
    std_n = bins.std(ddof=1)
    sqrt_mean = np.sqrt(mean_n)
    rel_diff = abs(std_n - sqrt_mean) / sqrt_mean * 100
    fano = std_n**2 / mean_n
    #погрешность самой оценки sigma_n
    sigma_of_sigma = std_n / np.sqrt(2 * (N - 1))
    print(f"tau={tau:>3} c:  sigma_n={std_n:.3f} +/- {sigma_of_sigma:.3f}   "
          f"sqrt(<n>)={sqrt_mean:.3f}   расхождение={rel_diff:.1f}%   ")






print("\n Доли |n-<n>| <= k*sigma_n ")
gauss_theory = {1: 0.6827, 2: 0.9545, 3: 0.9973}
frac_rows = []
for tau in taus:
    bins = results[tau]
    mean_n = bins.mean()
    std_n = bins.std(ddof=1)
    row = {"tau": tau}
    for k in (1, 2, 3):
        frac = np.mean(np.abs(bins - mean_n) <= k * std_n)
        row[f"k={k} (эксп.)"] = frac
        row[f"k={k} (Гаусс, теор.)"] = gauss_theory[k]
    frac_rows.append(row)

frac_df = pd.DataFrame(frac_rows)
print(frac_df.to_string(index=False))
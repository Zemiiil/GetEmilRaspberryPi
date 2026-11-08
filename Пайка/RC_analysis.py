# Обработка lab.csv: оценка постоянной времени tau = RC по зарядке и разрядке
# и сравнение с номиналом R1 = 1 МОм, C1 = 10 мкФ.
# Нужны только numpy и matplotlib.
# Результаты: графики в report/ и числа в report/results.json (для отчёта).
import json

import numpy as np
import matplotlib.pyplot as plt

CSV_NAME = "lab.csv"
OUT_DIR = "report"
R_NOM = 1.0e6    # Ом, R1: коричневый-чёрный-зелёный
C_NOM = 10e-6    # Ф, C1
TAU_NOM = R_NOM * C_NOM
DELTA_R = 0.05   # допуск R1
DELTA_C = 0.20   # допуск C1 (электролитический)

# Подписи рисунков делаются в отчёте, поэтому заголовков у графиков нет
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "Times New Roman", "DejaVu Serif"],
    "font.size": 12,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

data = np.loadtxt(CSV_NAME, delimiter=",", skiprows=1)
t, u, s = data[:, 0], data[:, 1], data[:, 2].astype(int)
tc, uc = t[s == 1], u[s == 1]
td, ud = t[s == 0], u[s == 0]
t_off = td[0]
tc = tc - tc[0]
td = td - td[0]


def level_tau(tt, uu, frac, rising):
    # время, за которое напряжение прошло долю frac от полного изменения
    u0, u1 = uu[0], (uu.max() if rising else uu.min())
    lvl = u0 + frac * (u1 - u0)
    idx = np.argmax(uu >= lvl) if rising else np.argmax(uu <= lvl)
    return tt[idx], lvl


def fit_exp(tt, uu, step=20):
    # МНК для u = A + B*exp(-t/tau): при фиксированном tau задача линейна по A, B,
    # tau перебираем по сетке (сначала грубо, потом точно)
    tt, uu = tt[::step], uu[::step]

    def sse(tau):
        X = np.column_stack([np.ones_like(tt), np.exp(-tt / tau)])
        coef, *_ = np.linalg.lstsq(X, uu, rcond=None)
        r = uu - X @ coef
        return r @ r, coef

    grid = np.arange(1.0, 30.0, 0.01)
    best = grid[np.argmin([sse(x)[0] for x in grid])]
    grid = np.arange(best - 0.02, best + 0.02, 0.0001)
    tau = grid[np.argmin([sse(x)[0] for x in grid])]
    res, (A, B) = sse(tau)
    rms = np.sqrt(res / len(tt))
    return tau, A, B, rms


def value_at(tt, uu, t0):
    return float(uu[np.argmin(np.abs(tt - t0))])


tau63, lvl63 = level_tau(tc, uc, 0.63, True)
tau37, lvl37 = level_tau(td, ud, 0.63, False)
tau_c, Ac, Bc, rms_c = fit_exp(tc, uc)
tau_d, Ad, Bd, rms_d = fit_exp(td, ud)

# линеаризация разрядки: ln(U - U_inf) = ln(U0) - t/tau
mask = (ud - Ad) > 0.05
k, b = np.polyfit(td[mask], np.log(ud[mask] - Ad), 1)
tau_ln = -1 / k

taus = np.array([tau63, tau37, tau_c, tau_d])
tau_mean = taus.mean()
tau_sigma = taus.std(ddof=1)
delta_nom = np.hypot(DELTA_R, DELTA_C)

print(f"Измерений: {len(t)}, длительность {t[-1]:.2f} с, частота {len(t) / t[-1]:.0f} Гц")
print(f"Зарядка:  U от {uc[0]:.3f} до {uc.max():.3f} В")
print(f"Разрядка: U от {ud[0]:.3f} до {ud.min():.3f} В")
print(f"tau (63 %, зарядка)   = {tau63:.3f} с, уровень {lvl63:.3f} В")
print(f"tau (37 %, разрядка)  = {tau37:.3f} с, уровень {lvl37:.3f} В")
print(f"tau (МНК, зарядка)    = {tau_c:.3f} с, U_inf = {Ac:.3f} В, СКО {rms_c * 1000:.1f} мВ")
print(f"tau (МНК, разрядка)   = {tau_d:.3f} с, U_inf = {Ad:.3f} В, СКО {rms_d * 1000:.1f} мВ")
print(f"tau (линеаризация)    = {tau_ln:.3f} с")
print(f"tau среднее = {tau_mean:.3f} +- {tau_sigma:.3f} с")
print(f"tau номинал = {TAU_NOM:.3f} +- {TAU_NOM * delta_nom:.2f} с, "
      f"отличие {(tau_mean - TAU_NOM) / TAU_NOM * 100:+.1f} %")

results = {
    "n_points": int(len(t)),
    "duration": float(t[-1]),
    "rate": float(len(t) / t[-1]),
    "dt_mean_ms": float(np.mean(np.diff(t)) * 1000),
    "u_charge_start": float(uc[0]), "u_charge_max": float(uc.max()),
    "u_dis_start": float(ud[0]), "u_dis_min": float(ud.min()),
    "tau63": float(tau63), "lvl63": float(lvl63),
    "tau37": float(tau37), "lvl37": float(lvl37),
    "tau_c": float(tau_c), "A_c": float(Ac), "B_c": float(Bc), "rms_c": float(rms_c),
    "tau_d": float(tau_d), "A_d": float(Ad), "B_d": float(Bd), "rms_d": float(rms_d),
    "tau_ln": float(tau_ln),
    "tau_mean": float(tau_mean), "tau_sigma": float(tau_sigma),
    "tau_nom": TAU_NOM, "delta_nom": float(delta_nom),
    # выборка точек для таблицы: каждые 5 с от начала этапа
    "samples": [[float(x), value_at(tc, uc, x), value_at(td, ud, x)]
                for x in np.arange(0, 50.1, 5)],
}
with open(f"{OUT_DIR}/results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

# Полный сигнал
plt.figure(figsize=(9, 4.8))
plt.plot(t, u, lw=0.8, label="измерение")
plt.axvline(t_off, color="red", ls="--", label="GPIO14 выключен")
plt.xlabel("Время t, с")
plt.ylabel("Напряжение на C1 U, В")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig_full.png", dpi=200)

# Зарядка
plt.figure(figsize=(9, 4.8))
plt.plot(tc, uc, lw=0.8, label="измерение")
plt.plot(tc, Ac + Bc * np.exp(-tc / tau_c), "r--", label=f"МНК: τ = {tau_c:.2f} с")
plt.axhline(lvl63, color="gray", ls=":")
plt.axvline(tau63, color="gray", ls=":", label=f"уровень 63 %: τ = {tau63:.2f} с")
plt.xlabel("Время от начала зарядки t, с")
plt.ylabel("U, В")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig_charge.png", dpi=200)

# Разрядка
plt.figure(figsize=(9, 4.8))
plt.plot(td, ud, lw=0.8, label="измерение")
plt.plot(td, Ad + Bd * np.exp(-td / tau_d), "r--", label=f"МНК: τ = {tau_d:.2f} с")
plt.axhline(lvl37, color="gray", ls=":")
plt.axvline(tau37, color="gray", ls=":", label=f"уровень 37 %: τ = {tau37:.2f} с")
plt.xlabel("Время от начала разрядки t, с")
plt.ylabel("U, В")
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig_discharge.png", dpi=200)

# Линеаризация разрядки
plt.figure(figsize=(9, 4.8))
plt.plot(td[mask], np.log(ud[mask] - Ad), lw=0.8, label="ln(U − U∞)")
plt.plot(td[mask], k * td[mask] + b, "r--", label=f"прямая, наклон −1/τ: τ = {tau_ln:.2f} с")
plt.xlabel("Время от начала разрядки t, с")
plt.ylabel("ln(U − U∞), U в вольтах")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig_ln.png", dpi=200)

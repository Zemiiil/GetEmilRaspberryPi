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


FIT_T = 30.0                 # с, основной участок аппроксимации (≈ 3τ)
FIT_T_SYS = (20.0, 40.0)     # с, участки для оценки систематической погрешности


def lin_mnk(x, y):
    """МНК для прямой y = K x + b: K, b, sigma_K и сумма квадратов остатков."""
    n = len(x)
    dx2 = np.mean(x * x) - x.mean() ** 2
    K = (np.mean(x * y) - x.mean() * y.mean()) / dx2
    b = y.mean() - K * x.mean()
    sK = np.sqrt(max((np.mean(y * y) - y.mean() ** 2) / dx2 - K ** 2, 0) / (n - 2))
    r = y - (K * x + b)
    return K, b, sK, r @ r


def fit_ln(tt, uu, t_max, charge):
    """Линеаризация: ln|U - U_inf| = ln|B| - t/tau, линейный МНК на участке t <= t_max.
    U_inf подбирается так, чтобы зависимость была ближе всего к прямой."""
    sign = -1 if charge else 1          # зарядка: U_inf - U > 0, разрядка: U - U_inf > 0
    edge = uu.max() if charge else uu.min()   # край всего этапа (50 с)
    m = tt <= t_max
    x, uu = tt[m], uu[m]

    def fit(ui):
        return lin_mnk(x, np.log(sign * (uu - ui)))

    grid = edge + sign * np.arange(-0.05, 0.3, 0.001)
    grid = [g for g in grid if np.all(sign * (uu - g) > 0)]
    best = grid[int(np.argmin([fit(g)[3] for g in grid]))]
    grid = np.arange(best - 0.001, best + 0.001, 0.0001)
    ui = grid[np.argmin([fit(g)[3] for g in grid])]
    K, b, sK, _ = fit(ui)
    return {"tau": -1 / K, "sigma_stat": sK / K ** 2, "U_inf": ui, "K": K, "b": b,
            "sigma_K": sK, "n": int(m.sum())}


def tau_with_errors(tt, uu, charge):
    main = fit_ln(tt, uu, FIT_T, charge)
    t1, t2 = (fit_ln(tt, uu, T, charge)["tau"] for T in FIT_T_SYS)
    main["tau_20"], main["tau_40"] = t1, t2
    main["sigma_sys"] = abs(t2 - t1) / 2
    main["sigma"] = float(np.hypot(main["sigma_stat"], main["sigma_sys"]))
    return main


def value_at(tt, uu, t0):
    return float(uu[np.argmin(np.abs(tt - t0))])


def value_at(tt, uu, t0):
    return float(uu[np.argmin(np.abs(tt - t0))])


tau63, lvl63 = level_tau(tc, uc, 0.63, True)
tau37, lvl37 = level_tau(td, ud, 0.63, False)
fc = tau_with_errors(tc, uc, charge=True)
fd = tau_with_errors(td, ud, charge=False)
tau_fin = (fc["tau"] + fd["tau"]) / 2
sigma_fin = np.hypot(fc["sigma"], fd["sigma"]) / 2
delta_nom = np.hypot(DELTA_R, DELTA_C)
eps = abs(TAU_NOM - tau_fin) / TAU_NOM

print(f"Измерений: {len(t)}, длительность {t[-1]:.2f} с, частота {len(t) / t[-1]:.0f} Гц")
print(f"tau (63 %, зарядка)  = {tau63:.3f} с, уровень {lvl63:.3f} В")
print(f"tau (37 %, разрядка) = {tau37:.3f} с, уровень {lvl37:.3f} В")
for name, f in (("зарядка", fc), ("разрядка", fd)):
    print(f"МНК {name}: tau = {f['tau']:.3f} с, U_inf = {f['U_inf']:.3f} В, "
          f"sigma_стат = {f['sigma_stat']:.4f} с, sigma_сист = {f['sigma_sys']:.3f} с "
          f"(tau(20 с) = {f['tau_20']:.3f}, tau(40 с) = {f['tau_40']:.3f}), sigma = {f['sigma']:.3f} с")
print(f"tau = {tau_fin:.3f} +- {sigma_fin:.3f} с; номинал {TAU_NOM:.1f} +- {TAU_NOM * delta_nom:.1f} с; "
      f"отличие {eps * 100:.1f} %")

results = {
    "n_points": int(len(t)),
    "duration": float(t[-1]),
    "rate": float(len(t) / t[-1]),
    "dt_mean_ms": float(np.mean(np.diff(t)) * 1000),
    "u_charge_start": float(uc[0]), "u_charge_max": float(uc.max()),
    "u_dis_start": float(ud[0]), "u_dis_min": float(ud.min()),
    "tau63": float(tau63), "lvl63": float(lvl63),
    "tau37": float(tau37), "lvl37": float(lvl37),
    "fit_T": FIT_T, "fit_T_sys": list(FIT_T_SYS),
    "charge": {k: float(v) for k, v in fc.items()},
    "discharge": {k: float(v) for k, v in fd.items()},
    "tau": float(tau_fin), "sigma": float(sigma_fin), "eps": float(eps),
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

# Зарядка и разрядка: данные, экспонента по параметрам линейного МНК, уровни 63 % / 37 %
def exp_curve(f, tt, charge):
    a = np.exp(f["b"]) * np.exp(f["K"] * tt)
    return f["U_inf"] - a if charge else f["U_inf"] + a


for name, tt, uu, f, charge, lvl, tl, lab, loc in (
        ("charge", tc, uc, fc, True, lvl63, tau63, "63 %", "lower right"),
        ("discharge", td, ud, fd, False, lvl37, tau37, "37 %", "upper right")):
    plt.figure(figsize=(9, 4.8))
    plt.plot(tt, uu, lw=0.8, label="измерение")
    plt.plot(tt, exp_curve(f, tt, charge), "r--", label=f"МНК: τ = {f['tau']:.2f} с")
    plt.axhline(lvl, color="gray", ls=":")
    plt.axvline(tl, color="gray", ls=":", label=f"уровень {lab}: τ = {tl:.2f} с")
    plt.xlabel("Время от начала " + ("зарядки" if charge else "разрядки") + " t, с")
    plt.ylabel("U, В")
    plt.legend(loc=loc)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig_{name}.png", dpi=200)

    # полулогарифмический масштаб
    m = tt <= FIT_T_SYS[1]
    y = np.log((f["U_inf"] - uu[m]) if charge else (uu[m] - f["U_inf"]))
    xf = np.array([0, FIT_T])
    plt.figure(figsize=(9, 4.8))
    plt.plot(tt[m], y, lw=0.8, label="ln(U∞ − U)" if charge else "ln(U − U∞)")
    plt.plot(xf, f["K"] * xf + f["b"], "r--", lw=1.5,
             label=f"МНК на 0–{FIT_T:.0f} с: наклон −1/τ, τ = {f['tau']:.2f} с")
    plt.axvspan(0, FIT_T, color="red", alpha=0.06)
    plt.xlabel("Время от начала " + ("зарядки" if charge else "разрядки") + " t, с")
    plt.ylabel(("ln(U∞ − U)" if charge else "ln(U − U∞)") + ", U в вольтах")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig_{name}_ln.png", dpi=200)

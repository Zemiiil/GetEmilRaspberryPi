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


FIT_T = 50.0       # с, основной участок аппроксимации: весь этап (≈ 5τ)
FIT_T_SYS = 25.0   # с, первая половина этапа — для оценки систематической погрешности


def lin_mnk(x, y):
    """МНК для прямой y = K x + b: K, b, их погрешности и сумма квадратов остатков."""
    n = len(x)
    dx2 = np.mean(x * x) - x.mean() ** 2
    K = (np.mean(x * y) - x.mean() * y.mean()) / dx2
    b = y.mean() - K * x.mean()
    sK = np.sqrt(max((np.mean(y * y) - y.mean() ** 2) / dx2 - K ** 2, 0) / (n - 2))
    sb = sK * np.sqrt(np.mean(x * x))
    r = y - (K * x + b)
    return K, b, sK, sb, r @ r


def fit_x(tt, uu, t_max):
    """Линеаризация U = K x + b, x = exp(-t/tau). tau подбирается так, чтобы
    зависимость U(x) была ближе всего к прямой (минимум суммы квадратов S(tau))."""
    m = tt <= t_max
    tt, uu = tt[m], uu[m]

    def S(tau):
        return lin_mnk(np.exp(-tt / tau), uu)[4]

    grid = np.arange(5.0, 15.0, 0.01)
    best = grid[np.argmin([S(g) for g in grid])]
    grid = np.arange(best - 0.02, best + 0.02, 0.0002)
    tau = grid[np.argmin([S(g) for g in grid])]
    # статистическая погрешность по кривизне S(tau) около минимума
    h = 0.002
    s2 = (S(tau + h) - 2 * S(tau) + S(tau - h)) / h ** 2
    s_min = S(tau)
    n = len(tt)
    K, b, sK, sb, _ = lin_mnk(np.exp(-tt / tau), uu)
    return {"tau": tau, "sigma_stat": np.sqrt(2 * s_min / ((n - 3) * s2)),
            "K": K, "b": b, "sigma_K": sK, "sigma_b": sb,
            "rms": np.sqrt(s_min / n), "n": n}


def tau_with_errors(tt, uu):
    main = fit_x(tt, uu, FIT_T)
    main["tau_half"] = fit_x(tt, uu, FIT_T_SYS)["tau"]
    main["sigma_sys"] = abs(main["tau"] - main["tau_half"]) / 2
    main["sigma"] = float(np.hypot(main["sigma_stat"], main["sigma_sys"]))
    return main


def value_at(tt, uu, t0):
    return float(uu[np.argmin(np.abs(tt - t0))])


tau63, lvl63 = level_tau(tc, uc, 0.63, True)
tau37, lvl37 = level_tau(td, ud, 0.63, False)
fc = tau_with_errors(tc, uc)
fd = tau_with_errors(td, ud)
tau_fin = (fc["tau"] + fd["tau"]) / 2
sigma_fin = np.hypot(fc["sigma"], fd["sigma"]) / 2
delta_nom = np.hypot(DELTA_R, DELTA_C)
eps = abs(TAU_NOM - tau_fin) / TAU_NOM

print(f"Измерений: {len(t)}, длительность {t[-1]:.2f} с, частота {len(t) / t[-1]:.0f} Гц")
print(f"tau (63 %, зарядка)  = {tau63:.3f} с, уровень {lvl63:.3f} В")
print(f"tau (37 %, разрядка) = {tau37:.3f} с, уровень {lvl37:.3f} В")
for name, f in (("зарядка", fc), ("разрядка", fd)):
    print(f"МНК {name}: tau = {f['tau']:.3f} с, K = {f['K']:.4f} В, b = U_inf = {f['b']:.4f} В, "
          f"СКО {f['rms'] * 1000:.1f} мВ, sigma_стат = {f['sigma_stat']:.4f} с, "
          f"tau(0-{FIT_T_SYS:.0f} с) = {f['tau_half']:.3f} с, sigma_сист = {f['sigma_sys']:.3f} с, "
          f"sigma = {f['sigma']:.3f} с")
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
    "fit_T": FIT_T, "fit_T_sys": FIT_T_SYS,
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

# Зарядка и разрядка: данные, экспонента по результату МНК, уровни 63 % / 37 %
for name, tt, uu, f, charge, lvl, tl, lab, loc in (
        ("charge", tc, uc, fc, True, lvl63, tau63, "63 %", "lower right"),
        ("discharge", td, ud, fd, False, lvl37, tau37, "37 %", "upper right")):
    stage = "зарядки" if charge else "разрядки"
    plt.figure(figsize=(9, 4.8))
    plt.plot(tt, uu, lw=0.8, label="измерение")
    plt.plot(tt, f["K"] * np.exp(-tt / f["tau"]) + f["b"], "r--", label=f"МНК: τ = {f['tau']:.2f} с")
    plt.axhline(lvl, color="gray", ls=":")
    plt.axvline(tl, color="gray", ls=":", label=f"уровень {lab}: τ = {tl:.2f} с")
    plt.xlabel(f"Время от начала {stage} t, с")
    plt.ylabel("U, В")
    plt.legend(loc=loc)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig_{name}.png", dpi=200)

    # линеаризация: U от x = exp(-t/tau)
    x = np.exp(-tt / f["tau"])
    xf = np.array([0, 1])
    plt.figure(figsize=(9, 4.8))
    plt.plot(x, uu, ".", ms=1.5, label="измерение")
    plt.plot(xf, f["K"] * xf + f["b"], "r--", lw=1.5,
             label=f"МНК: U = Kx + b, τ = {f['tau']:.2f} с")
    plt.xlabel(f"x = exp(−t/τ), τ = {f['tau']:.2f} с")
    plt.ylabel("U, В")
    plt.xlim(0, 1)
    plt.legend(loc="lower left" if charge else "upper left", markerscale=6)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig_{name}_x.png", dpi=200)

# Обработка lab.csv: оценка постоянной времени tau = RC по зарядке и разрядке
# и сравнение с номиналом R1 = 1 МОм, C1 = 10 мкФ.
# Нужны только numpy и matplotlib.
import numpy as np
import matplotlib.pyplot as plt

CSV_NAME = "lab.csv"
OUT_DIR = "report"
R_NOM = 1.0e6    # Ом, R1: коричневый-чёрный-зелёный
C_NOM = 10e-6    # Ф, C1
TAU_NOM = R_NOM * C_NOM

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

data = np.loadtxt(CSV_NAME, delimiter=",", skiprows=1)
t, u, s = data[:, 0], data[:, 1], data[:, 2].astype(int)
tc, uc = t[s == 1], u[s == 1]
td, ud = t[s == 0], u[s == 0]
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


tau63, lvl63 = level_tau(tc, uc, 0.63, True)
tau37, lvl37 = level_tau(td, ud, 0.63, False)
tau_c, Ac, Bc, rms_c = fit_exp(tc, uc)
tau_d, Ad, Bd, rms_d = fit_exp(td, ud)

taus = np.array([tau63, tau37, tau_c, tau_d])
tau_mean = taus.mean()
tau_spread = taus.std(ddof=1)

print(f"Измерений: {len(t)}, длительность {t[-1]:.2f} с, частота {len(t) / t[-1]:.0f} Гц")
print(f"Зарядка:  U от {uc[0]:.3f} до {uc.max():.3f} В")
print(f"Разрядка: U от {ud[0]:.3f} до {ud.min():.3f} В")
print(f"tau (63 %, зарядка)   = {tau63:.3f} с, уровень {lvl63:.3f} В")
print(f"tau (37 %, разрядка)  = {tau37:.3f} с, уровень {lvl37:.3f} В")
print(f"tau (МНК, зарядка)    = {tau_c:.3f} с, U_inf = {Ac:.3f} В, СКО {rms_c * 1000:.1f} мВ")
print(f"tau (МНК, разрядка)   = {tau_d:.3f} с, U_inf = {Ad:.3f} В, СКО {rms_d * 1000:.1f} мВ")
print(f"tau среднее = {tau_mean:.3f} +- {tau_spread:.3f} с")
print(f"tau номинал = {TAU_NOM:.3f} с, отличие {(tau_mean - TAU_NOM) / TAU_NOM * 100:+.1f} %")
print(f"R по tau при C = 10 мкФ: {tau_mean / C_NOM / 1e3:.0f} кОм")
print(f"C по tau при R = 1 МОм: {tau_mean / R_NOM * 1e6:.2f} мкФ")

# Рис. 1: полный сигнал
plt.figure(figsize=(9, 5))
plt.plot(t, u, lw=0.8, label="Измерение")
plt.axvline(t[s == 0][0], color="red", ls="--", label="GPIO14 выключен")
plt.xlabel("Время t, с")
plt.ylabel("Напряжение на C1, В")
plt.title("Зарядка и разрядка конденсатора C1 через R1")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig1_full.png", dpi=150)

# Рис. 2: зарядка и разрядка с аппроксимацией
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
ax[0].plot(tc, uc, lw=0.8, label="Измерение")
ax[0].plot(tc, Ac + Bc * np.exp(-tc / tau_c), "r--", label=f"МНК, τ = {tau_c:.2f} с")
ax[0].axhline(lvl63, color="gray", ls=":")
ax[0].axvline(tau63, color="gray", ls=":", label=f"63 %: τ = {tau63:.2f} с")
ax[0].set_title("Зарядка")
ax[1].plot(td, ud, lw=0.8, label="Измерение")
ax[1].plot(td, Ad + Bd * np.exp(-td / tau_d), "r--", label=f"МНК, τ = {tau_d:.2f} с")
ax[1].axhline(lvl37, color="gray", ls=":")
ax[1].axvline(tau37, color="gray", ls=":", label=f"37 %: τ = {tau37:.2f} с")
ax[1].set_title("Разрядка")
for a in ax:
    a.set_xlabel("Время от начала этапа, с")
    a.set_ylabel("U, В")
    a.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig2_fit.png", dpi=150)

# Рис. 3: линеаризация разрядки ln(U - U_inf) от t
mask = (ud - Ad) > 0.05
k, b = np.polyfit(td[mask], np.log(ud[mask] - Ad), 1)
plt.figure(figsize=(9, 4.5))
plt.plot(td[mask], np.log(ud[mask] - Ad), lw=0.8, label="ln(U − U∞)")
plt.plot(td[mask], k * td[mask] + b, "r--", label=f"прямая, наклон −1/τ, τ = {-1 / k:.2f} с")
plt.xlabel("Время от начала разрядки, с")
plt.ylabel("ln(U − U∞), U в вольтах")
plt.title("Разрядка в полулогарифмическом масштабе")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/fig3_ln.png", dpi=150)
print(f"tau (линеаризация разрядки) = {-1 / k:.3f} с")

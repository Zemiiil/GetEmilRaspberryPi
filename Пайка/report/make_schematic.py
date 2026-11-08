# Упрощённая схема RC-цепи для отчёта.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Liberation Serif", "Times New Roman", "DejaVu Serif"],
                     "font.size": 13})
fig, ax = plt.subplots(figsize=(7, 5))
ax.set_aspect("equal")
ax.axis("off")
kw = dict(color="black", lw=1.6)

# источник: выход GPIO14 Raspberry Pi
ax.add_patch(Rectangle((0, 7.2), 2.4, 1.6, fill=False, lw=1.6))
ax.text(1.2, 8.0, "Raspberry Pi\nGPIO14", ha="center", va="center")
ax.plot([2.4, 4], [8, 8], **kw)
# R1
ax.plot([4, 4], [8, 7], **kw)
ax.add_patch(Rectangle((3.7, 5.2), 0.6, 1.8, fill=False, lw=1.6))
ax.text(4.5, 6.1, "R1\n1 МОм", va="center")
ax.plot([4, 4], [5.2, 4.2], **kw)
# узел SIG
ax.plot(4, 4.2, "ko", ms=6)
ax.text(3.6, 4.2, "SIG", ha="right", va="center")
# C1
ax.plot([4, 4], [4.2, 3.2], **kw)
ax.plot([3.4, 4.6], [3.2, 3.2], color="black", lw=2.5)
ax.plot([3.4, 4.6], [2.9, 2.9], color="black", lw=2.5)
ax.text(4.8, 3.05, "C1\n10 мкФ", va="center")
ax.plot([4, 4], [2.9, 1.9], **kw)
# земля
for i, w in enumerate([0.6, 0.4, 0.2]):
    ax.plot([4 - w, 4 + w], [1.9 - i * 0.2] * 2, color="black", lw=1.6)
ax.text(4.0, 1.2, "GND", ha="center", va="top")
# АЦП
ax.plot([4, 7.2], [4.2, 4.2], **kw)
ax.add_patch(Rectangle((7.2, 3.4), 2.6, 1.6, fill=False, lw=1.6))
ax.text(8.5, 4.2, "АЦП\nMCP3021", ha="center", va="center")
# шина I2C от АЦП к Raspberry Pi
ax.plot([8.5, 8.5, 1.2, 1.2], [5.0, 9.3, 9.3, 8.8], color="gray", lw=1.0, ls="--")
ax.text(5.3, 9.45, "I²C", ha="center", color="gray")
ax.set_xlim(-0.2, 10)
ax.set_ylim(0.6, 9.9)
plt.tight_layout()
plt.savefig("fig_schematic.png", dpi=200, bbox_inches="tight")

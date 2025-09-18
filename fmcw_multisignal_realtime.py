import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# === Parameter Tetap FMCW ===
f_start = 24e9       # Frekuensi awal (Hz)
B = 100e6            # Bandwidth (Hz)
T_chirp = 10e-6      # Durasi 1 chirp (s)
fs = 2e9             # Sampling rate (Hz)

# === Waktu untuk 1 chirp ===
t_chirp = np.arange(0, T_chirp, 1/fs)
k = B / T_chirp  # slope

def update_plot(N_chirps):
    N_chirps = int(N_chirps)

    # === Generate sinyal untuk N_chirps ===
    s_chirp = np.cos(2 * np.pi * (f_start * t_chirp + 0.5 * k * t_chirp**2))
    s_t = np.tile(s_chirp, N_chirps)

    f_chirp = f_start + k * t_chirp
    f_t = np.tile(f_chirp, N_chirps)

    t_total = np.arange(0, N_chirps * len(t_chirp)) / fs

    # Update plot
    line1.set_data(t_total * 1e6, s_t)
    ax1.set_xlim(0, t_total[-1] * 1e6)
    ax1.set_ylim(-1.1, 1.1)

    line2.set_data(t_total * 1e6, f_t * 1e-9)
    ax2.set_xlim(0, t_total[-1] * 1e6)
    ax2.set_ylim((f_start - 0.1*B) * 1e-9, (f_start + 1.1*B) * 1e-9)

    fig.canvas.draw_idle()

# === Plot Awal ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

line1, = ax1.plot([], [], lw=1)
ax1.set_title("FMCW Signal (Time Domain)")
ax1.set_xlabel("Time (µs)")
ax1.set_ylabel("Amplitude")
ax1.grid()

line2, = ax2.plot([], [], lw=1)
ax2.set_title("Instantaneous Frequency")
ax2.set_xlabel("Time (µs)")
ax2.set_ylabel("Frequency (GHz)")
ax2.grid()

# === Slider untuk N_chirps ===
axcolor = 'lightgoldenrodyellow'
ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03], facecolor=axcolor)
chirp_slider = Slider(ax_slider, 'N_chirps', 1, 10, valinit=2, valstep=1)

chirp_slider.on_changed(update_plot)
update_plot(2)  # panggil pertama kali

plt.show()

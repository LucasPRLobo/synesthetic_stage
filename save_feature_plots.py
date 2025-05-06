import numpy as np
import json
import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === CONFIGURATION ===
feature_name = "RMS"  # Change this to: "Spectral Centroid", "Pitch", or "Beat Strength"
feature_index = {
    "RMS": 0,
    "Spectral Centroid": 1,
    "Pitch": 2,
    "Beat Strength": 6
}[feature_name]
feature_json = "features.json"
audio_file = "test_audio.wav"
output_filename = f"{feature_name.lower().replace(' ', '_')}_zoomed.mp4"

# === LOAD DATA ===
# Load feature matrix
with open(feature_json, "r") as f:
    feature_matrix = np.array(json.load(f))

# Load audio to determine timing
y, sr = librosa.load(audio_file, sr=44100)
duration = len(y) / sr
window_hop = 1024
window_duration = window_hop / sr
n_windows = len(feature_matrix)
time_axis = np.arange(n_windows) * window_duration

# Get data for selected feature
data = feature_matrix[:, feature_index]

# Calculate zoomed-in y-axis limits
min_val, max_val = data.min(), data.max()
margin = (max_val - min_val) * 0.1
y_min, y_max = min_val - margin, max_val + margin

# === CREATE ANIMATION ===
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, duration)
ax.set_ylim(y_min, y_max)
ax.set_title(f"{feature_name} Over Time (Zoomed)")
ax.set_xlabel("Time (s)")
ax.set_ylabel(feature_name)
ax.grid(True)

line, = ax.plot([], [], lw=2)
x_vals, y_vals = [], []

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t = time_axis[frame]
    x_vals.append(t)
    y_vals.append(data[frame])
    line.set_data(x_vals, y_vals)
    return line,

ani = animation.FuncAnimation(
    fig, update, frames=n_windows, init_func=init,
    blit=True, interval=1000 * window_duration
)

# === SAVE OUTPUT ===
ani.save(output_filename, writer='ffmpeg', fps=int(round(1 / window_duration)))
plt.close()
print(f"✅ Saved: {output_filename}")
